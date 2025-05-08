from django.urls import path
# from .views import show_all_messages
from .views import (
    # show_all_messages,
    list_sessions,
    create_session,
    get_messages_by_session,
    delete_session,
)


urlpatterns = [
    # path('show_all_messages/', show_all_messages, name='chatbot-show_all_messages'),
    path('sessions/', list_sessions),  # GET
    path('sessions/create/', create_session),  # POST
    path('sessions/<int:session_id>/messages/', get_messages_by_session),  # GET
    path('sessions/<int:session_id>/delete/', delete_session),  # DELETE
]
