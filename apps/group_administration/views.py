from django.shortcuts import render
from apps.group_management.models import Room

# 이 부분 나중에 수정되어야 함
def show_admin_page(request, room_id):
    ctx = {
        'room_id':room_id,
    }
    return render(request, 'group_administration/group_admin_base.html', ctx)

def show_member_list(request, room_id):
    members = Room.objects.get(pk=room_id).members
    cnt = {
        'members':members,
        'room_id':room_id,
    }
    return render(request, 'group_administration/group_member_list.html', cnt)
