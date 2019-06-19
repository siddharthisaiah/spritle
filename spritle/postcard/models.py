from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Postcard(models.Model):
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    


class Comment(models.Model):
    comment = models.TextField()
    postcard = models.ForeignKey(Postcard, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postcard = models.ForeignKey(Postcard, on_delete=models.CASCADE)

