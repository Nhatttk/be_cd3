from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )

    def create(self, validated_data):
        group = Group.objects.get(name="user")
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.groups.set([group])
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
