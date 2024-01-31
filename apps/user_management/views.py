from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, authenticate
from .models import User

def start(request):
    return render(request, "user_management/start.html")

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 사용자 인증
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # 사용자가 인증되었을 때 로그인
            login(request, user)
            return redirect('user_management:main')
        else:
            # 인증 실패 시 처리
            return render(request, 'user_management/login.html', {'error': 'Invalid email or password'})

    return render(request, 'user_management/login.html')

def user_signup(request):
    return render(request, "user_management/signup.html")

def user_signup_email(request):
    if request.method == "GET":
        form = CustomUserCreationForm()
        ctx = {
            "form": form,
        }
        return render(request, "user_management/signup_email.html", ctx)
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user) # 회원가입한 사용자를 자동으로 로그인
        return redirect("user_management:nickname") # 회원가입 성공 시 리다이렉트
    
def user_nickname(request):
    if request.method == 'POST':
        form = UserNicknameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_management:main')  # nickname 설정 후 메인 페이지로 이동
    else:
        form = UserNicknameForm(instance=None)

    return render(request, 'user_management/input_nickname.html', {'form': form})

def main(request):
    return render(request, "user_management/main.html")

def detail(request, pk):
    user = User.objects.get(id=pk)
    ctx = {
        'user':user
    }
    return render(request, 'user_management/user_detail.html', ctx)