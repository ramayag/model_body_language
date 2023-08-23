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

from loginlogout.connection_database import DataBase
from loginlogout.views import index
# from loginlogout.main import set_global
# from loginlogout.PoseDetector import *
import loginlogout.main
from django.urls import re_path
# from . import consumers
# from loginlogout.views import main
from loginlogout.main import main
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from loginlogout import views 
# import loginlogout.consumers


# websocket_urlpatterns = [
#     re_path(r'ws/continuous_processing/$', consumers.ContinuousProcessingConsumer.as_asgi()),
# ]

# application = ProtocolTypeRouter(
#     {
#         "websocket": AuthMiddlewareStack(
#             URLRouter(
#                websocket_urlpatterns
#             )
#         ),
#     }
# )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('loginlogout.urls')),
    # path('api/set-global/', set_global, name='set_global'),
    # path('api/runcode/', loginlogout.main.main, name='run'),
    path('api/get_videos/', DataBase.get_all_vedio_of_user , name='videos'),
    path('api/get_video_information/', DataBase.get_specific_video_and_evaluation , name='information'),
    path('api/show_evals/', loginlogout.main.show_eval, name='show'),
    path('api/runcode/soket/', loginlogout.main.run_with_soket, name='soket'),
    path('api/runcode/disoket/', loginlogout.main.di_with_soket, name='disoket'),
    path('api/runcode/', main , name='run'),
    path('api/send_image/', loginlogout.main.send_image, name='image'),
    # path('api/upload_image', loginlogout.main.send_image , name='send_image'),
    path('api/upload_image', views.upload_image_view, name='upload_image'),
    
    path('', index, name="index"),
]
