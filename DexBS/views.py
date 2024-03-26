import os
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import *
from .forms import *
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

@csrf_exempt
def auth_receiver(request):
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return render(request,'error.html',{'code':909,'desc':'Bhai Error aagya, dhruv se baat karle, kehde ki google oauth verification error hai','redirect':'/u/create','btn_label':'Return To Login'})
    
    request.session['user_data'] = user_data
    userfind = User.objects.filter(email=user_data['email'])
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
            inst = User.objects.create(name=name,username=username,desc=desc,email=email,cover=cover,propic=propic,cake_day=datetime.now())
            inst.save()
            request.session['register'] = False
            return render(request,'usergate.html')
    else:
        form = Register()
        return render(request,'usergate.html',{'form':form})

def index(request):
    if 'user_data' in request.session:

        g_data = request.session['user_data']
        user = User.objects.filter(email=g_data['email'])
        if len(user)<2 and len(user)>0:
            membership = Membership.objects.filter(user=user[0])
            dexs_filtered =[]
            for i in membership:
                dexs_filtered.append(i.dex)
            posts = Post.objects.all()
            posts = list(reversed(posts))
            user = User.objects.get(email=g_data['email'])
            #form
            return render(request,'index.html',{'user_data':user,'dexs':dexs_filtered,'posts':posts})
        else:
            return redirect('user',username='create')
    else:
        return redirect('user',username='create')

def sign_out(request):
    del request.session['user_data']
    try:
        del request.session['register']
    except:
        return redirect('user',username='create')
    return redirect('user',username='create')

def user(request, username):
    if username=='create' or not User.objects.filter(username=username) and not request.session['user_data']:
        return render(request,'usercreate.html')
    else:
        #form
        user = User.objects.get(username=username)
        posts = Post.objects.filter(owner=user)
        membership = Membership.objects.filter(user=user)
        dexs = []
        for i in membership:
            dexs.append(i.dex)
        return render(request,'user.html',{'user_data':user,'dexs':dexs,'posts':posts})

def dex(request, dex):
    if request.method == 'POST':
        form = Create_Dex(request.POST)
        if form.is_valid():
            #this creates a dex sub for user
            print()
    else:
        if 'user_data' in request.session and dex!='create':
            g_data = request.session['user_data']
            user = User.objects.filter(email=g_data['email'])
            if len(user)<2 and len(user)>0:
                user = User.objects.get(email=g_data['email'])
                dex = Dex.objects.get(dex=dex)
                memberships = Membership.objects.filter(dex=dex)
                members = []
                for i in memberships:
                    members.append(i.user)
                posts = Post.objects.filter(dex=dex)
                posts = list(reversed(posts))
                modship = Mod.objects.filter(dex=dex)
                moderators = []
                for i in modship:
                    moderators.append(i.user)
                return render(request,'dex.html',{'user_data':user,'dex':dex,'posts':posts,'total_user':len(members)-1,'total_post':len(posts),'members':members,'moderators':moderators})
            else:
                return redirect('user',username='create')
        elif dex=='create' and 'user_data' in request.session:
            g_data = request.session['user_data']
            user = User.objects.filter(email=g_data['email'])
            if len(user)<2 and len(user)>0:
                dex = Create_Dex()
                user = User.objects.get(email=g_data['email'])
                #form
                return render(request,'dexcreate.html',{'user_data':user,'dex_form':dex})
            else:
                return redirect('user',username='create')
        else:
            return redirect('user',username='create')

def search(request, what):
    if what == 'd':
        dex = Dex.objects.all()
        return render(request,'search.html',{'items':dex})
    elif what == 'u':
        user = User.objects.all()
        return render(request, 'search.html',{'items':user})
    elif what == 'post':
        post = Post.objects.all()
        return render(request,'search.html',{'items':post})
    else:
        post = Post.objects.all()
        user = User.objects.all()
        dex = Dex.objects.all()
        data = []
        for i in post:
            data.append(i)
        for i in user:
            data.append(i)
        for i in dex:
            data.append(i)
        return render(request,'search.html',{'items':data})


def post(request, dex, rfid):
    if request.method == 'POST':
        form = Create_Post(request.POST)
        if form.is_valid():
            #this func creates a post
            print()
            return redirect('dex',dex=dex)
    else:
        if 'user_data' in request.session and rfid!='create':
            g_data = request.session['user_data']
            user = User.objects.filter(email=g_data['email'])
            if len(user)<2 and len(user)>0:
                dex = Dex.objects.get(dex=dex)
                post = Post.objects.get(rfid=int(rfid))
                user = User.objects.get(email=g_data['email'])
                #form
                return render(request,'post.html',{'user_data':user,'dex':dex,'post':post,})
            else:
                return redirect('user',username='create')
        elif rfid=='create' and 'user_data' in request.session:
            g_data = request.session['user_data']
            user = User.objects.filter(email=g_data['email'])
            if len(user)<2 and len(user)>0:
                post_form = Create_Post()
                dex = Dex.objects.get(dex=dex)
                user = User.objects.get(email=g_data['email'])
                #form
                return render(request,'postcreate.html',{'user_data':user,'dex':dex,'post_form':post_form})
            else:
                return redirect('user',username='create')
        else:
            return redirect('user',username='create')
        
def del_post(request,dex,rfid):
    post = Post.objects.get(rfid=rfid)
    post.delete()
    return redirect('dex',dex=dex)

def follow(request, dex, rfid):
    dex_obj = Dex.objects.get(dex=dex)
    user_obj = User.objects.get(rfid=rfid)
    inst = Membership.objects.create(user=user_obj,dex=dex_obj)
    inst.save()
    return_url = request.GET.get('return_url')
    return redirect(return_url)

def unfollow(request, dex, rfid):
    dex_obj = Dex.objects.get(dex=dex)
    user_obj = User.objects.get(rfid=rfid)
    inst = Membership.objects.get(user=user_obj,dex=dex_obj)
    inst.delete()
    return_url = request.GET.get('return_url')
    return redirect(return_url)

def mod_maker(request,dex, rfid):
    dex_obj = Dex.objects.get(dex=dex)
    user_obj = User.objects.get(rfid=rfid)
    inst = Mod.objects.create(dex=dex_obj,user=user_obj)
    inst.save()
    return redirect('dex',dex=dex)

def mod_remover(request,dex,rfid):
    dex_obj = Dex.objects.get(dex=dex)
    user_obj = User.objects.get(rfid=rfid)
    inst = Mod.objects.get(user=user_obj,dex=dex_obj)
    inst.delete()
    return redirect('dex',dex=dex)

def upvote(request,dex,post_id,rfid):
    post = Post.objects.get(rfid=post_id)
    user_obj = User.objects.get(rfid=rfid)
    like = Vote.objects.filter(post=post,user=user_obj)
    if len(like)>0:
        if like.type == 'upvote':
            post.upvote -= 1
            post.save()
            like.delete()
    else:
        post.upvote += 1
        post.save()
        like = Vote.objects.create(user=user_obj,post=post,type='upvote')
        like.save()
    return_url = request.GET.get('return_url')
    return redirect(return_url)

def downvote(request,dex,post_id,rfid):
    post = Post.objects.get(rfid=post_id)
    user_obj = User.objects.get(rfid=rfid)
    like = Vote.objects.filter(post=post,user=user_obj)
    if len(like)>0:
        if like.type == 'downvote':
            post.downvote -= 1
            post.save()
            like.delete()
    else:
        post.downvote += 1
        post.save()
        like = Vote.objects.create(user=user_obj,post=post,type='downvote')
        like.save()
    return_url = request.GET.get('return_url')
    return redirect(return_url)

def del_dex(request, dex):
    dex_obj = Dex.objects.get(dex=dex)
    dex_obj.delete()
    return redirect('index')
    