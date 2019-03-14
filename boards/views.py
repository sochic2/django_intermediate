from django.shortcuts import render, redirect
from .models import Board, Comment
# from pprint import pprint

# Create your views here.

    
def index(request):
    # pprint(request)     #pprint 세개 하고 웹페이지 새로고침하면 WSGIRequest, class 'django.core.handlers, 블라블라 뜸'
    # pprint(type(request))
    # pprint(dir(request))
    # pprint(request.scheme)
    # pprint(request.get_host())
    # pprint(request.get_full_path())
    # pprint(request.build_absolute_uri())  
    # pprint(request.META)
    # pprint(request.method)
    
    boards = Board.objects.order_by('-pk')    
    context = {
        'boards' : boards,
    }
    return render(request, 'boards/index.html', context)

def new(request):
    if request.method == 'POST':
        # CREATE
        # new.html, edit.html에서 form에 action이 없어도 자기 자신의 주소로 보내는 행동을 한다.
        title = request.POST.get('title')
        content = request.POST.get('content')
    
        board = Board(title=title, content=content)
        board.save()    
        
        return redirect('boards:detail', board.pk)

    else:
        return render(request, 'boards/new.html')
    

def detail(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    comments = board.comment_set.all()
    
    
    context = {
        'board': board,
        'comments':comments,
    }
    return render(request, 'boards/detail.html', context)
    
    
def delete(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    if request.method == 'POST':
        board.delete()
        return redirect('boards:index')
        
    else:
        return redirect('boards:detail', board.pk)
    
def edit(request, board_pk):
    if request.method == 'POST':
        #UPDATE
        board = Board.objects.get(pk=board_pk)
        board.title = request.POST.get('title')
        board.content = request.POST.get('content')
        board.save()
        return redirect('boards:detail', board.board_pk)
    
    else:
        # EDIT
        board = Board.objects.get(pk=board_pk)
        context = {
            'board' : board,
        }
        return render(request, 'boards/edit.html', context)
        
def comments_create(request, board_pk):
    # 댓글을 달 게시물 가져오기
    board = Board.objects.get(pk=board_pk)
    
    # form에서 넘어온 comment data!
    content = request.POST.get('content')
    
    # 댓글 생성 및 저장
    # 앞의 board는 board_id 인데 orm에서는 board라고 적어야함!!
    comment = Comment(board=board, content=content)
    comment.save()
    return redirect('boards:detail', board.pk)
    
def comments_delete(request, board_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('boards:detail', board_pk)
    
    else:
        return redirect('boards:detail', board_pk)
