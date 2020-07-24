from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404, UpdateAPIView
from .serializers import ProfileSerializer, AuthSerializer, RoomCreateSerializer, RoomRetrieveSerializer, \
    ExamSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Room, Exam, UserProfile

from .serializers import UserRoomJoinSerializer


class CreateUser(CreateAPIView):
    serializer_class = ProfileSerializer


class Authentication(APIView):
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.data.get('username'))

            if user.check_password(request.data.get('password')):
                profile = user.user_profile
                profile_serializer = ProfileSerializer(instance=profile)

                return Response(profile_serializer.data)
            raise User.DoesNotExist
        except User.DoesNotExist:
            return Response({'error': 'Invalid Username or Password'}, status=400)


class CreateRoom(CreateAPIView):
    serializer_class = RoomCreateSerializer


class RetrieveRoom(RetrieveAPIView):
    serializer_class = RoomRetrieveSerializer
    queryset = Room.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'room_id'


class CreateExam(CreateAPIView):
    serializer_class = ExamSerializer


class RetrieveExam(RetrieveAPIView):
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'exam_id'


class RetrieveUserRooms(APIView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(UserProfile, id=kwargs.get('user_id'))

        admin = RoomRetrieveSerializer(instance=user.controlling.all(), many=True)
        participated = RoomRetrieveSerializer(instance=user.classes.all(), many=True)

        data = {
            'admin': admin.data,
            'participated': participated.data
        }

        return Response(data, status=200)


class RetrieveRoomExams(APIView):

    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, id=kwargs.get('room_id'))
        exams = ExamSerializer(instance=room.exams.all(), many=True)

        return Response(exams.data, status=200)


class JoinRoom(UpdateAPIView):
    serializer_class = UserRoomJoinSerializer
