from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm

# Create your views here.
def board_list(request):
  post_list = Post.objects.order_by('-created_at')
  context = {'post_list': post_list}
  return render(request, 'free_board/board_list.html', context)

def post_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  context = {'post': post}
  return render(request, 'free_board/post_detail.html', context)

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:  # 댓글 내용이 있을 경우에만 생성
            # Comment 인스턴스를 직접 생성하고 저장하는 방법으로 변경
            comment = Comment(post=post, author=request.user, content=content, created_at=timezone.now())
            comment.save()
    return redirect('free_board:detail', post_id=post_id)


@login_required  # 로그인한 사용자만 글을 등록할 수 있도록 합니다.
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

@login_required  # 댓글을 달기 위해서는 로그인이 필요합니다.
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # 댓글이 속한 게시글을 설정합니다.
            comment.author = request.user  # 댓글 작성자를 현재 로그인한 사용자로 설정합니다.
            comment.save()
            return redirect('free_board:detail', post_id=post_id)
    else:
        form = CommentForm()
    context = {'post': post, 'form': form}
    return render(request, 'free_board/post_detail.html', context)