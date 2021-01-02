from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = 'Created',


admin.site.register(Todo, TodoAdmin)
