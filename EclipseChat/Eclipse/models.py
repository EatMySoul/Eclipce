from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from Eclipse.managers import UserManager


class Chats(models.Model):

    CHATS_STATUS = [
        ('pub','public'),
        ('sec', 'private')
    ]

    title = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=128, null=True,blank=True,)
    status = models.CharField(max_length=20, choices=CHATS_STATUS)
    icon = models.ImageField(upload_to='chat/icon/chat/', default='chat/icon/chat/default.jpg')

    _password = None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):


        def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        password = make_password(self.password)
        super().save(**kwargs)

    class Meta:
        verbose_name = "Chats"
        verbose_name_plural = "Chats"




class Users_icons(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='chat/icon/users',default='chat/icon/users/default.jpg')


    def __str__(self):
        return self.user.__str__()


    class Meta:
        verbose_name = "User icon"
        verbose_name_plural = "Users icons"


class Messages(models.Model):

    message = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Chats_users(models.Model):

    USERS_STATUS = [
        ('A','Admin'),
        ('U','User')
    ]

    chat = models.ForeignKey(Chats, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=20, choices=USERS_STATUS)

    class Meta:
        verbose_name = "Chats users"
        verbose_name = "Chats user"


