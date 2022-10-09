from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import (CustomUser, Patient, Appointment, Test, Drug)

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class PatientsCreateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
    

class AppointmentCreateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"

class DrugCreateForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = "__all__"

class TestCreateForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = "__all__"


