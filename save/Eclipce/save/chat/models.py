from django.db import models

# Create your models here.


class Chats(models.Model):

    CHATS_STATUS = [
        ('pub','public'),
        ('sec', 'private')
    ]

    title = models.CharField(max_length=30,unique=True)
    status = models.CharField(max_length=20, choices=CHATS_STATUS)
    icon = models.ImageField(upload_to='chat/img/chats')

class Users(models.Model):

    name = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='chat/img/users')



class Massages(models.Model):

    massage = models.TextField()
    date_time = models.DateTimeField()
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class Chats_users(models.Model):

    USERS_STATUS = [
        ('A','Admin'),
        ('U','User')
    ]

    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=20,choices=USERS_STATUS)


