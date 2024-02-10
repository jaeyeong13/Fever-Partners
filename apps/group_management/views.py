from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from apps.goal_management.models import Goal
from apps.alarm.models import Alarm
from apps.group_management.models import Room 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.urls import reverse
from elasticsearch_dsl import Search, Q
from apps.group_administration.decorators import room_admin_required

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
        my_goal.belonging_group_id = room.id
        my_goal.save()

        url = reverse('group_management:recommendation_page', kwargs={'room_id': room.pk})
        return redirect(url)
    
    else:
        return HttpResponseBadRequest('잘못된 접근방식입니다.')
    
# 임시로 작성해둠
def show_user_list(request):
    return render(request, 'group_management/member_recom.html')

@room_admin_required
def recommend_member(request, room_id):
    room = Room.objects.get(pk=room_id)
    tag_ids = [tag.id for tag in room.tags.all()]
    activity_tags_ids = [tag.id for tag in room.activityTags.all()]
    alarms = Alarm.objects.filter(room__pk=room_id)
    is_pending = [alarm.goal.pk for alarm in alarms]

    must_queries = []
    should_queries = []
    must_not_queries = []

    # 최소조건 명시 : 분류 태그 중 하나는 같아야 함(사실 이는 원시태그로 한정되긴 함)
    # group에 가입되지 않은 목표여야 함 
    at_least = Q('nested', path='tags', query=Q('terms', **{'tags.tag_id': tag_ids}), boost=0)
    in_group_check_query = Q('term', is_in_group = False)
    must_queries.append(at_least)
    must_queries.append(in_group_check_query)

    # 가중 조건 : 검색결과에 점수를 추가적으로 부여하는 로직들
    for tag_id in tag_ids:
        tag_query = Q('nested', path='tags', query=Q('terms', **{'tags.tag_id': [tag_id]}), boost=3)
        should_queries.append(tag_query)

    for activity_tag_id in activity_tags_ids:
        activity_tag_query = Q('nested', path='activityTags', query=Q('terms', **{'activityTags.tag_id': [activity_tag_id]}), boost=3)
        should_queries.append(activity_tag_query)

    offline_boost_query = Q('term', favor_offline={'value': room.favor_offline, 'boost': 2})
    should_queries.append(offline_boost_query)

    master_detecting_query = Q('term', **{'user.id': room.master.pk})
    must_not_queries.append(master_detecting_query)

    final_query = Q('bool', must=must_queries, should=should_queries, must_not=must_not_queries)
    
    s = Search(index='goals').query(final_query)
    response = s.execute()
    hit_ids = [hit.meta.id for hit in response]
    goals = Goal.objects.filter(pk__in=hit_ids).exclude(pk__in=is_pending)
    cnt = {
        'goals' : goals,
        'room' : room
    }
    return render(request, 'group_management/member_recom.html', cnt)

def suggest_join(request, room_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        goal_id = request.POST.get('goal_id')
        user = get_object_or_404(get_user_model(), id=user_id)
        room = get_object_or_404(Room, id=room_id)  # 방 정보 가져오기
        goal = get_object_or_404(Goal, id=goal_id)
        # 새 알람 객체 생성 시 인스턴스로 변환된 사용자를 할당
        Alarm.objects.create(alarm_from=request.user, alarm_to=user, room = room, goal = goal)
        return redirect(f'/group/member_recommendation/{room.id}')
    else:
        return redirect('/')  # POST 요청이 아닌 경우 홈페이지로 리다이렉트
    
def show_group_list(request):
    user = request.user
    rooms = Room.objects.filter(members__in = [user])
    return render(request, 'group_management/group_list.html', {'rooms': rooms})
