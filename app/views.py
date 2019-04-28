from django.shortcuts import render
from app.models import AppFbUser
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def index(request):
    context_dict = {}
    if request.user.is_active:
        app_user = AppFbUser.objects.get(user=request.user)
        context_dict["app_user"] = app_user
    return render(request, 'index.html', context_dict)


def user_login(request):
    if request.user.is_active:
        return HttpResponseRedirect('/app/')
    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/app/')
