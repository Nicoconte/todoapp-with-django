from django import forms
from django.forms import widgets

class TaskForm(forms.Form):
    CHOICES = (("alta", "Alta"), ("media", "Media"), ("baja", "Baja"))

    task = forms.CharField(label="", widget=forms.Textarea(attrs={
        "class" : "form-control",
        "placeholder" : "Tarea a realizar"
    }))

    priority = forms.ChoiceField(label="", choices=CHOICES, widget=forms.Select(attrs={
        "class" : "form-control mt-2"
    }))

    limit_date = forms.DateField(label="", widget=forms.DateInput(attrs={
        "class" : "form-control mt-2",
        "type" : "date"
    }))

