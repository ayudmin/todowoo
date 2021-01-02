from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    Title = models.CharField(max_length=100)
    Memo = models.TextField(blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Datecompleted = models.DateTimeField(null=True, blank=True)
    Important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Title
