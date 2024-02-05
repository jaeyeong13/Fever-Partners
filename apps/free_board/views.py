from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def create_post(request):
  return HttpResponse('이것은 커뮤니티 페이지')
