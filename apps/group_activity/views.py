from django.shortcuts import render, redirect, get_object_or_404
from apps.group_management.models import Room
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import AuthenticationForm, MemberAuthenticationForm
from apps.goal_management.models import Goal
import json
from django.http import HttpResponse, JsonResponse
from apps.group_administration.views import show_member_list
from django.views.decorators.http import require_http_methods

def show_activity_main(request, room_id):
    room = Room.objects.get(pk=room_id)
    ctx = {
        'room_id':room_id,
        'room': room,
    }
    return render(request, 'group_activity/group_activity_base.html', ctx)

#그룹 활동 페이지로..(임시작성)
def activate(request, pk):
    room = get_object_or_404(Room, id=pk)
    authentication = Authentication.objects.filter(room=room)
    master = False
    if room.master == request.user:
        master = True
    ctx = {
        'room': room,
        'authentication': authentication,
        'master':master,
        'room_id':pk,
    }
    return render(request, 'group_activity/group_activate.html', ctx)

#그룹장이 방에 인증 틀을 생성하는 것
def create_auth(request, pk):
    if request.method == 'GET':
        form = AuthenticationForm()

        ctx = {
            'form': form,
            'pk': pk,
            }
        return render(request, 'group_activity/create_auth.html', ctx)

    # POST일때
    form = AuthenticationForm(request.POST)
    room = get_object_or_404(Room, id=pk)
    
    form.instance.room = room
    form.instance.user = request.user
    form.save()

    return redirect('group_activity:activate', pk=room.id)

#그룹장이 올린 인증 틀에 멤버들이 인증을 생성하는 것
def create_authentication(request, pk):
    if request.method == 'GET':
        form = MemberAuthenticationForm()

        ctx = {
            'form': form,
            'pk': pk,
            }
        return render(request, 'group_activity/create_authentication.html', ctx)

    # POST일때
    form = MemberAuthenticationForm(request.POST, request.FILES)
    room = get_object_or_404(Room, id=pk)
    
    form.instance.room = room
    form.instance.user = request.user
    form.save()

    return redirect('group_activity:activate', pk=room.id)

#그룹장이 인증확인 창으로 이동
@login_required
def verify(request, pk):
    memberAuthentication = MemberAuthentication.objects.filter(room=pk).filter(is_completed=False)
    room_id = pk
    room = Room.objects.get(pk = room_id)
    ctx = {
        'memberAuthentication':memberAuthentication,
        'room_id':pk,
        'room':room,
    }
    return render(request, 'group_activity/verifying_auth.html', ctx)

#인증 수락을 눌렀을 때
def accept_auth_log(request, pk):
    memberAuthentication = MemberAuthentication.objects.get(id=pk)
    user =  memberAuthentication.user
    user.fuel = add_fever(user.fuel)
    user.save()
    memberAuthentication.is_auth = True
    memberAuthentication.is_completed = True
    memberAuthentication.save()

    return redirect('group_activity:verify', memberAuthentication.room.id)

#겹치는 코드가 많아서 합칠 수 있을 거 같은데..
#인증 거절을 눌렀을 때
def refuse_auth_log(request, pk):
    memberAuthentication = MemberAuthentication.objects.get(id=pk)
    user =  memberAuthentication.user
    user.fuel = loss_fever(user.fuel)
    user.save()
    memberAuthentication.is_completed = True
    memberAuthentication.save()

    return redirect('group_activity:verify', memberAuthentication.room.id)

def add_fever(fever):
    if 0 <= fever <= 25:
        fever_after = fever + 5
    elif 25 < fever <= 50:
        fever_after = fever + 1
    elif 50 < fever <= 75:
        fever_after = fever + 0.5
    elif 75 < fever <= 100:
        fever_after = max(100, fever + 0.1)
    return fever_after

def loss_fever(fever):
    if 0 <= fever <= 25:
        fever_after = max(0, fever - 1)
    elif 25 < fever <= 50:
        fever_after = fever - 3
    elif 50 < fever <= 75:
        fever_after = fever - 5
    elif 75 < fever <= 100:
        fever_after = fever - 10
    return fever_after

#현황(인증로그) 창으로 이동
def show_log(request, pk):
    auth_log = MemberAuthentication.objects.filter(room=pk).filter(is_completed=True).order_by('-created_date')
    
    ctx = {
        'auth_log':auth_log,
        'room_id':pk,
    }
    return render(request, 'group_activity/show_log.html', ctx)

def show_member_list(request, room_id):

    member_goal_pairs = {}
    room = Room.objects.get(id=room_id)
    for member in room.members.all():
        target_goal = member.goal.all().get(belonging_group_id=room_id)
        member_goal_pairs[member] = target_goal

    cnt = {
        'room_id': room_id,
        'member_goal_pairs': member_goal_pairs,
    }

    return render(request, 'group_activity/member_list.html', cnt)

@require_http_methods(["POST"])
def permission_check(request):
    try:
        data = json.loads(request.body)
        room_id = data.get('roomId')
        user_id = data.get('userId')

        master = Room.objects.get(pk=room_id).master
        if master.pk != user_id:
            return HttpResponse(status=403)
        return HttpResponse(status=204)
    except Exception:
        return HttpResponse(status=400)

@require_http_methods(["POST"])
def withdraw_from_room(request):
    try:
        data = json.loads(request.body)
        room_id = data.get('roomId')
        user_id = data.get('userId')
        
        room = Room.objects.get(pk=room_id)
        master = room.master
        # 관리자는 바로 탈퇴 불가능
        if master.pk == user_id:
            return HttpResponse(status=403)
        
        target = room.members.get(pk=user_id)
        room.members.remove(target)
        room.save()

        #Goal을 리셋하는 작업
        target_goal = Goal.objects.filter(user__pk=user_id).get(belonging_group_id=room_id)
        target_goal.belonging_group_id = None
        target_goal.is_in_group = False
        target_goal.save()
        
        return JsonResponse({'message':'탈퇴처리가 성공적으로 완료되었습니다.'}, status=200)
    except Exception:
        return HttpResponse(status=400)
