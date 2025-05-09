from django.contrib import admin
from django.urls import path
from .views import (
    login_view,
    register_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('register/', register_view),
] 
