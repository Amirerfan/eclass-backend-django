from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404
from .serializers import ProfileSerializer, AuthSerializer, RoomCreateSerializer, RoomRetrieveSerializer, \
    ExamSerializer, QuestionSerializer, ExamRetrieveSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Room, Exam, UserProfile


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


class RetrieveUser(RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'


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


class JoinRoom(APIView):

    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, link=kwargs.get('room_link'))
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        user_profile = user.user_profile
        room.participate.add(user_profile)
        room = RoomRetrieveSerializer(instance=room)
        return Response(room.data, status=200)


class ExamCreate(CreateAPIView):
    serializer_class = ExamSerializer


class AddAdminToRoom(APIView):

    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, id=kwargs.get('room_id'))
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        user_profile = user.user_profile
        room.admin.add(user_profile)

        room.participate.remove(user.user_profile)

        room = RoomRetrieveSerializer(instance=room)
        return Response(room.data, status=200)


class RetrieveQuestion(RetrieveAPIView):
    serializer_class = QuestionSerializer


class RetrieveExamQuestions(APIView):

    def get(self, request, *args, **kwargs):
        exam = get_object_or_404(Exam, id=kwargs.get('exam_id'))
        questions = exam.question

        exam = ExamRetrieveSerializer(instance=exam).data
        questions = QuestionSerializer(instance=questions, many=True).data
        return Response({'exam': exam, 'questions': questions }, status=200)
