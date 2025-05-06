from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Chore_Definition, Work, Play
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Value, F, Sum
from django.db import IntegrityError

# Create your views here.

def get_log_and_balance(user):
    work = user.work_done.all().annotate(
        log_name=F('chore__name'),
        type=Value("work"),
        time_value=F('chore__minute_value')
        ).values('log_name', 'date_logged', 'type', 'time_value')
    play = user.play_done.all().annotate(
        log_name=F('game'),
        type=Value("play"),
        time_value=F('minutes_played')
        ).values('log_name', 'date_logged', 'type', 'time_value')
    log_items = work.union(play).order_by("-date_logged")
    work_balance = work.aggregate(Sum('time_value'))['time_value__sum'] or 0
    play_balance = play.aggregate(Sum('time_value'))['time_value__sum'] or 0
    balance = work_balance - play_balance
    return log_items, balance


def index(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'PARENT':
            children = request.user.children.all()
            child_list = []
            for child in children:
                log_items, balance = get_log_and_balance(child)
                child = {
                    'username': child.username,
                    'balance': balance
                }
                child_list.append(child)
            chores = request.user.defined_chores.all()

            return render(request, "index-for-parents.html", {
                'child_list': child_list,
                "chores": chores,
        })

        if request.user.user_type == 'CHILD':
            log_items, balance = get_log_and_balance(request.user)
            return render(request, "index-for-children.html", {
                "log_items": log_items,
                "balance": balance
        })

    return render(request, "start.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse("index"))
        else:
            # https://docs.djangoproject.com/en/5.2/ref/contrib/messages/#adding-a-message
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")

    return render(request, "login.html")

def register_parent(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            messages.error(request, "Passwords do not match")
            return render (request, "register-parent.html")
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, user_type='PARENT')
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken")
            return render (request, "register-parent.html")
        
        login(request, user)
        return redirect(reverse('index'))
    else:
        return render(request, "register-parent.html")

def register_child(request):
    if request.method == "POST":
        username = request.POST["username"]
        parent_email = request.POST["parent-email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            messages.error(request, "Passwords do not match")
            return render (request, "register-child.html")
        
        # Check for parent
        try:
            parent = User.objects.get(email=parent_email)
        except:
            messages.error(request, "Parent not found")
            return render(request, "register-child.html")
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email=None, password=password, user_type='CHILD', parent=parent)
            user.save()
        except IntegrityError:
            messages.error(request, "Username already taken")
            return render (request, "register-child.html")
        
        login(request, user)
        return redirect(reverse('index'))
    else:
        return render(request, "register-child.html")
    #TODO: Maybe parent should get a request that they have to accept.

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

def full_log(request):
    pass
    #TODO: View full log of credits and debits. Children can see their own. Parents can see their children's.

def log_chore(request):
    pass

def log_play(request):
    pass

def define_chore(request):
    pass