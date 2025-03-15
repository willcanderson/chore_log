from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Chore_Definition, Work, Play

admin.site.register(User, UserAdmin)
admin.site.register(Chore_Definition)
admin.site.register(Work)
admin.site.register(Play)
