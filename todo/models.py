from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    Title = models.CharField(max_length=100, unique=True)
    Memo = models.TextField(blank=True)
    Created = models.DateTimeField(auto_now_add=True)
    Datecompleted = models.DateTimeField(null=True, blank=True)
    Important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file =  models.OneToOneField('File', blank=True,  on_delete=models.CASCADE)
    def __str__(self):
        return self.Title

class File(models.Model):
    name = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to="todo/files/photos/", blank=True)
    file = models.FileField(upload_to="todo/files/", blank=True)

    def __str__(self):
        return self.name