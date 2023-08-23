from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import User
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer

# import motion
import math
import cv2
import mediapipe as mp
import numpy as np
from experta import *
from enum import Enum
# import mysql.connector
# import pymssql
from sqlalchemy import create_engine
from .connection_database import DataBase
import time
import os
from django.http import JsonResponse
import base64
# from flask import Flask, request, jsonify, render_template, Response
# from flask_cors import CORS, cross_origin
# from flask_socketio import SocketIO, emit
from django.views.decorators.csrf import csrf_exempt
import time
import plotly.graph_objects as go
from PIL import Image
from tkinter import Tk, Label, Canvas, NW
from PIL import ImageTk

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# from .views import store 




class Record(generics.ListCreateAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(generics.GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)

        if serializer_class.is_valid(raise_exception=True):
            # request.session['user_id'] = serializer_class.validated_data['user_id']
            try:
                user = User.objects.get(username=serializer_class.validated_data['user_id'])
            except User.DoesNotExist:
                return Response({"detail": "User not found"}, status=HTTP_400_BAD_REQUEST)

            # Save the user's ID in the session
            request.session['user_id'] = user.id
            request.session.save()
            print ( request.session['user_id'])
            return Response(serializer_class.data, status=HTTP_200_OK)
            
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)



@csrf_exempt
def upload_image_view(request):
    if request.method == 'POST':
        # Process the uploaded image and any data here
        # You can access the uploaded image using request.FILES['image']
        
        # Example: Save the uploaded image to a model or file system
        uploaded_image = request.FILES['image']
        # Save or process the image here
        
        # Read the image data and encode as base64
        image_data = uploaded_image.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Construct the API response
        api_response = {
            "message": "Image uploaded successfully.",
            "image_data": base64_image
        }
        
        return JsonResponse(api_response)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
def index(request):
    return redirect('/api/login')

