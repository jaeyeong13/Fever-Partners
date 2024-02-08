from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.decorators import login_required
from elasticsearch_dsl import Search, Q
from apps.group_management.models import Room

def start_creation(request):
    tags = Tag.objects.filter(parent_tag__isnull=True).order_by('tag_name')
    actTags = ActivityTag.objects.all()
    cnt = {
        'tags':tags,
        'actTags':actTags,
    }
    return render(request, 'goal_management/goal_creation.html', cnt)

def get_subtags(request, id):
    subtags = Tag.objects.filter(parent_tag__id = id)
    cnt = {
        'subtags':subtags
    }
    html_content = render(request, 'goal_management/subtag_container.html', cnt).content
    return JsonResponse({'result':html_content.decode('utf-8')})

def show_branching_point(request):
    return render(request, 'goal_management/branching_point.html')

@login_required
def create_goal(request):
    if request.method == 'POST':
        selected_tag_id = request.POST.get('selected_tag')
        activity_type_ids = request.POST.getlist('activity-type[]')
        title = request.POST.get('goal-title')
        details = request.POST.get('goal-details')
        meeting_preference = request.POST.get('meeting-preference')
        
        try:
            selected_subtag_id = request.POST.get('selected_subtag')
        except (ValueError, TypeError):
            selected_subtag_id = None

        # 서버사이드 validation => 추후에 수정
        # if not selected_tag_id or not activity_type_ids or not title or not details or not meeting_preference:
        #     return redirect('your_redirect_url')

        selected_tag = Tag.objects.get(id=selected_tag_id)
        activity_tags = ActivityTag.objects.filter(id__in=activity_type_ids)
        favor_offline = True if meeting_preference == 'True' else False

        goal = Goal.objects.create(
            user=request.user,
            title=title,
            content=details,
            favor_offline=favor_offline
        )

        goal.tags.add(selected_tag)
        goal.activityTags.set(activity_tags)

        if selected_subtag_id:
            selected_subtag = Tag.objects.get(id=selected_subtag_id)
            goal.tags.add(selected_subtag)

        return redirect('goal_management:show_branching_point')
    
    # GET 요청으로 접근한 경우 예외처리 추후에 추가
    # return redirect()

@login_required
def goal_list(request):
    user = request.user
    goals = user.goal.all()
    ctx = {
        "goals": goals,
    }
    return render(request, "goal_management/goal_list.html", ctx)

# 사용자의 목표 수정
def goal_update(request, pk):
    goal = Goal.objects.get(id=pk)
    tags = Tag.objects.filter(parent_tag__isnull=True).order_by('tag_name')
    actTags = ActivityTag.objects.all()
    ctx = {
        "goal": goal,
        "pk": pk,
        'tags':tags,
        'actTags':actTags,
    }
    return render(request, "goal_management/goal_update.html", ctx)

def recommend_group(request, goal_id):
    if request.method != 'POST':
        return HttpResponseNotFound('<h1>잘못된 접근방식입니다.</h1>')

    goal = Goal.objects.get(pk=goal_id)
    tag_ids = [tag.id for tag in goal.tags.all()]
    activity_tag_ids = [tag.id for tag in goal.activityTags.all()]

    must_queries = []
    should_queries = []
    must_not_queries = []

    # 최소조건 명시: 분류 태그 중 하나는 같아야 함
    at_least_tag = Q('nested', path='tags', query=Q('terms', **{'tags.tag_id': tag_ids}), boost=0)
    must_queries.append(at_least_tag)

    # 가중 조건: 검색결과에 점수를 추가적으로 부여하는 로직들
    for tag_id in tag_ids:
        tag_query = Q('nested', path='tags', query=Q('terms', **{'tags.tag_id': [tag_id]}), boost=3)
        should_queries.append(tag_query)

    for activity_tag_id in activity_tag_ids:
        activity_tag_query = Q('nested', path='activityTags', query=Q('terms', **{'activityTags.tag_id': [activity_tag_id]}), boost=3)
        should_queries.append(activity_tag_query)

    # favor_offline이 같을 경우 높은 점수
    offline_boost_query = Q('term', favor_offline={'value': goal.favor_offline, 'boost': 2})
    should_queries.append(offline_boost_query)
    
    # is_active가 False일때만 추천 목록에 반영 
    is_active_query = Q('term', is_active=False)
    must_queries.append(is_active_query)

    # Goal의 user는 Room의 master가 아니여야함. 즉 자기자신이 개설한 방에 대해서는 목록에 반영하지 않음.
    # => 상식적으로 이럴 일은 없겠으나, 일단 예외처리함
    user_master_mismatch_query = Q('term', master__id=goal.user.id)
    must_not_queries.append(user_master_mismatch_query)

    final_query = Q('bool', must=must_queries, should=should_queries, must_not=must_not_queries)
    s = Search(index='rooms').query(final_query)
    response = s.execute()

    room_ids = [hit.meta.id for hit in response]
    rooms = Room.objects.filter(pk__in=room_ids)
    cnt = {
        'rooms': rooms, 
        'goal': goal
    }
    return render(request, 'goal_management/group_recom.html', cnt)