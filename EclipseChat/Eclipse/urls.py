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
    path('lobby/setting/', views.lobby_setting),
] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
