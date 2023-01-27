from django.db import models

# Create your models here.

# importar modelo user
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    # relación con la tabla de django User
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title