from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register-parent/', views.register_parent, name='register-parent'),
    path('register-child/', views.register_child, name='register-child'),
    path('log/<str:username>', views.full_log, name='full-log'),
    path('submit_work', views.log_chore, name='log_chore'),
    path('submit_play', views.log_play, name='log_play'),
    path('define_chore', views.define_chore, name='define_chore'),
]