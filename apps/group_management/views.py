from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from apps.goal_management.models import Goal
from apps.user_management.models import User
from apps.alarm.models import Alarm
from apps.group_management.models import Room 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.urls import reverse

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

        return redirect(f'/group_management/recommendation_page/{room.id}')
    
    else:
        return HttpResponseBadRequest()
    
# 임시로 작성해둠
def show_user_list(request, room_id):
    room = Room.objects.get(pk=room_id)
    # 현재 로그인된 사용자 정보 가져오기
    current_user = request.user
    # is_superuser가 False이고 현재 로그인된 사용자가 아닌 사용자 정보 가져오기
    users = User.objects.filter(is_superuser=False).exclude(pk=current_user.pk)
    
    return render(request, 'group_management/member_recom.html', {'users': users, 'room':room})

def suggest_join(request, room_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(get_user_model(), id=user_id)
        room = get_object_or_404(Room, id=room_id)  # 방 정보 가져오기
        # 새 알람 객체 생성 시 인스턴스로 변환된 사용자를 할당
        Alarm.objects.create(alarm_from=request.user, alarm_to=user, room = room)
        return redirect(f'/group/member_recommendation/{room.id}')
    else:
        return redirect('/')  # POST 요청이 아닌 경우 홈페이지로 리다이렉트