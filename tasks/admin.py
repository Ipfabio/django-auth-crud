from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",) # Pasamos en la tupla el elemento que queremos hacer visible

# Register your models here.
admin.site.register(Task, TaskAdmin)