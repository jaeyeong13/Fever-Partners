from django.shortcuts import render
from apps.group_management.models import Room
from apps.goal_management.models import Goal
import json
from django.http import HttpResponse, JsonResponse
from apps.group_administration.views import show_member_list
from django.views.decorators.http import require_http_methods

def show_activity_main(request, room_id):
    cnt = {
        'room_id':room_id,
    }
    return render(request, 'group_activity/group_activity_base.html', cnt)

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