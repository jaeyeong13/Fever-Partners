from django.shortcuts import render, redirect, get_object_or_404
from apps.group_management.models import Room
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import AuthenticationForm, MemberAuthenticationForm

def show_activity_main(request, room_id):
    ctx = {
        'room_id':room_id,
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
    
    ctx = {
        'memberAuthentication':memberAuthentication,
        'room_id':pk,
    }
    return render(request, 'group_activity/verifying_auth.html', ctx)

#인증 수락을 눌렀을 때
def accept_auth_log(request, pk):
    memberAuthentication = MemberAuthentication.objects.get(id=pk)
    memberAuthentication.is_auth = True
    memberAuthentication.is_completed = True
    memberAuthentication.save()

    return redirect('group_activity:verify', memberAuthentication.room.id)

#겹치는 코드가 많아서 합칠 수 있을 거 같은데..
#인증 거절을 눌렀을 때
def refuse_auth_log(request, pk):
    memberAuthentication = MemberAuthentication.objects.get(id=pk)
    memberAuthentication.is_completed = True
    memberAuthentication.save()

    return redirect('group_activity:verify', memberAuthentication.room.id)

#현황(인증로그) 창으로 이동
def show_log(request, pk):
    auth_log = MemberAuthentication.objects.filter(room=pk)
    
    ctx = {
        'auth_log':auth_log,
    }
    return render(request, 'group_activity/show_log.html', ctx)