from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Parent, Child

admin.site.register(User, UserAdmin)
admin.site.register(Parent)
admin.site.register(Child)
