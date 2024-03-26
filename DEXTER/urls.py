"""
URL configuration for DEXTER project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from DexBS.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('auth-receiver', auth_receiver, name='auth_receiver'),
    path('user-gate',user_gate,name='user_gate'),
    path('u/<str:username>',user,name='user'),
    path('d/<str:dex>',dex, name='dex'),
    path('d/<str:dex>/delete',del_dex),
    path('d/<str:dex>/post/<str:rfid>',post,name='post'),
    path('search/<str:what>',search,name='search'),
    path('d/<str:dex>/post/delete/<int:rfid>',del_post),
    path('d/<str:dex>/post/<int:post_id>/upvote/<int:rfid>',upvote),
    path('d/<str:dex>/post/<int:post_id>/downvote/<int:rfid>',downvote),
    path('d/<str:dex>/follow/<int:rfid>', follow),
    path('d/<str:dex>/unfollow/<int:rfid>', unfollow),
    path('d/<str:dex>/mod/create/<int:rfid>',mod_maker),
    path('d/<str:dex>/mod/delete/<int:rfid>',mod_remover),
    path('search',search,{'what':''}, name='search_empty'),
    path('exit',sign_out,name='exit')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

