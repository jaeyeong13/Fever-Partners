from django.shortcuts import render

def show_activity_main(request, room_id):
    return render(request, 'group_activity/group_activity_base.html')