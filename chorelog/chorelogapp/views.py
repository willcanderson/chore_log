from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Chore_Definition, Work, Play
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Value, F, Sum
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.forms import ModelForm

# Create your views here.

class LogWorkForm(ModelForm):
    class Meta:
        model = Work
        fields = ['chore']

    def __init__(self, *args, **kwargs):
        super(LogWorkForm, self).__init__(*args, **kwargs)
        self.fields['chore'].queryset = self.fields['chore'].queryset.order_by('name')

class LogPlayForm(ModelForm):
    class Meta:
        model = Play
        fields = ['game', 'minutes_played']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["game"].widget.attrs.update({"list": "game-titles"})

class DefineChoreForm(ModelForm):
    class Meta:
        model = Chore_Definition
        fields = ['name', 'minute_value']

def get_log_and_balance(user, log_limit=None):
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
    log_items = work.union(play).order_by("-date_logged")[:log_limit]
    # If no work or play has been logged yet, assign 0 value
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
            chores = request.user.defined_chores.all().order_by('name')

            return render(request, "index-for-parents.html", {
                'child_list': child_list,
                "chores": chores,
                "define_chore_form": DefineChoreForm(),
        })

        if request.user.user_type == 'CHILD':
            log_items, balance = get_log_and_balance(request.user, 10)
            return render(request, "index-for-children.html", {
                "log_items": log_items,
                "balance": balance,
                "log_work_form": LogWorkForm(),
                "log_play_form": LogPlayForm(),
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

def full_log(request, username):
    log_user = User.objects.get(username=username)

    # Children can only see their own logs. Parents can see their children's logs.
    if request.user != log_user and request.user != log_user.parent:
        messages.error(request, "Access not permitted")
        return redirect(reverse('index'))
    
    # Parents don't log anything, so it doesn't make any sense to try to view the log of a parent
    if log_user.user_type == 'PARENT':
        messages.info(request, "Parents do not have hours logs.")
        return redirect(reverse('index'))
           
    log_username = log_user.username
    log_items, balance = get_log_and_balance(log_user)

    paginator = Paginator(log_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "full-log.html", {
        "page_obj": page_obj,
        "balance": balance,
        "username": log_username
    })

def log_chore(request):
    if request.method == 'POST':
        form = LogWorkForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Invalid")
            return redirect(reverse('index'))
        
        chore = form.cleaned_data["chore"]
        entry = Work(chore=chore, done_by=request.user)
        entry.save()

    return redirect(reverse('index'))

def log_play(request):
    if request.method == 'POST':
        form = LogPlayForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Invalid")
            return redirect(reverse('index'))
        
        game = form.cleaned_data["game"]
        minutes_played = form.cleaned_data["minutes_played"]
        entry = Play(game=game, minutes_played=minutes_played, child=request.user)
        entry.save()

    return redirect(reverse('index'))

def define_chore(request):
    if request.method == 'POST':
        form = DefineChoreForm(request.POST)

        if not form.is_valid():
            messages.error(request, "Invalid")
            return redirect(reverse('index'))
        
        name = form.cleaned_data["name"]
        minute_value = form.cleaned_data["minute_value"]
        entry = Chore_Definition(name=name, minute_value=minute_value, defined_by=request.user)
        entry.save()

    return redirect(reverse('index'))