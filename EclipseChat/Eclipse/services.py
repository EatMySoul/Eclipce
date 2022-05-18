from Eclipse.models import Chats, Chats_users, Users_icons, User, Messages




def get_user_chats(user):
    return Chats_users.objects.filter(user=user)


def add_massage(message,username,chat_title):
    user = User.objects.get(username=username)
    chat = Chats.objects.get(title=chat_title)
    message = Messages(message=message,user=user,chat=chat)
    message.save()
    date_time = message.date_time.__str__()[:19]
    return date_time