from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.crypto import get_random_string

from .models import UserProfile, Room, Exam, Question


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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class ExamRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    questions = serializers.ListField(write_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'start_time', 'end_time', 'room', 'questions']

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        exam = Exam.objects.create(**validated_data)

        for question in questions:
            Question.objects.create(exam=exam, **question)

        return exam
