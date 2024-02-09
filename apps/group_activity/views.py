from django.shortcuts import render
from apps.group_management.models import Room

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