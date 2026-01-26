from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, ClassInfo
from .serializers import UserSerializer, ClassInfoSerializer

class LoginView(APIView):
    """
    用户登录接口 (升级版：返回真实 Token)
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "msg": "登录成功",
                "token": token.key,
                "role": user.role,
                "username": user.nickname or user.username
            })
        else:
            return Response({"msg": "账号或密码错误"}, status=400)

class ClassInfoViewSet(viewsets.ModelViewSet):
    queryset = ClassInfo.objects.all().order_by('-created_at')
    serializer_class = ClassInfoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role', 'class_info']
    search_fields = ['nickname', 'username', 'phone']

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """重置密码为 123456"""
        user = self.get_object()
        user.set_password('123456')
        user.save()
        return Response({"msg": "密码已重置为 123456"}, status=status.HTTP_200_OK)