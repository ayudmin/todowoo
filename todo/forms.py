from django.forms import ModelForm
from .models import Todo, File


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['Title', 'Memo', 'Important']

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'photo', 'file']