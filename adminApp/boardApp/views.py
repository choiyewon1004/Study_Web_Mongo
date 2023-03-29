from django.shortcuts import render, redirect
from boardApp.models import user_tbl
from boardApp.models import board_tbl

# Create your views here.
def main(request):
    print(">>>>>>>>>>>>>>>>> main")
    return render(request, 'board/index.html')

def login(request):
    print(">>>>>>>>>>>>>>>>> login")
    id = request.POST['id']
    pwd = request.POST['pwd']

    user = user_tbl.objects.get(user_id = id, user_pwd = pwd)

    request.session['session_name'] = user.user_name
    request.session['session_img'] = user.user_img
    request.session['session_user_id'] = user.user_id
    context = {}
    context['name']= request.session['session_name']
    context['img']= request.session['session_img']
    context['user_id']= request.session['session_user_id']

    return render(request, 'board/main.html', context)

def list(request):
    print(">>>>>>>>>>>>>>>>> list")
    boards = board_tbl.objects.all().order_by('-id')
    print(type(boards))
    context ={'boards' : boards}
    context['name'] = request.session['session_name']
    context['img'] = request.session['session_img']
    context['user_id'] = request.session['session_user_id']
    return render(request, 'board/list.html', context)

def joinForm(request):
    print(">>>>>>>>>>>>>>>>>>>>>>joinForm")
    return render(request, 'board/join.html')

def join(request):
    print(">>>>>>>>>>>>>>>>>>>>>>join")

    id = request.POST.get('id')
    pwd = request.POST.get('pwd')
    name = request .POST.get('name')
    print("id : ",id, "   pwd : ", pwd, "  name : ", name)


    user_tbl(user_id = id, user_pwd = pwd, user_name = name, user_img='boy.png').save()

    return redirect('index')

def registerForm(request):
    context = {}
    context['name'] = request.session['session_name']
    context['img'] = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    return render(request, 'board/register.html', context)

def register(request):

    title = request.POST.get('title')
    content = request.POST.get('content')
    writer = request.POST.get('writer')
    # print(">>>>>>>>>>>>>>>>>>>>>>>print",title, content, writer)
    user = user_tbl.objects.get(user_id=writer)
    # print("writer >>>>>>>>>>>>>>>>>>", user)
    board_tbl(title=title, writer=user, content=content).save()

    return redirect('list')

# 게시글의 식별번호 id를 파라미터로 받아 해당 게시글의 정보를 DB에서 select 후 화면으로 렌더링
def read(request) :
    print(">>>>>>>>>>>>>>>>>>>>>view : ")

    board = board_tbl.objects.get(id=request.GET['id'])
    context = {'board':board}
    context['name'] = request.session['session_name']
    context['img'] = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    return render(request, 'board/read.html', context)

def delete(request):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>delete")
    board_id = board_tbl.objects.get(id=request.GET['id'])
    print(board_tbl.objects.get(id = board_id))
    return redirect('list')