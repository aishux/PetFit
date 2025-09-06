from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages

def handleLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = email.split("@")[0]
        user = authenticate(username=username, password=password)
        auth.login(request, user)
        
        if request.user.is_authenticated:
            messages.success(request, 'Logged in Successfully!')
            return HttpResponseRedirect(reverse("mainpage"))
        else:
            messages.error(request, 'Authentication Failed! Please check credentials')
    return render(request, "login.html")


def handleSignup(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = email.split("@")[0]
        fullname = fullname.split()

        user = User.objects.create_user(username=username, email=email, password=password)

        user.first_name = fullname[0]
        if len(fullname) > 1:
            user.last_name = fullname[1]

        messages.success(request, "Successfully Signed Up! Please login now")

    return HttpResponseRedirect(reverse("login"))


def handleLogout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, "Successfully Logged out!")
    return HttpResponseRedirect(reverse("mainpage"))


def mainpage(request):
    return render(request, "index.html")

def addPet(request):
    return render(request, "add-pet.html")

def chat(request):
    return render(request, "chat.html")

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html")
    else:
        return HttpResponseRedirect(reverse("login"))