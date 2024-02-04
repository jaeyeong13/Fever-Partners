from django.shortcuts import redirect,render
from apps.alarm.models import Alarm

def alarm_list(request):
    return render(request, 'alarm/alarm_list.html')

def delete(request, pk):
    if request.method == 'POST':
        Alarm.objects.get(id=pk).delete()
    return redirect('user_management:detail', pk=request.user.pk)