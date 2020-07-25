from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.crypto import get_random_string

from .models import UserProfile, Room, Exam


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'username']
        extra_kwargs = {
            "password": {"write_only": True}
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'token']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data.pop('user'))
        profile = UserProfile(**validated_data, user=user)
        profile.save()

        return profile


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'link', 'admin']
        extra_kwargs = {
            "link": {"read_only": True}
        }

    def create(self, validated_data):
        link = get_random_string(length=32)
        admin = validated_data.pop('admin')[0]

        room = Room(**validated_data, link=link)
        room.save()
        room.admin.add(admin)

        return room


class RoomRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'link', 'admin', 'participate']


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'title', 'start_time', 'end_time', 'room']


# class UserRoomJoinSerializer(serializers.ModelSerializer):
#     user_profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
#
#     class Meta:
#         model = Room
#         fields = ['id', 'user_profile']
#         extra_kwargs = {
#             "user_profile": {"write_only": True}
#         }
#
#     def update(self, instance, validated_data):
#         instance.participate.add(validated_data.get('user_profile'))
#         return instance
