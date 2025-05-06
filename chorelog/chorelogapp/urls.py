from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register-parent/', views.register_parent, name='register-parent'),
    path('register-child/', views.register_child, name='register-child'),
    path('log/<str:username>', views.full_log, name='full-log'),
]