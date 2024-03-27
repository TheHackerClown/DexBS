import os
from django.shortcuts import render, redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import *
from .forms import *
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


@csrf_exempt
def auth_receiver(request):
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ.get('GOOGLE_CLIENT_ID')
        )
    except ValueError:
        return HttpResponse(content='Google OAuth Error, Dhruv se baat karle')
    
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

def filetourl(path):
    import requests
    import base64
    import os
    USERNAME = 'TheHackerClown'
    REPO_NAME = 'DexBS_Asset_Library'
    ACCESS_TOKEN = os.environ.get('GITHUB_PAT')
    FILE_PATH = path
    FILE_NAME = os.path.basename(FILE_PATH)
    if FILE_NAME[-3::1] in ['ico','webp','gif','jpeg','png','jpg']:
        file_type = 'image'
    else:
        file_type = 'file'
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    with open(FILE_PATH,'rb') as file:
        content = file.read()
    # Prepare request payload with new file content
    payload = {
        'message': 'Create new file',
        'content': base64.b64encode(content).decode(),
    }

    # Make PUT request to create file
    response = requests.put(
        f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{FILE_NAME}',
        headers=headers,
        json=payload
    )

    # Check if the creation was successful
    if True:
        file_info = response.json()
        file_name = FILE_NAME.replace(' ','%20')
        file_url = 'https://thehackerclown.github.io/DexBS_Asset_Library/' + file_name    
        return file_url
    else:
        print(f'Error creating file: {response.text}')

def del_git_file(path):
    import requests
    USERNAME = 'TheHackerClown'
    REPO_NAME = 'DexBS_Asset_Library'
    ACCESS_TOKEN = os.environ.get('GITHUB_PAT')
    path = (path.split('?'))[0]
    path = path.replace('%20',' ')
    FILE_GITHUB_PATH = (path.split('/'))[-1]
    headers = {
        'Authorization': f'token {ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(
        f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{FILE_GITHUB_PATH}',
        headers=headers
    )

    # Check if the file exists
    if response.status_code == 200:
        # Extract the SHA hash of the file
        file_sha = response.json()['sha']

        # Prepare request payload
        payload = {
            'message': f'Delete {FILE_GITHUB_PATH}',
            'sha': file_sha,
        }

        # Make DELETE request to delete file
        response = requests.delete(
            f'https://api.github.com/repos/{USERNAME}/{REPO_NAME}/contents/{FILE_GITHUB_PATH}',
            headers=headers,
            json=payload
        )

        # Check if the deletion was successful
        if response.status_code == 200:
            return "Done"
        else:
            return 'Not Done'
    else:
        return 'Not Done'

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
        form = Create_Dex(request.POST, request.FILES)
        if form.is_valid():
            g_data = request.session['user_data']
            user = User.objects.get(email=g_data['email'])
            dex = form.cleaned_data['dex']
            name = form.cleaned_data['name']
            desc = form.cleaned_data['desc']
            rules = form.cleaned_data['rules']
            cover = form.cleaned_data['cover']
            #rules = list(rules.split('\r\n'))
            uploaded_file = request.FILES['propic']
            file_path = BASE_DIR / f'static/{uploaded_file.name}'
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            url = filetourl(file_path)
            inst = Dex.objects.create(name=name,desc=desc,dex=dex,rules=rules,propic=url,cover=cover,cake_day=datetime.now(),owner=user)
            inst.save()
            another_inst = Membership.objects.create(user=user,dex=Dex.objects.get(dex=dex))
            another_inst.save()
            os.remove(file_path)
            return redirect('dex', dex=dex)
            
            
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
                dexs = []
                membership = Membership.objects.filter(user=user)
                for i in membership:
                    dexs.append(i.dex)
                #form
                return render(request,'dexcreate.html',{'user_data':user,'dex_form':dex,'dexs':dexs})
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
        form = Create_Post(request.POST,request.FILES)
        if form.is_valid():
            g_data = request.session['user_data']
            user = User.objects.get(email=g_data['email'])
            dex = Dex.objects.get(dex=dex)
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                file_path = BASE_DIR / f'static/{uploaded_file.name}'
                print(file_path)
                with open(file_path, 'wb') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                url = filetourl(file_path)
                file_type = (uploaded_file.name)[-3::1]
                if file_type in ['ico','png','gif','jpeg','jpg']:
                    file_type = 'image'
                elif file_type =='mp4':
                    file_type = 'video'
                elif file_type == 'mp3':
                    file_type = 'music'
                os.remove(file_path)
            else:
                url = None
                file_type = 'text'
            inst = Post.objects.create(owner=user,dex=dex,title=title,desc=desc,cake_day=datetime.now(),file=url,type=file_type)
            inst.save()
            return redirect('dex',dex=dex.dex)
    else:
        if 'user_data' in request.session and rfid!='create':
            g_data = request.session['user_data']
            user = User.objects.filter(email=g_data['email'])
            if len(user)<2 and len(user)>0:
                dex = Dex.objects.get(dex=dex)
                post = Post.objects.get(rfid=int(rfid))
                user = User.objects.get(email=g_data['email'])
                comment = Create_Comment()
                comments = Comment.objects.all()
                comments = list(reversed(comments))   
                modship = Mod.objects.filter(dex=dex)
                moderators = []
                for i in modship:
                    moderators.append(i.user)
                return render(request,'post.html',{'user_data':user,'dex':dex,'post':post,'comment_form':comment,'comments':comments,'moderators':moderators})
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
    if post.file != None:
        del_git_file(post.file)
        post.delete()
    else:
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
    inst = del_git_file(dex_obj.propic)
    dex_obj.delete()
    return redirect('index')
def comment(request,dex,rfid):
    if request.method == 'POST':
        form = Create_Comment(request.POST)
        if form.is_valid():
            desc = form.cleaned_data['comment']
            post = Post.objects.get(rfid=rfid)
            dex = Dex.objects.get(dex=dex)
            g_data = request.session['user_data']
            user = User.objects.get(email=g_data['email'])
            inst = Comment.objects.create(owner=user,content=desc,cake_day=datetime.now(),post=post,dex=dex,upvote=0,downvote=0)
            inst.save()
    return redirect('post',dex=dex.dex,rfid=rfid)

def del_comment(request,dex,rfid,comment_id):
    inst = Comment.objects.get(rfid=comment_id)
    inst.delete()
    return redirect('post',dex=dex,rfid=rfid)
    