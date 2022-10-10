from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from solo.models import SingletonModel




class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=True)

    def get_full_name(self) -> str:
        return super().get_full_name()

class Schedule(models.Model):
    day = models.CharField(max_length=16)
    from_time = models.CharField(max_length=25)
    to_time = models.CharField(max_length=25)


    def __str__(self):
        return self.day
    


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    title = models.CharField(max_length=10)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=16)
    biography = models.TextField(blank=True, null=True)
    hospital_email = models.EmailField()
    currency = models.CharField(max_length=25)
    vat = models.DecimalField(decimal_places=2, max_digits=3, default=0.00)
    language = models.CharField(max_length=55)
    avatar = models.ImageField(upload_to="media/avatars/", null=True, blank=True, default="media/avatar.jpg")
    appt_interval = models.CharField(max_length=25)
    schedules = models.ManyToManyField(Schedule, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.user.get_full_name()}"



class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    mobile_number = models.CharField(max_length=16)
    dob = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=55)
    sex = models.CharField(max_length=16)
    blood_group = models.CharField(max_length=16)
    weight = models.CharField(max_length=255, null=True, blank=True)
    height = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="media/avatars/", default="media/patient.jpg")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}  [{self.id}]"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient, related_name="history", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class MedicalCondition(models.Model):
    diseases = models.TextField()
    period = models.CharField(max_length=255)
    family_history = models.CharField(max_length=255)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appt')
    date = models.DateField()
    time = models.CharField(max_length=255)
    brief = models.CharField(max_length=10000)
    status = models.CharField(max_length=25, default="Pending", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Drug(models.Model):
    trade_name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.trade_name


class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return self.name
    

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_prescriptions")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_prescriptions")
    drug_list = models.JSONField(default=dict)
    test_list = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class SiteConfiguration(SingletonModel):
    sync_data_realtime = models.BooleanField(default=False)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
    


