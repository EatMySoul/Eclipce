from django.shortcuts import render , redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate ,login
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from Eclipse.models import Chats, Messages, Chats_users , Users_icons

from Eclipse.forms import JoinChatForm



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





def lobby(request, chat_title=""):
    if not request.user.is_authenticated:
        return redirect('/user/login/')
    user_id = request.user.id
    current_chat_icon_path  = None
    current_chat_messages = None
    user_status = 'User'
    if chat_title != "":
        try:
            current_chat = Chats.objects.get(title=chat_title)
            current_chat_icon_path = current_chat.icon
            current_chat_messages = Messages.objects.filter(chat=current_chat)
            user_status = Chats_users.objects.get(chat=current_chat,user_id=user_id).user_status
        except Chats.DoesNotExist:
            return redirect('/lobby')
        except Chats_users.DoesNotExist:
            return redirect('/lobby')
    users_chats = _get_user_chats(user_id)
    user_icon_path = Users_icons.objects.get(user_id=user_id).icon


    return render(request, 'chat/lobby.html' , {'user_icon_path' : user_icon_path,
                                                'users_chats' : users_chats,
                                                'chat_title': chat_title,
                                                'current_chat_icon_path' : current_chat_icon_path,
                                                'messages' : current_chat_messages,
                                                'user_status': user_status})




def join_chat(request):
    if request.method == "POST":
        try:
            chat = Chats.objects.get(title=request.POST['chat_title'])
            if chat.status == "Private":
                raise Chats.DoesNotExist
        except Chats.DoesNotExist:
            return redirect('/lobby')
        user_id = request.user.id
        chat_user = Chats_users(user_id=user_id, chat=chat, user_status='User')
        chat_user.save()
        url = '/lobby/' +  chat.title + '/'
        return redirect(url)
    return redirect('/lobby/')




def chat_setting(request, chat_title):
    if request.user.is_authenticated:
        user_id = request.user.id
        url = '/lobby/' + chat_title + '/'
        try:
            chat = Chats.objects.get(title=chat_title)
        except Chats.DoesNotExist:
            return redirect('/lobby')
        user_status = Chats_users.objects.get(user_id=user_id, chat=chat).user_status

        if user_status == "Admin":

            if request.method == "POST":
                if request.POST['chat_title']:

                    title = request.POST['chat_title']
                    try:
                        Chats.objects.get(title=title)
                        return redirect('/lobby')
                    except Chats.DoesNotExist:
                        chat = Chats.objects.get(title=chat_title)
                        chat.title = title
                        chat.save()


                return redirect(url)


            else:
                try:
                    chat = Chats.objects.get(title=chat_title)
                except Chats.DoesNotExist:
                    return redirect('/lobby')
                users = []
                chat_users = Chats_users.objects.filter(chat=chat)
                for chat_user in chat_users:
                    username =  User.objects.get(id=chat_user.user_id).username
                    icon_path = Users_icons.objects.get(user_id=chat_user.user_id).icon
                    users.append({'username' : username,
                                  'icon_path' : icon_path})



                return render(request, 'chat/chat_setting.html',{'users' : users,
                                                             'chat' : chat})
        else:
            return redirect('/lobby')
    else:
        return redirect('')




def create_chat(request):
    if request.method == "POST":
        if request.POST['chat_title']:
            chat_title = request.POST['chat_title']
            user_id = request.user.id
            try:
                Chats.objects.get(title=chat_title)
                return redirect('/lobby')
            except Chats.DoesNotExist:
                new_chat = Chats(title=chat_title,status='public')
                new_chat.save()
                chat_user = Chats_users(chat=new_chat,user_id=user_id,user_status='Admin')
                chat_user.save()
                url = '/lobby/' + chat_title + '/'
                return redirect(url)
    else:
        return redirect('/lobby')


def remove_chat(request,chat_title):
    print('removing ',chat_title)
    if request.user.is_authenticated:
        if request.method == "POST":

            user_id = request.user.id
            try:
                chat = Chats.objects.get(title=chat_title)
            except Chats.DoesNotExist:
                return redirect('/lobby')
            user_status = Chats_users.objects.get(user_id=user_id,chat=chat).user_status

            if user_status == "Admin":
                chat.delete()
            return redirect('/lobby')

def remove_chat_user(request,chat_title,username):
    if request.user.is_authenticated:

        user_id = request.user.id
        try:
            chat = Chats.objects.get(title=chat_title)
        except Chats.DoesNotExist:
            return redirect('/lobby')
        user_status = Chats_users.objects.get(user_id=user_id, chat=chat).user_status

        if user_status == "Admin":
            user_to_delete_id = User.objects.get(username=username).id
            user_to_delete = Chats_users.objects.get(chat=chat,user_id=user_to_delete_id)
            url = '/lobby/' + chat_title + '/setting/'
            if user_to_delete.user_status == "Admin":
                return redirect(url)
            else:
                user_to_delete.delete()
            return redirect(url)
        else:
            return redirect('/lobby')
    else:
        return redirect('')



def _get_user_chats(user_id):
    chats = Chats_users.objects.filter(user_id=user_id)
    return chats