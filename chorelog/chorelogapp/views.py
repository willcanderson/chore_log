from django.shortcuts import render
from .models import User, Chore_Definition, Work, Play

# Create your views here.

def index(request):
    if request.user.user_type == 'PARENT':
        children = request.user.children.all()
        chores = request.user.defined_chores.all()

        return render(request, "index-for-parents.html", {
            'children': children,
            "chores": chores,
    })

    if request.user.user_type == 'CHILD':
        work = request.user.work_done.all()
        play = request.user.play_done.all()

        return render(request, "index-for-children.html", {
            'work': work,
            "play": play,
    })

    return render(request, "start.html")

def login(request):
    pass
    #TODO: Investigate Django's provided log-in form

def register_parent(request):
    pass
    #TODO: Email address, username, password
    # https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms

def register_child(request):
    pass
    #TODO: parent's email address, username, password. Error message if parent's email is not found.
    # Maybe parent should get a request that they have to accept.

def logout(request):
    pass

def full_log(request):
    pass
    #TODO: View full log of credits and debits. Children can see their own. Parents can see their children's.

def log_chore(request):
    pass

def log_play(request):
    pass

def define_chore(request):
    pass