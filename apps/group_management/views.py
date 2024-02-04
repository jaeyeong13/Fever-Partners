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

from elasticsearch_dsl import Search, Q
from .models import *

def recommend_member(request, room_id):

    room = Room.objects.get(pk=room_id)
    tags = [tag.tag_name for tag in room.tags.all()]
    activity_tags = [tag.tag_name for tag in room.activityTags.all()]

    tag_ids = [1, 5]
    activity_tags_ids = [1,2]

    queries = []
    queries2 = []

    must_query = Q('nested', path='tags', query=Q('terms', **{'tags.tag_id': tag_ids}), boost=0)
    queries.append(must_query)

    for tag_id in tag_ids:
        tag_query = Q('nested', path='tags', query=Q('terms', **{'tags.tag_id': [tag_id]}), boost=2)
        queries2.append(tag_query)

    for activity_tag_id in activity_tags_ids:
        activity_tag_query = Q('nested', path='activityTags', query=Q('terms', **{'activityTags.tag_id': [activity_tag_id]}), boost=2)
        queries2.append(activity_tag_query)

    offline_boost_query = Q('match', favor_offline={'query': False, 'boost': 3})
    queries2.append(offline_boost_query)

    combined_query = Q('bool', must=queries, should=queries2)
    
    s = Search(index='goals').query(combined_query)

    response = s.execute()

    print(response)
    goals = [Goal.objects.get(id=hit.meta.id) for hit in response]
    scores = [hit.meta.score for hit in response]
    cnt = {
        'goals' : goals,
        'scores' : scores,
        'room' : room
    }
    return render(request, 'group_management/member_recom.html', cnt)