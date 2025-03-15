from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Chore_Definition, Work, Play

class MyUserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ["user_type","parent"]}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ["user_type","parent"]}),)

admin.site.register(User, MyUserAdmin)
admin.site.register(Chore_Definition)
admin.site.register(Work)
admin.site.register(Play)
