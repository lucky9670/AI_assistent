from rest_framework import serializers
from django.contrib.auth.models import Group
from rest_apis.models import User

class RegisterSerialization(serializers.Serializer):
    phone = serializers.CharField(required = True)
    password = serializers.CharField(required = True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required = True)
    gender = serializers.CharField(required = False)
    age = serializers.CharField(required = False)
    address = serializers.CharField(required = False)
    prefrence = serializers.JSONField(required=False)

class LoginSerialization(serializers.Serializer):
    email = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

class LogOutSerializer(serializers.Serializer):
    pass

class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=False)
    gender = serializers.CharField(required=True)
    age = serializers.CharField(required=True)
    address = serializers.CharField(required = False)
    prefrence = serializers.JSONField(required=False)

class UpdateProfileImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)

class UserSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username', 'email', 'phone', 'gender', 'age', 'image', "prefrence"]
