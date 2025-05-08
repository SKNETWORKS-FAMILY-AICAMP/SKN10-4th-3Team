from django.db import models

class Session(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    # session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='messages')  # 이 줄 중요!!
    sender = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

