# from django.shortcuts import render, redirect

# def login_view(request):
#     if request.method == 'POST':
#         # 로그인 처리 로직
#         return render(request, 'chatbot/chatbot.html')
#     return render(request, 'account/login.html')    

# def register_view(request):
#     if request.method == 'POST':
#         # 회원가입 처리 로직
#         return redirect('account:login')  # 로그인 페이지로 리다이렉트
#     return render(request, 'account/register.html')

from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView 
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed , APIException
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from .token import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from .serializer import UserSerializer
from .models import CustomUser

# 회원가입
class RegisterView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            _ = decode_access_token(token)
            return render(request, 'chatbot/chatbot.html')
        return render(request, 'account/register.html')

    def post(self, request):
        username = request.data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise APIException('이미 존재하는 유저입니다.')
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        return response

# 로그인
class LoginView(APIView):
    def get(self, request):
        # print('request get: ', request.META)
        print('request get: ', request.META)
        auth = get_authorization_header(request).split()
        print('auth: ', auth)
        if auth and len(auth) == 1:
            token = auth[1].decode('utf-8')
            _ = decode_access_token(token)
            return render(request, 'chatbot/chatbot.html')  # 챗봇 페이지 render => redirect로 수정해야할 듯 싶어요
        return render(request, 'account/login.html')

    def post(self, request):
        print('request post: ', request.data)
        username = request.data['credential']
        password = request.data['password']

        user = CustomUser.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('존재하지 않는 유저입니다.')
        if not user.check_password(password):
            raise AuthenticationFailed('비밀번호가 틀렸습니다.')
    
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.set_cookie(key='access_token', value=access_token, httponly=True)
        response.data = {
            'token': access_token
        }
        return response

class LogoutView(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.delete_cookie(key='access_token')
        response.data = {
            'message': '로그아웃 성공'
        }
        return response