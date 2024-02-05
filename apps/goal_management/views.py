from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required

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
