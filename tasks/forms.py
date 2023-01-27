from django.forms import ModelForm
from .models import Task

#importar el formulario
from django import forms
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']
        # especificar otros atributos de inputs que esta generando
        widgets = {
            # Agregar clases html
            'title': forms.TextInput(attrs={'class':'form-control border-dark', 'placeholder': 'write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control border-dark', 'placeholder': 'write a description'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input border-dark'}), 
        }