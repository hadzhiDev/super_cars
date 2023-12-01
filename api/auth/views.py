from django.contrib.auth import authenticate
from account.models import User, UserResetPassword
# from account.managers import UserPasswordResetManager

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, UpdateAPIView, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.auth.serializers import LoginSerializer, UserSerializer, RegisterUserSerializer, ChangePasswordSerializer, \
    ProfileSerializer, SendResetPasswordKeySerializer, ResetPasswordSerializer
from api.auth.mixins import UltraModelViewSet
from api.auth.services import ResetPasswordManager


class LoginGenericAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user:
            token = Token.objects.get_or_create(user=user)[0]
            user_serializer = UserSerializer(instance=user, context={'request': request})
            return Response({
                **user_serializer.data,
                'token': token.key,
            })
        return Response({'message': 'The user is not found or the password is invalid'},
                        status=status.HTTP_400_BAD_REQUEST)


class RegisterGenericAPIView(GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)[0]
        user_serializer = UserSerializer(instance=user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key,
        })


class UsersViewSet(UltraModelViewSet):
    queryset = User.objects.all()
    # pagination_class = SimpleResultPagination
    serializer_classes = {
        'list': UserSerializer,
        'create': RegisterUserSerializer,
        'update': RegisterUserSerializer,
        'retrieve': UserSerializer,
    }
    lookup_field = 'id'
    permission_classes = (AllowAny,)


class ProfileViewSet(UltraModelViewSet):
    queryset = User.objects.all()
    # pagination_class = SimpleResultPagination
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    permission_classes = (AllowAny,)


class ChangePasswordApiView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if self.object.check_password(serializer.data.get("old_password")):
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)
            else:
                return Response({"old_password": ['Wrong password']}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SendResetPasswordKeyApiView(GenericAPIView):
    serializer_class = SendResetPasswordKeySerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email', None)
        user = get_object_or_404(User, email=email)
        manager = ResetPasswordManager(user)
        manager.send_key()
        return Response({'detail': 'Ключ успещно отправлен'})


class ResetPasswordApiView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.validated_data.get('key', None)
        new_password = serializer.validated_data.get('new_password', None)
        user = get_object_or_404(UserResetPassword, key=key).user
        manager = ResetPasswordManager(user)
        is_changed = manager.reset_password(key, new_password)
        return Response(
            {'is_changed': is_changed},
            status=status.HTTP_200_OK if is_changed else status.HTTP_400_BAD_REQUEST
        )
