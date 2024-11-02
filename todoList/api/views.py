from django.shortcuts import render
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoListView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API view để quản lý danh sách todo.
    """

    def get(self, request):
        """
        Lấy danh sách tất cả todo.
        """
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Tạo mới một todo.
        """
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid() and request.user.groups.filter(name="admin").exists():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        """
        Cập nhật thông tin của một todo cụ thể.
        """
        todo = Todo.objects.get(pk=pk)
        if todo is None:
            return Response({"detail": "Todo not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Xóa một todo cụ thể.
        """        
        todo = Todo.objects.get(pk=pk)
        if todo is None:
            return Response({"detail": "Todo not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.groups.filter(name='admin').exists(): 
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "You do not permission."}, status=status.HTTP_404_NOT_FOUND)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        # Kiểm tra tính hợp lệ của token
        token = request.data.get("token", None)
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]

            # Truy vấn thông tin người dùng
            user = User.objects.get(id=user_id)
            user_data = {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }

            return Response(
                {"message": "Token is valid", "user": user_data},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"message": "Token is invalid", "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )
