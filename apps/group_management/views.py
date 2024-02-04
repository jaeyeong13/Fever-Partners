from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from apps.goal_management.models import Goal
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

        url = reverse('group_management:recommendation_page', kwargs={'room_id': room.pk})
        return redirect(url)
    
    else:
        return HttpResponseBadRequest()
    
# 임시로 작성해둠
def show_user_list(request):
    return render(request, 'group_management/member_recom.html')

from elasticsearch_dsl import Search
from .models import *

def recommend_member(request, room_id):

    room = Room.objects.get(pk=room_id)
    tags = [tag.tag_name for tag in room.tags.all()]
    activity_tags = [tag.tag_name for tag in room.activityTags.all()]

    tag_queries = [{'terms': {'tags.tag_name': [tag], 'boost': 2}} for tag in tags]
    activity_tag_queries = [{'terms': {'activityTags.tag_name': [tag], 'boost': 2}} for tag in activity_tags]

    s = Search(index='goals').query(
        'bool',
        should=[
            *tag_queries,
            *activity_tag_queries,
            {'match': {'title': {'query': room.title, 'boost': 3}}},
            {'match': {'favor_offline': {'query': room.favor_offline, 'boost': 2}}},
        ]
    )   

    response = s.execute()
    goals = [Goal.objects.get(id=hit.meta.id) for hit in response]
    scores = [hit.meta.score for hit in response]
    cnt = {
        'goals' : goals,
        'scores' : scores,
    }
    return render(request, 'group_management/member_recom.html', cnt)