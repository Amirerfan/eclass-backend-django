from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')

    def __str__(self):
        return str(self.user)

    @property
    def token(self):
        token, created = Token.objects.get_or_create(user=self.user)
        return token.key


class Room(models.Model):
    name = models.CharField(max_length=225)
    link = models.CharField(max_length=225)

    admin = models.ManyToManyField(UserProfile, related_name="controlling")
    participate = models.ManyToManyField(UserProfile, blank=True, related_name="classes")

    def __str__(self):
        return self.name


class Question(models.Model):
    number = models.IntegerField()
    text = models.CharField(max_length=500)
    credit = models.IntegerField()
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, related_name="question")

    def __str__(self):
        return str(self.exam) + " : " + str(self.text)


class Exam(models.Model):
    title = models.CharField(max_length=225)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="exams")

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        return self.start_time <= timezone.now() <= self.end_time


class Answer(models.Model):
    text = models.CharField(max_length=500)

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    exam_answer = models.ForeignKey('ExamAnswer', on_delete=models.CASCADE, related_name="answers")

    def __str__(self):
        return str(self.question) + " : " + str(self.text)


class ExamAnswer(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="exam_answers")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="answers")

    @property
    def is_active(self):
        return self.exam.is_active

    def __str__(self):
        return str(self.user_profile) + " : " + str(self.exam)
