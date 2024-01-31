from django.shortcuts import render
from .models import User

# Create your views here.
def detail(request, pk):
    user = User.objects.get(id=pk)
    ctx = {
        'user':user
    }
    return render(request, 'user_management/user_detail.html', ctx)