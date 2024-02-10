from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def post_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  context = {'post': post}
  return render(request, 'free_board/post_detail.html', context)


@login_required(login_url='user_management:login')  # 로그인한 사용자만 글을 등록할 수 있도록 합니다.
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.author = request.user  # 현재 로그인한 사용자를 글의 작성자로 설정합니다.
            post.save()
            return redirect('free_board:list')  # 글 목록 페이지로 리다이렉션
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'free_board/post_create.html', context)


@login_required(login_url='user_management:login')
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('free_board:detail', post_id=post_id)
    else:
        form = CommentForm()
    context = {'post': post, 'form': form}
    return render(request, 'free_board/post_detail.html', context)

# def index(request):
#     notice_posts = Post.objects.filter(notice=True).order_by('-created_at')
#     free_posts = Post.objects.filter(notice=False).order_by('-created_at')
#     # 공지 게시물과 자유 게시물을 하나의 리스트로 합치기 위해 chain을 사용합니다.
#     from itertools import chain
#     post_list = list(chain(notice_posts, free_posts))
#     paginator = Paginator(post_list, 8)  # 페이지당 게시글 수는 8로 설정
#     page = request.GET.get('page', '1')
#     page_obj = paginator.get_page(page)
#     context = {'post_list': page_obj}
#     return render(request, 'free_board/board_list.html', context)

def index(request):
    tab = request.GET.get('tab', 'notice')  # '공지' 탭을 기본값으로 설정

    if tab == 'notice':
        posts = Post.objects.filter(notice=True).order_by('-created_at')
    elif tab == 'free':
        posts = Post.objects.filter(notice=False).order_by('-created_at')
    else:
        posts = Post.objects.order_by('-created_at')

    paginator = Paginator(posts, 8)  # 페이지당 게시글 수는 8로 설정
    page = request.GET.get('page', '1')
    page_obj = paginator.get_page(page)

    context = {'page_obj': page_obj, 'tab': tab}
    return render(request, 'free_board/board_list.html', context)

@login_required(login_url='user_management:login')
def modify_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        messages.error(request, '수정 권한이 없습니다!')
        return redirect('free_board:detail', post_id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.updated_at = timezone.now()
            post.save()
            return redirect('free_board:detail', post_id=post.id)
    else:  # 폼이 처음 로드되었을 때 혹은 유효하지 않을 때
        form = PostForm(instance=post)

    context = {'form': form}
    return render(request, 'free_board/post_create.html', context)


@login_required(login_url='user_management:login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, "삭제 권한이 없습니다!")
        return redirect('free_board:detail', post_id=post.id)
    post.delete()
    return redirect('free_board:list')


@login_required(login_url='user_management:login')
def modify_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "수정 권한이 없습니다!")
        return redirect('free_board:detail', post_id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.updated_at = timezone.now()
            comment.save()
            return redirect('free_board:detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'free_board/comment_form.html', context)


@login_required(login_url='user_management:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제 권한이 없습니다!')
    else:
        comment.delete()
    return redirect('free_board:detail', post_id=comment.post.id)


@login_required(login_url='user_management:login')
def vote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        post.voter.add(request.user)
    return redirect('free_board:detail', post_id=post.id)

def view_notice(request, post_id):
    posts = Post.objects.filter(notice=True).order_by('-created_at')
    paginator = Paginator(posts, 10)  # 페이지 당 10개의 게시글을 보여줍니다.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'free_board/notice_posts.html', {'page_obj': page_obj})

def view_free(request, post_id):
    posts = Post.objects.filter(notice=False).order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'free_board/free_posts.html', {'page_obj': page_obj})