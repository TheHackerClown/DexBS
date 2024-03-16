import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import *
from .forms import *
from datetime import datetime


def main(request):
    return render(request,'main.html')

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)
    
    request.session['user_data'] = user_data
    return redirect('user_gate')

def feed(request):
    if request.session['signin']:
        if request.method == "POST":
            form = SignIn(request.POST)
            if form.is_valid():
                g_data = request.session['user_data']
                cover = form.cleaned_data['cover']
                desc = form.cleaned_data['desc']
                username = form.cleaned_data['username']
                propic = g_data['picture']
                name = g_data['name']
                email = g_data['email']
                User.objects.create(name=name,username=username,desc=desc,email=email,cover=cover,propic=propic,cake_day=datetime.now())
                del request.session['signin']
                return render(request,'feed.html',{'user':'hehe'})
    else:
        del request.session['signin']
        return render(request,'feed.html',{'user':'mar dala'})

def user_gate(request):
    g_data = request.session['user_data']
    userfind = User.objects.filter(email=g_data['email'])
    if userfind:
        request.session['signin'] = False
        return render(request,'usergate.html')
    else:
        form = SignIn()
        request.session['signin'] = True
        return render(request,'usergate.html',{'form':form})

def sign_out(request):
    del request.session['user_data']
    return redirect('main')
