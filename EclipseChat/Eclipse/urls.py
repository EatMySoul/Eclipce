from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index ,name='index'),
    path('user/registration/',views.registration_page , name='registration_page'),
    path('reguser/', views.registrate_user, name='reguser'),
    path('user/', include('django.contrib.auth.urls') , name='django_auth'),
    path('lobby/', views.lobby, name="lobby"),
    path('lobby/<str:chat_title>/', views.lobby, name='chat'),
    path('lobby/<str:chat_title>/setting/', views.chat_setting),
    path('search/' , views.join_chat),
    path('create/', views.create_chat),
    path('remove/<str:chat_title>/',views.remove_chat),
    path('remove_chat_user/<str:chat_title>/<str:username>/', views.remove_chat_user)
 #   path('<str:room_name>/', views.room, name='room'),
] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
