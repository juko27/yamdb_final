import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import RegisterSerializer, UsersSerializer, VerifySerializer

User = get_user_model()


class Register(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = request.data.get('email')
            username = email.split('@')[0]
            code = random.random()
            get_user_model().objects.create(
                email=email,
                username=username,
                confirmation_code=code,
            )
            user = get_user_model().objects.get(
                username=username,
                email=email
            )
            password = get_user_model().objects.make_random_password(length=8)
            user.set_password(password)
            user.save()
            send_mail(code,
                      password,
                      settings.EMAIL_HOST_USER,
                      [email, ],
                      fail_silently=False,
                      )
            return Response(
                {
                    "user": UsersSerializer(
                        user,
                        context=self.get_serializer_context()
                    ).data,
                    "message": "Подтвердите email отправленным кодом.",
                },
                status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Verify(generics.GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            user = get_user_model().objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            if user.confirmation_code == \
                    serializer.data.get('confirmation_code'):
                return Response(
                    {
                        'refresh': str(refresh),
                        'token': str(refresh.access_token),
                        'message': 'Почта подтверждена успешно.'
                    }
                )
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersCommonViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin, IsAuthenticated)
    serializer_class = UsersSerializer
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = UsersSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
