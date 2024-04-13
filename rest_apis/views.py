from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, viewsets
from knox.models import AuthToken
from .models import User, Activity
from drf_yasg.utils import swagger_auto_schema
from .serialization import *
from knox.auth import TokenAuthentication
from rest_framework.parsers import MultiPartParser
from django.db.models import Q
from rest_apis.serial.activity_serial import ActivitySerializer
from django.shortcuts import render

def password_check(passwd):
    flag = 0
    import re
    if not re.search("[A-Z]", passwd):
        flag = 1
    if not re.search("[0-9]", passwd):
        flag = 2
    if not re.search("[@$!%*#?&]", passwd):
        flag = 3
    return flag

def index(request):
    return render(request, 'index.html')

class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerialization

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        password = request.data.get('password')
        email = request.data.get('email')
        gender = request.data.get('gender')
        age = request.data.get('age')
        address = request.data.get('address')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        try:
            user = User.objects.get(email=email)
            if user:
                return Response({'message': "User Already exist with this phone! please login"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # If user does not exist, create a new user
            checkpoint = password_check(password)
            if checkpoint == 1:
                return Response({'response': 'Password must contain atleast one capital alphbat'}, status=status.HTTP_400_BAD_REQUEST)
            if checkpoint == 2:
                return Response({'response': 'Password must contain atleast one digit'}, status=status.HTTP_400_BAD_REQUEST)
            if checkpoint == 3:
                return Response({'response': 'Password must contains one special character like @, $,#,&'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=email, email=email, phone=phone, password=password, first_name=first_name, last_name=last_name, gender=gender, age=age, address=address)
            return Response(UserSerial(user).data, status=status.HTTP_201_CREATED)

class LoginAPI(GenericAPIView):
    serializer_class = LoginSerialization

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': "User does not exist!"})
        if user.check_password(password):
            token = AuthToken.objects.create(user)[1]
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'gender': user.gender,
                'age': user.age,
                'email': user.email
            }
            result = {
                'token': token,
                **user_data
            }
            return Response({'message': 'You have signin successfully!', 'data': result}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalide Phone or Password!"}, status=status.HTTP_400_BAD_REQUEST)


class LogOutAPI(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = LogOutSerializer

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request, *args, **kwargs):
        AuthToken.objects.filter(user=request.user).delete()
        return Response({"message": "Logout Successfully!"})

class UpdateProfile(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerial

    @swagger_auto_schema(tags=['Authentication'], request_body=UpdateProfileSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UpdateProfileSerializer(data = request.data)
        if serializer.is_valid():
            user = request.user
            data = request.data
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.phone = data.get('phone')
            user.age = data.get('age')
            user.gender = data.get('gender')
            user.prefrence = data.get('prefrence')
            user.save()
            return Response(UserSerial(request.user).data)
        else:
            return Response({'message':"Invalid data!"})

class UpdateProfileImage(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(tags=['Authentication'], request_body=UpdateProfileImageSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UpdateProfileImageSerializer(data = request.data)
        if serializer.is_valid():
            user = request.user
            data = request.data
            if data.get('image'):
                user.image = data.get('image')
            else:
                user.image = None
            user.save()
            return Response(UserSerial(request.user).data)
        else:
            return Response({'message':"Invalid data!"})

class RecomendationView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(tags=['Recommendation'])
    def list(self, request, *args, **kwargs):
        user = request.user
        filter_query = Q()
        preferences = user.prefrence
        print(preferences)
        for preference in preferences:
            filter_query |= Q(name__icontains=preference)
        print(filter_query)
        activity = Activity.objects.filter(filter_query)
        print(activity)
        serializer = ActivitySerializer(activity, many=True)  # Pass many=True to serialize a queryset
        return Response(serializer.data, status=status.HTTP_200_OK)

class ScheduleTaskView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ScheduleTaskSerial

    
    def get_queryset(self):
        return ScheduleTask.objects.all()


class GetUsersAssignTask(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(tags=['Get User Schedule Task'])
    def list(self, request, *args, **kwargs):
        day = request.GET.get('day')
        user = request.user
        if day:
            user_schedule_task = ScheduleTask.objects.filter(user=user, is_completed = False, schedule_day=day)
            serializer = ScheduleTaskSerial(user_schedule_task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        user_schedule_task = ScheduleTask.objects.filter(user=user, is_completed = False)
        serializer = ScheduleTaskSerial(user_schedule_task, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.decorators import action
from django.http import JsonResponse
import json
from django.core import serializers
@action(methods=['POST'], detail=False)
def executeTask(request, id):
    task = ScheduleTask.objects.get(id = id)
    if not task.is_completed:
        task.is_completed = True
        task.save()

        data = {
            "schedule_day": task.schedule_day,
            "is_completed": task.is_completed,
            "task": task.task.id,
            "user": task.user.id
        }
        return JsonResponse(data)
    return JsonResponse({"message": "Task completed already"})
