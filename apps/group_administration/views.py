from django.shortcuts import render
from apps.group_management.models import Room
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
import json
from .decorators import room_admin_required

# 이 부분 나중에 수정되어야 함
@room_admin_required
def show_admin_page(request, room_id):
    ctx = {
        'room_id':room_id,
    }
    return render(request, 'group_administration/group_admin_base.html', ctx)

@room_admin_required
def show_member_list(request, room_id):
    master = Room.objects.get(pk=room_id).master
    members = Room.objects.get(pk=room_id).members.exclude(pk=master.pk)
    cnt = {
        'members':members,
        'room_id':room_id,
    }
    return render(request, 'group_administration/group_member_list.html', cnt)

@require_http_methods(["DELETE"])
def expel_member(request):
    try:
        data = json.loads(request.body)
        room_id = data.get('roomId')
        member_id = data.get('memberId')

        room = Room.objects.get(pk=room_id)
        member = room.members.get(pk=member_id)

        # 추방에 따른 로직 => 관련 정보 수정 및 초기화
        target_goal = member.goal.filter(belonging_group_id=room_id).first()
        target_goal.is_in_group = False
        target_goal.belonging_group_id = None
        target_goal.save()

        room.members.remove(member)
        return JsonResponse({'message': '멤버가 성공적으로 삭제되었습니다.'}, status=200)
    except Exception:
        return HttpResponse(status=400)

@require_http_methods(["POST"]) 
def transfer_master(request):
    try:
        data = json.loads(request.body)
        room_id = data.get('roomId')
        member_id = data.get('memberId')

        room = Room.objects.get(pk=room_id)
        room.master = room.members.get(pk=member_id)
        room.save()

        return JsonResponse({'message': '권한이 성공적으로 양도되었습니다.'}, status=200)
    except Exception:
        return HttpResponse(status=400)