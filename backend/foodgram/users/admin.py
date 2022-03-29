from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'password')
    search_fields = ('username',)
    list_filter = ('first_name', 'email',)
    # list_editable = ('password',)
    empty_value_display = '-empty-'


admin.site.register(User, UserAdmin)
