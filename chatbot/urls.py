from django.urls import path
from .views import show_all_messages

urlpatterns = [
    path('show_all_messages/', show_all_messages, name='chatbot-show_all_messages'),
]
