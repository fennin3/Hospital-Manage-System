from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Prescription, Schedule, Doctor, Patient, PatientHistory, Appointment, Drug, Test

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "time", "date", "brief")

class TestAdmin(admin.ModelAdmin):
    list_display = ("name", )




admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Schedule)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(PatientHistory)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Drug)
admin.site.register(Test)
admin.site.register(Prescription)