from django.contrib import admin
from .models import Chats, Users_icons, Chats_users, Messages

class UsersIconsAdmin(admin.ModelAdmin):
    list_display = ('user','icon')

class ChatsAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'icon')


admin.site.register(Chats, ChatsAdmin)
admin.site.register(Users_icons, UsersIconsAdmin)
admin.site.register(Chats_users)
admin.site.register(Messages)
