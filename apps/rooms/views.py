from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import *
# Create your views here.

def detail(request):
    rooms = Room.objects.all()
    authentication_images = AuthenticationImage.objects.filter(room__in=rooms)
    return render(request, 'rooms/detail.html', {'room_list': rooms, 'authentication_images': authentication_images})

@login_required
def upload_image(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        image = request.FILES.get('image')
        if room_id and image:
            room = Room.objects.get(id=room_id)
            if request.user in room.members.all():
                auth_image = AuthenticationImage(room=room, user=request.user, image=image)
                auth_image.save()
                return redirect('rooms:detail')
    return HttpResponseBadRequest()