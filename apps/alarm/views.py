from django.shortcuts import redirect,render, get_object_or_404
from apps.alarm.models import Alarm
from django.contrib.auth.decorators import login_required

def show_alarms(request):
    alarms = Alarm.objects.filter(alarm_to=request.user) #현재 유저일때만
    alarm_data = [{'alarm': alarm, 'alarm_from_nickname': alarm.alarm_from.nickname} for alarm in alarms]
    return render(request, 'alarm/alarms.html', {'alarms': alarm_data})

def alarm_detail(request, pk):
    alarm = get_object_or_404(Alarm, pk=pk)
    
    context = {
        'alarm': alarm,
    }
    return render(request, 'alarm/alarm_detail.html', context)

@login_required
def accept_request(request, alarm_id):
    alarm = get_object_or_404(Alarm, id=alarm_id)
    room = alarm.room
    room.members.add(alarm.alarm_to)
    alarm.delete()

    return redirect('alarm:show_alarms')

@login_required
def reject_request(request, alarm_id):
    alarm = get_object_or_404(Alarm, id=alarm_id)

    alarm.delete()

    return redirect('alarm:show_alarms')