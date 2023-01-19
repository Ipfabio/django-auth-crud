from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True) # cuando creamos la tarea, añade la fecha y la hora por defecto en caso de que no le pasemos el dato
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # El modelo de usuario

    def __str__(self):
        str = f"Tarea: {self.title} - by {self.user.username} "
        return str
    
