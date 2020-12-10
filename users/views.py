from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .forms import UserLoginForm, UserRegisterForm
from .models import UserToken, User

from tasks.views import list_all_user_tasks, get_all_tasks_count

# Create your views here.
def login_render(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))

    return render(request, "users/login.html", {
        "user_login_form" : UserLoginForm()
    })


def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():

            name = request.POST['name']
            password = request.POST['password']

            user = authenticate(request, username=name, password=password)

            if user:
                login(request, user)

                token = UserToken.objects.get(user=user)
                request.session['token'] = str(token.token)

                return HttpResponseRedirect(reverse('dashboard'))

            else:
                return render(request, "users/login.html", {
                    "status" : False, "user_login_form" : form })
        else:
            return render(request, "users/login.html", {
                "status" : None, "user_login_form" : UserLoginForm() })


def logout_user(request):
    request.session['token'] = None
    logout(request)
    return render(request, "users/login.html", {
        "user_login_form" : UserLoginForm()
    })

def register_render(request):
    return render(request, "users/register.html", {
        "user_register_form" : UserRegisterForm(), "status" : None })

def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'])
            user.save()

            user = User.objects.last()
            token = UserToken.objects.create(user=user)
            token.save()

            return render(request, "users/register.html", {
                "user_register_form" : UserRegisterForm(), "status" : True })

        else:
            return render(request, "users/register.html", {
                "user_register_form" : form, "status" : False })
    else:
        return render(request, "users/register.html", { "user_register_form" : UserRegisterForm(), "status" : None })

def dashboard_user(request):
    if not request.user.is_authenticated or request.session['token'] == None:
        return redirect(reverse("login"))

    counts = get_all_tasks_count(request)

    return render(request, "users/dashboard.html", {
        "user_login_form" : UserLoginForm(),
        "user_tasks" : list_all_user_tasks(request),
        "tasks_done" : counts['done'],
        "tasks_pending" : counts['pending'],
        "all_tasks" : counts['all'] 
    })

def user_error_not_found(request):
    return render(request, "error404.html")