from django.shortcuts import render

# 이 부분 나중에 수정되어야 함
def show_admin_page(request, room_id):
    return render(request, 'group_administration/group_admin_base.html')