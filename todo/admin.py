from django.contrib import admin
from .models import Todo, File


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = 'Created',

class FileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Todo, TodoAdmin)
admin.site.register(File, FileAdmin)

