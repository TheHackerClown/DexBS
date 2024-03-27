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
    path('d/<str:dex>/post/<str:rfid>/comment',comment,name='comment'),
    path('d/<str:dex>/post/<str:rfid>/comment/delete/<str:comment_id>',del_comment,name='comment_delete'),
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

