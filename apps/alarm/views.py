from django.shortcuts import redirect
from apps.alarm.models import Alarm

def delete(request, pk):
    if request.method == 'POST':
        Alarm.objects.get(id=pk).delete()
    return redirect('user_management:detail')