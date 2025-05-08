from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
