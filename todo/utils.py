from .models import File, Todo

def find_file(todo):
    todo = Todo.objects.get(Title=todo)
    if todo:
        try:
            todo_file = File.objects.get(todo=todo)
            if todo_file:
                return todo_file
        except File.DoesNotExist:
            return False
