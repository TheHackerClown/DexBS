import os

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import *
from .forms import *
from datetime import datetime


def guard(request):
    return render(request,'guard.html')

@csrf_exempt
def auth_receiver(request):
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
        data = {'email':user_data['email'],'picture':user_data['picture'],'name':user_data['name']}
    except ValueError:
        return HttpResponse(status=403)
    
    request.session['user_data'] = data
    userfind = User.objects.filter(email=data['email'])
    request.session['register'] = False if userfind else True
    return redirect('user_gate')

def user_gate(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            g_data = request.session['user_data']
            cover = form.cleaned_data['cover']
            desc = form.cleaned_data['desc']
            username = form.cleaned_data['username']
            propic = g_data['picture']
            name = g_data['name']
            email = g_data['email']
            User.objects.create(name=name,username=username,desc=desc,email=email,cover=cover,propic=propic,cake_day=datetime.now())
            request.session['register'] = False
            return render(request,'usergate.html')
    else:
        form = Register()
        return render(request,'usergate.html',{'form':form})

def index(request):
    try:
        request.session['user_data']
        email = request.session['user_data']['email']
        user = User.objects.get(email=email)
        try:
            dexs = Dex.objects.get(owner=user)
            dexs += Membership.objects.get(user=user)
        except:
            dexs = False
        posts = Post.objects.all()
        form = Search()
        return render(request,'index.html',{'user':user,'dexs':dexs,'posts':posts,'form':form})
    except:
        posts = Post.objects.all()
        dexs = Dex.objects.all()
        search = Search()
        return render(request, 'index.html',{'posts':posts,'dexs':dexs,'form':search})

def sign_out(request):
    del request.session['user_data']
    del request.session['register']
    return redirect('index')

def user_profile(request, username):
    form = Search()
    user = User.objects.get(username=username)
    return render(request,'user.html',{'user':user,'form':form})

def dex(request, dex):
    dex = Dex.objects.get(dex=dex)
    form= Search()
    return render(request,'dex.html',{'dex':dex,'form':form})

def create_dex(request):
    return render(request,'dexcreate.html')

def create_post(request):
    return render(request, 'postcreate.html')

def search(request):
    return render(request,'search.html')

