from django.shortcuts import render
from .models import Message
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.

# 예시 API에요!
@api_view(['GET'])
def show_all_messages(request):
    messages = Message.objects.all()    # 모든 메시지를 가져옵니다.
    return render(request, 'chatbot/chatbot.html', context={'messages': messages})
