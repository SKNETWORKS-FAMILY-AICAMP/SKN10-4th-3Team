from django.contrib import admin
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', views.chatbot_view, name='chat'),
]
