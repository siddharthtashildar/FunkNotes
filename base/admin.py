from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import NoteDatabase, User

class AccountAdmin(UserAdmin):
    list_display=('email', 'username' , 'user_uuid' ,'date_joined','last_login','is_admin', 'is_staff')
    search_fields=('email','username')
    readonly_fields=('user_uuid','date_joined','last_login')

    filter_horizontal=()
    list_filter=()
    fieldsets=()


admin.site.register(NoteDatabase)
admin.site.register(User,AccountAdmin)
