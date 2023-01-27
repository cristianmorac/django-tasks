from django.contrib import admin

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    # muestra el campo en lectura
    readonly_fields = ('created',)

from .models import Task
admin.site.register(Task,TaskAdmin)

