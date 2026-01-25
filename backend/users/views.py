from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer

# 这是一个独立的登录视图 (如果不想用 Token 库的话，这是最简单的写法)
from rest_framework.views import APIView


class LoginView(APIView):
    """
    用户登录接口 (升级版：返回真实 Token)
    """
    authentication_classes = []  # 不需要认证即可访问
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # 验证账号密码
        user = authenticate(username=username, password=password)

        if user is not None:
            # 🟢 [核心修改] 获取或创建真实的 DRF Token
            # 注意：这会在数据库 authtoken_token 表中生成记录
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                "msg": "登录成功",
                "token": token.key,  # 👈 返回真实的 Token 字符串
                "role": user.role,
                "username": user.nickname or user.username
            })
        else:
            return Response({"msg": "账号或密码错误"}, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['role', 'class_name']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    # 启用过滤和搜索
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    # 精确过滤 (比如按角色、班级筛选)
    filterset_fields = ['role', 'class_name']

    # 模糊搜索 (比如按昵称、账号、手机号搜索)
    search_fields = ['nickname', 'username', 'phone']