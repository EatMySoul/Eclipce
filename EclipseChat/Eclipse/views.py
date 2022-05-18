from django.shortcuts import render , redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate ,login
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from Eclipse.models import Chats, Massages, Chats_users , Users_icons



def index(request):
    print(request.user)
    if not request.user.is_authenticated:
        return redirect('/user/login/')
    else:
        return redirect('/lobby/')


def registrate_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        check_pass = request.POST['passwordRepeat']

        if password == check_pass:
            try:
                user = User.objects.create_user(username=username, password=password)
                Users_icons(user=user).save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/lobby')
            except IntegrityError:
                return HttpResponse("Error username already exist")
        else:
            return HttpResponse("passwords are dont match")


def registration_page(request):

    return render(request , 'chat/regist.html')

def lobby(request):
    if not request.user.is_authenticated:
        return redirect('/user/login/')
    user_id = request.user.id
    users_chats = _get_user_chats(user_id)
   # print('title of chat',chats[0].chat.title)
    user_icon_path = Users_icons.objects.get(user_id=user_id).icon



    return render(request, 'chat/lobby.html' , {'user_icon_path' : user_icon_path, 'users_chats' : users_chats})


def lobby_setting(request):

    return render(request, 'chat/chat_setting.html')


def _get_user_chats(user_id):
    chats = Chats_users.objects.filter(user_id=user_id)
    return chats