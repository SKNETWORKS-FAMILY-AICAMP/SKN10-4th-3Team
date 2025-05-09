from django.shortcuts import render
from .models import Message, Session
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

# Create your views here.


# 예시 API에요!
# @api_view(['GET'])
# def show_all_messages(request):
#     messages = Message.objects.all()    # 모든 메시지를 가져옵니다.
#     return render(request, 'chatbot/chatbot.html', context={'messages': messages})


@api_view(['GET'])
def list_sessions(request):
    sessions = Session.objects.all().order_by('-created_at')
    data = [
        {
            'id': session.id,
            'title': session.title,
            'created_at': session.created_at,
        }
        for session in sessions
    ]
    return Response(data)

@api_view(['POST'])
def create_session(request):
    title = request.data.get('title', f"New session {timezone.now().strftime('%Y-%m-%d %H:%M')}")
    session = Session.objects.create(title=title)
    return Response({
        'id': session.id,
        'title': session.title,
        'created_at': session.created_at,
    })


@api_view(['GET'])
def get_messages_by_session(request, session_id):
    messages = Message.objects.filter(id=session_id).order_by('created_at')
    data = [
        {
            'id': m.id,
            'sender': m.sender,
            'text': m.text,
            'created_at': m.created_at,
        }
        for m in messages
    ]
    return Response(data)

@api_view(['POST'])
def delete_session(request, session_id):
    try:
        session = Session.objects.get(id=session_id)
        session.delete()
        return Response({'success': True})
    except Session.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

