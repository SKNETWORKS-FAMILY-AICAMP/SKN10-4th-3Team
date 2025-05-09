from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def login_view(request):
    if request.method == 'POST':
        # 로그인 처리 로직
        return Response({
            'message': '로그인 성공',
            # redirect_url 수정 필요
            'redirect_url': '/chatbot/'  # 챗봇 페이지로 리다이렉트
        }, status=status.HTTP_200_OK)
    return render(request, 'account/login.html')    

@api_view(['GET', 'POST'])
def register_view(request):
    if request.method == 'POST':
        # 회원가입 처리 로직
        return Response({
            'message': '회원가입 성공',
            'redirect_url': '/account/login/'  # 로그인 페이지로 리다이렉트
        }, status=status.HTTP_201_CREATED)
    return render(request, 'account/register.html')


