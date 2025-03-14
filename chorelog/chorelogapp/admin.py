from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Parent, Child, Chore_Definition, Work, Play

admin.site.register(User, UserAdmin)
admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(Chore_Definition)
admin.site.register(Work)
admin.site.register(Play)