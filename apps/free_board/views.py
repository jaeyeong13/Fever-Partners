from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def create_post(request):
  post_list = Post.objects.order_by('-created_at')
  context = {'post_list': post_list}
  return render(request, 'free_board/board_list.html', context)

def post_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  context = {'post': post}
  return render(request, 'free_board/post_detail.html', context)

@login_required  # 댓글을 작성하려면 사용자가 로그인해야 합니다.
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:  # 댓글 내용이 있을 경우에만 생성
            # Comment 인스턴스를 직접 생성하고 저장하는 방법으로 변경
            comment = Comment(post=post, author=request.user, content=content, created_at=timezone.now())
            comment.save()
    return redirect('free_board:detail', post_id=post_id)
