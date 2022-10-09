from django.urls import path, include
from . import views


urlpatterns = [
    path("",views.home, name="home"),
    path("login", views.sign_in, name="login"),
    path("logout", views.log_out, name="logout"),
    path("register", views.register, name="register"),
    path("forgot-password", views.password_reset, name="forgot_pass"),
    path("all-doctors", views.all_doctor, name="all_doctors"),
    path("doctor-profile/<int:id>", views.doctor_profile, name="doctor_profile"),
    path('new-appointment', views.new_appointment, name="new_appointment"),
    path('update-appointment/<int:id>', views.update_appt_status, name="appt_status"),
    path('add-prescription', views.add_prescription, name="add_prescription"),
    path('all-prescriptions', views.all_prescription, name="all_prescription"),
    path('new-patient', views.new_patient, name="new_patient"),
    path('update-patient/<int:id>', views.update_patient, name="update_patient"),
    path('delete-patient/<int:id>', views.delete_patient, name="delete_patient"),
    path('all-patients', views.all_patients, name="all_patient"),
    path('add-test', views.add_test, name="add_test"),
    path('all-test', views.all_test, name="all_test"),
    path('update-test/<int:id>', views.update_test, name="update_test"),
    path('delete-test/<int:id>', views.delete_test, name="delete_test"),
    path('add-drug', views.add_drug, name="add_drug"),
    path('update-drug/<int:id>', views.update_drug, name="update_drug"),
    path('delete-drug/<int:id>', views.delete_drug, name="delete_drug"),
    path('reports', views.reports, name="reports"),
    path('doctor-settings', views.doctor_settings, name="doctor_settings"),
    path('prescription-settings', views.prescription_settings, name="prescription_settings"),
]
