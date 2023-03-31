from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
def main(request):
    print(">>>>>>>>>>>>>>>>> main")
    if request.session.get('session_user_id'):
        print('>>>>>>>>>>>>>>>>> session active')
        context = {}
        context['name'] = request.session['session_name']
        context['img'] = request.session['session_img']
        context['user_id'] = request.session['session_user_id']

        return render(request, 'board/main.html', context)
    else :
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

    paginator = Paginator(boards,3)
    page = int(request.GET.get('page',1))
    board_list = paginator.get_page(page)




    context ={'boards' : board_list}
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
    id = request.GET['id']
    board = board_tbl.objects.get(id= id)
    board.viewcount = board.viewcount +1
    board.save()

    # replys = reply_tbl.objects.filter(board_id = board.id)

    context = {'board':board}
    context['name'] = request.session['session_name']
    context['img'] = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    return render(request, 'board/read.html', context)

def delete(request):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>delete")
    id = request.GET['id']
    board_tbl.objects.get(id= id).delete()
    return redirect('list')

def update(request):
    id = request.GET['id']
    title = request.GET['title']
    content = request.GET['content']
    print(">?>>>>>>>>>>>>>>>>",id, title, content)
    board = board_tbl.objects.get(id=id)
    board.title = title
    board.content = content
    board.save()

    return redirect('list')

def logout(request):
    print("l>>>>>>>>>>>>>>>>>logout")
    request.session['session_name'] = {}
    request.session['session_img'] = {}
    request.session['session_user_id'] = {}
    return redirect('index')

def search(request):
    print(">>>>>>>>>>>>>>>>>search  : ajax Json Response")
    type = request.POST['searchType']
    keyword = request.POST['searchKeyword']
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>type, keyword ", type, keyword)

    if type == 'title':
        # select * from table where title like '%keyword%'
        boards = board_tbl.objects.filter(title__icontains= keyword)
    elif type == 'writer':
        # select * from table where title like 'keyword%'

        boards = board_tbl.objects.filter(writer_id= keyword)

    print('>>>>>>>>>>>> check : ', len(boards), boards)


    response_json =[]
    for board in boards:
        response_json.append({
            'id' : board.id,
            'title': board.title,
            'writer' : board.writer.user_id,
            'regdate': board.regdate,
            'viewcount' : board.viewcount
        })
    print(response_json)
    return JsonResponse(response_json, safe=False)