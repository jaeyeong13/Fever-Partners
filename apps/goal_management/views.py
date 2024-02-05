from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required

def start_creation(request):
    tags = Tag.objects.filter(parent_tag__isnull=True).order_by('tag_name')
    # Tony: 리턴의 키 값은 CamelCase여도 변수명은 snake_head로 해야합니다.
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
    # Tony: HTML 콘텐트를 JSON으로 리턴해주는 이유가 있나요?
    return JsonResponse({'result':html_content.decode('utf-8')})

def show_branching_point(request):
    return render(request, 'goal_management/branching_point.html')

@login_required
def create_goal(request):
    if request.method == 'POST':
        # Tony: 키 값에 -와 _가 혼재되어 있습니다.
        selected_tag_id = request.POST.get('selected_tag')
        activity_type_ids = request.POST.getlist('activity-type[]')
        title = request.POST.get('goal-title')
        details = request.POST.get('goal-details')
        meeting_preference = request.POST.get('meeting-preference')
        
        # Tony: 위 로직과 중복됩니다.
        try:
            selected_subtag_id = request.POST.get('selected_subtag')
        except (ValueError, TypeError):
            selected_subtag_id = None

        # 서버사이드 validation => 추후에 수정
        # if not selected_tag_id or not activity_type_ids or not title or not details or not meeting_preference:
        #     return redirect('your_redirect_url')

        selected_tag = Tag.objects.get(id=selected_tag_id)
        activity_tags = ActivityTag.objects.filter(id__in=activity_type_ids)
        # Tony: form-data 형식으로 데이터를 받지 않고 JSON으로 받으면 Type을 받아 아래 로직을 생략할 수 있습니다.
        # Tony: https://velog.io/@hojin11choi/TIL-Django-JSON-request.body
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

# 사용자의 목표 리스트
def goal_list(request):
    # Tony: goals = request.user.goal.all() 한 줄로 가능
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
    # Tony: pk를 제공받았는데 pk를 리턴하는 이유가 있나요?
    # Tony: goal.id하면 pk를 호출할 수 있어 같은 데이터를 두 번 리턴합니다.
    ctx = {
        "goal": goal,
        "pk": pk,
        'tags':tags,
        'actTags':actTags,
    }
    return render(request, "goal_management/goal_update.html", ctx)