from backend.foodgram.users.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username')
    search_fields = ('username',)
    list_filter = ('first_name', 'email',)
    empty_value_display = '-empty-'


admin.site.register(User, UserAdmin)
