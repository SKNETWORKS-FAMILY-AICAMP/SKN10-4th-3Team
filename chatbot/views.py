from django.shortcuts import render
from .models import Message, Session, PhilosophyData
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .utils.extract_keyword import get_keyword
from .utils.vectorizer import OpenAI_vectorizer
from .utils.llm import chat_with_philosophy

# Create your views here.


# 예시 API에요!
# @api_view(['GET'])
# def show_all_messages(request):
#     messages = Message.objects.all()    # 모든 메시지를 가져옵니다.
#     return render(request, 'chatbot/chatbot.html', context={'messages': messages})
def chatbot_page(request):
    return render(request, 'chatbot/chatbot2.html')


@api_view(['POST'])
def chat_api(request):
    message = request.data.get('message')
    session_id = request.data.get('session_id')

    if session_id:
        session = Session.objects.get(id=session_id)
        Message.objects.create(text=message, sender='user', session_id=session)

    # 여기서 실제 OpenAI 처리
    response = chat_with_philosophy(message)

    if session_id:
        Message.objects.create(text=response, sender='bot', session_id=session)

    return Response({"response": response})
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

    title = request.data.get('title')
    if not title:
        title = f"New session {timezone.now().strftime('%Y-%m-%d %H:%M')}"

    session = Session.objects.create(title=title,user_id=request.user)
    return Response({
        'id': session.id,
        'title': session.title,
        'created_at': session.created_at,
    })


@api_view(['GET'])
def get_messages_by_session(request, session_id):
    messages = Message.objects.filter(session_id=session_id).order_by('created_at')
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

<<<<<<< HEAD
=======

@api_view(['POST'])
def add_philosophy_data(request):
    author = request.data.get('author')
    quote = request.data.get('quote')
    quote_keywords = get_keyword(quote)
    quote_emb = OpenAI_vectorizer(quote)
    keywords_emb = OpenAI_vectorizer(quote_keywords)
    new_data = PhilosophyData.objects.create(
        author=author,
        quote=quote,
        quote_keywords=quote_keywords,
        quote_emb=quote_emb,
        keywords_emb=keywords_emb,
    )
    return Response({'success': True, 'quote': new_data.quote})
>>>>>>> origin/develop
