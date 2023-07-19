"""projectapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from loginlogout.views import index
# from loginlogout.main import set_global
# from loginlogout.PoseDetector import *
import loginlogout.main


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('loginlogout.urls')),
    # path('api/set-global/', set_global, name='set_global'),
    path('api/runcode/', loginlogout.main.main, name='run'),

    path('', index, name="index"),
]
