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
    path('sign-in', sign_in, name='sign_in'),
    path('sign-up',sign_up, name='sign_up'),
    path('sign-out', sign_out, name='sign_out'),
    path('auth-receiver', auth_receiver, name='auth_receiver')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

