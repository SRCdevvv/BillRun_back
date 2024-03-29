"""BillRun_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from api.views import *
from django.conf.urls import url, static
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from .admin import admin_site

admin.autodiscover()

urlpatterns = [
    path('', main, name="main"),
    # path('admin/', admin.site.urls, name="admin"),
    path('admin/', admin_site.urls),
    path('api/', include('api.urls')),

    #jwt
    path('token/', obtain_jwt_token), #획득
    path('token/verify/', verify_jwt_token), #확인
    path('token/refresh/', refresh_jwt_token), #갱신

] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)