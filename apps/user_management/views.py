from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout

def start(request):
    return render(request, "user_management/start.html")

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            user = User.objects.get(email=email)
            
            if user.check_password(raw_password):
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    else:
        msg = None
        form = LoginForm()
    return render(request, "user_management/login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("user_management:start")

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
    error_data = form.errors.as_data()
    if form.is_valid():
        user = form.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend') # 회원가입한 사용자를 자동으로 로그인
        return redirect("user_management:nickname") # 회원가입 성공 시 리다이렉트
    else:
        print(error_data)
        return redirect("user_management:signup_email")
    
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
