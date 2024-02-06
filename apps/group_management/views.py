from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from apps.goal_management.models import Goal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .forms import AuthenticationForm, MemberAuthenticationForm

def start_creation(request):
    goals = Goal.objects.filter(user = request.user).filter(is_in_group = False)
    cnt = {
        'goals':goals
    }
    return render(request, 'group_management/group_creation.html', cnt)

@login_required
def create_room(request):
    if request.method == 'POST':
        goal_id = request.POST.get('goal')
        title = request.POST.get('title')
        detail = request.POST.get('detail')
        cert_required = request.POST.get('cert_required')
        cert_detail = request.POST.get('cert_detail', '')
        penalty = request.POST.get('penalty', 0)
        favor_offline_str = request.POST.get('favor_offline', 'False')
        favor_offline = favor_offline_str == 'True'

        # 서버사이드 validation
        # if not goal_id or not title or not detail:
        #     return redirect('your_redirect_url')

        my_goal = get_object_or_404(Goal, pk=goal_id)

        room = Room.objects.create(
            title = title,
            detail = detail,
            master=request.user,
            cert_required = bool(cert_required),
            favor_offline = favor_offline
        )

        if bool(cert_required):
            room.cert_detail = cert_detail
            room.penalty_value = int(penalty)
        
        # 일단은 master도 member로 추가, 혹시 문제가 되면 수정
        room.members.add(request.user)
        room.tags.set(my_goal.tags.all())
        room.activityTags.set(my_goal.activityTags.all())
        room.save()
        
        my_goal.is_in_group = True
        my_goal.save()

        return redirect('group_management:recommendation_page')
    
    else:
        return HttpResponseBadRequest()
    
# 임시로 작성해둠
def show_user_list(request):
    return render(request, 'group_management/member_recom.html')

def show_group_list(request):
    user = request.user
    rooms = Room.objects.filter(members__in = [user])

    return render(request, 'group_management/group_list.html', {'rooms': rooms})

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
    }
    return render(request, 'group_management/group_activate.html', ctx)

#그룹장이 방에 인증 틀을 생성하는 것
def create_auth(request, pk):
    if request.method == 'GET':
        form = AuthenticationForm()

        ctx = {
            'form': form,
            'pk': pk,
            }
        return render(request, 'group_management/create_auth.html', ctx)

    # POST일때
    form = AuthenticationForm(request.POST)
    room = get_object_or_404(Room, id=pk)
    
    form.instance.room = room
    form.instance.user = request.user
    form.save()

    return redirect('group_management:activate', pk=room.id)

#그룹장이 올린 인증 틀에 멤버들이 인증을 생성하는 것
def create_authentication(request, pk):
    if request.method == 'GET':
        form = MemberAuthenticationForm()

        ctx = {
            'form': form,
            'pk': pk,
            }
        return render(request, 'group_management/create_authentication.html', ctx)

    # POST일때
    form = MemberAuthenticationForm(request.POST, request.FILES)
    room = get_object_or_404(Room, id=pk)
    
    form.instance.room = room
    form.instance.user = request.user
    form.save()

    return redirect('group_management:activate', pk=room.id)

#그룹장이 인증확인 창으로 이동
@login_required
def verify(request, pk):
    memberAuthentication = MemberAuthentication.objects.filter(room=pk)
    
    ctx = {
        'memberAuthentication':memberAuthentication,
    }
    return render(request, 'group_management/verifying_auth.html', ctx)

#def auth_log(request):
#    # 인증 없애고
#    auth = MemberAuthentication.objects.get()
#    # 로그 생성하고
#    # verify로 ㄱㄱ