from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from mainapp.producer import publish

from mainapp.utils import save_sql_queries
from .models import (Doctor, Drug, Patient, Appointment, PatientHistory,
 MedicalCondition, Prescription, Schedule, Test)
from .forms import PatientsCreateForm, AppointmentCreateForm, DrugCreateForm, TestCreateForm
from django.db import connections
from .models import SiteConfiguration


User = get_user_model()

@login_required(login_url='login')
def home(request):
    patients = Patient.objects.all().order_by('-created_at')
    doctors = Doctor.objects.all().order_by('-created_at')
    appts = Appointment.objects.all().order_by('-created_at')
    context = {
        'patients':patients,
        'doctors':doctors,
        'appts':appts
    }
    return render(request, 'mainapp/index.html', context)

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        user = authenticate(request,username=username, password=password)

        if user is None:
            messages.error(request, "Sorry, incorrect credentials")
            return redirect(request.META['HTTP_REFERER'])
        else:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')
    return render(request, 'mainapp/auth/login.html')

@login_required(login_url='login')
def log_out(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_n', None)
        last_name = request.POST.get('last_n', None)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exist")
            return redirect(request.META['HTTP_REFERER'])
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exist")
            return redirect(request.META['HTTP_REFERER'])
        else:
            user = User.objects.create(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )

            user.set_password(password)
            user.save()
            # publish('user',{'first_name':first_name,'last_name':last_name,'username':username,'email':email,'password':password,'who':'node1'})
            messages.success(request, "Account has been created")
            return redirect('login')
    return render(request, 'mainapp/auth/register.html')

def password_reset(request):
    return render(request, 'mainapp/auth/password.html')

@login_required(login_url='login')
def all_doctor(request):
    doctors = Doctor.objects.exclude(user=request.user)
    context = {'doctors':doctors}
    return render(request,'mainapp/doctor-list.html', context)

@login_required(login_url='login')
def doctor_profile(request, id):
    doctor = Doctor.objects.get(id=id)
    return render(request,'mainapp/doctor-profile.html', {'doctor':doctor})

@login_required(login_url='login')
def new_appointment(request):
    if request.method == "POST":
        form = AppointmentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            # data = form.cleaned_data
            # data['who'] = 'node1'
            # publish('appt',data)
            messages.success(request,"Appointment has been created successfully")
            save_sql_queries(connections['default'].queries[-1], 'appt')
            config = SiteConfiguration.get_solo()
            if config.sync_data_realtime:
                publish()
            return redirect(request.META['HTTP_REFERER'])
        else:
            # print(form)
            messages.error(request,form.errors)
            return redirect(request.META['HTTP_REFERER'])
    appts = Appointment.objects.all().order_by('-created_at')
    patients = Patient.objects.all()
    context = {
        "appts":appts,
        "patients":patients
    }
    return render(request, 'mainapp/new-appointment.html', context)

@login_required(login_url='login')
def update_appt_status(request, id):
    appt = Appointment.objects.get(id=id)
    value = request.POST.get('status')
    appt.status = value
    appt.save()
    # publish('appt_update',{'who':'node1', 'id':id,'status':value})
    save_sql_queries(connections['default'].queries[-1], 'appt')
    config = SiteConfiguration.get_solo()
    if config.sync_data_realtime:
        
        publish()
    messages.success(request, "Appointment status has been updated successfully")
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='login')
def add_prescription(request):
    if request.method == "POST":
        try:
            patient = request.POST.get('patient')
            drug_list = {}
            drug_list['drug1'] = request.POST.get('drug1')
            drug_list['drugUnit1'] = request.POST.get('drugUnit1')
            drug_list['dose1'] = request.POST.get('dose1')
            drug_list['duration1'] = request.POST.get('duration1')
            drug_list['note1'] = request.POST.get('note1')
            
            if request.POST.get('drug2'):
                drug_list['drug2'] = request.POST.get('drug2')
                drug_list['drugUnit2'] = request.POST.get('drugUnit2')
                drug_list['dose2'] = request.POST.get('dose2')
                drug_list['duration2'] = request.POST.get('duration2')
                drug_list['note2'] = request.POST.get('note2')

            if request.POST.get('drug3'):
                drug_list['drug3'] = request.POST.get('drug3')
                drug_list['drugUnit3'] = request.POST.get('drugUnit3')
                drug_list['dose3'] = request.POST.get('dose3')
                drug_list['duration3'] = request.POST.get('duration3')
                drug_list['note3'] = request.POST.get('note3')


            test_list = {}
            if request.POST.get('test1'):
                test_list['test1'] = request.POST.get('test1')
                test_list['testdes1'] = request.POST.get('testdes1')
            
            if request.POST.get('test2'):
                test_list['test2'] = request.POST.get('test2')
                test_list['testdes2'] = request.POST.get('testdes2')
            
            if request.POST.get('test3'):
                test_list['test3'] = request.POST.get('test3')
                test_list['testdes3'] = request.POST.get('testdes3')

            prescription = Prescription.objects.create(
                patient = Patient.objects.get(id=patient),
                doctor = request.user.profile,
                drug_list = drug_list,
                test_list = test_list
            )
            prescription.save()
            # data = {
            #     'who':'node1',
            #     'patient':patient,
            #     'doctor': request.user.profile.id,
            #     'drug_list':drug_list,
            #     'test_list':test_list
            # }
            # publish('prescription',data)
            save_sql_queries(connections['default'].queries[-1], 'pres')
            config = SiteConfiguration.get_solo()
            if config.sync_data_realtime:
                publish()
            messages.success(request, "Precription has been created successfully")
            return redirect('all_prescription')
        except Exception as e:
            print(e)
            messages.error(request, "Sorry, something went wrong")
            return redirect(request.META['HTTP_REFERER'])

    patients = Patient.objects.all()
    drugs = Drug.objects.all()
    tests = Test.objects.all()
    return render(request, "mainapp/add-prescription.html", {'patients':patients, 'drugs':drugs,'tests':tests})

@login_required(login_url='login')
def all_prescription(request):
    context = {
        "prescriptions": Prescription.objects.all()
    }
    return render(request, "mainapp/all-prescriptions.html", context)


@login_required(login_url='login')
def new_patient(request):
    if request.method == 'POST':
        patient = PatientsCreateForm(request.POST,request.FILES)
        if patient.is_valid():
            patient.save()

            save_sql_queries(connections['default'].queries[-1], 'pat')
            config = SiteConfiguration.get_solo()
            if config.sync_data_realtime:
                publish()
            messages.success(request, "Patient has been created successfully")
            return redirect('all_patient')
        else:
            messages.error(request, "Sorry something went wrong")
            return redirect(request.META['HTTP_REFERER'])
    return render(request, "mainapp/new-patient.html")

@login_required(login_url='login')
def all_patients(request):
    patients = Patient.objects.all()

    return render(request, "mainapp/patients.html", {'patients':patients})

@login_required(login_url='login')
def update_patient(request, id):
    patient = Patient.objects.get(id=id)
    try:
        patient.first_name = request.POST.get('first_name')
        patient.last_name = request.POST.get('last_name')
        patient.dob = request.POST.get('dob')
        patient.mobile_number = request.POST.get('mobile_number')
        patient.email = request.POST.get('email')
        patient.marital_status = request.POST.get('marital_status')
        patient.sex = request.POST.get('sex')
        patient.blood_group = request.POST.get('blood_group')
        patient.weight = request.POST.get('weight')
        patient.height = request.POST.get('height')
        patient.address = request.POST.get('address')
        patient.avatar = request.FILES.get('avatar', None)
        patient.save()
        save_sql_queries(connections['default'].queries[-1], 'pat')
        config = SiteConfiguration.get_solo()
        if config.sync_data_realtime:
            publish()
        messages.success(request, "Patient details has been updated successfully")
        return  redirect(request.META['HTTP_REFERER'])
    except Exception as e:
        print(e)
        messages.error(request, "Sorry, something went wrong")
        return  redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def delete_patient(request, id):
    patient = Patient.objects.get(id=id)
    patient.delete()

    config = SiteConfiguration.get_solo()
    save_sql_queries(connections['default'].queries[-1], 'pat')
    if config.sync_data_realtime:
        
        publish()

    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def add_test(request):
    if request.method == "POST":
        form = TestCreateForm(request.POST)
        if form.is_valid():
            form.save()
            save_sql_queries(connections['default'].queries[-1], 'test')
            config = SiteConfiguration.get_solo()
            if config.sync_data_realtime:
                
                publish()
            messages.success(request, "Test has been added successfully")
            return redirect('all_test')
        else:
            messages.error(request, form.errors)
            return redirect(request.META['HTTP_REFERER'])
    return render(request, "mainapp/add-test.html")

@login_required(login_url='login')
def all_test(request):
    context = {
        "tests":Test.objects.all()
    }
    return render(request, "mainapp/all-tests.html", context)

@login_required(login_url='login')
def update_test(request, id):
    test = Test.objects.get(id=id)
    test.name = request.POST.get('name')
    test.description = request.POST.get('description')
    test.save()
    save_sql_queries(connections['default'].queries[-1], 'test')
    config = SiteConfiguration.get_solo()
    if config.sync_data_realtime:
        
        publish()

    messages.success(request, "Test has been updated successfully")
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def delete_test(request, id):
    test = Test.objects.get(id=id)
    test.delete()
    save_sql_queries(connections['default'].queries[-1], 'test')
    config = SiteConfiguration.get_solo()
    if config.sync_data_realtime:
        publish()

    messages.success(request, "Test has been deleted successfully")
    return redirect(request.META['HTTP_REFERER'])    

@login_required(login_url='login')
def add_drug(request):
    if request.method == "POST":
        form = DrugCreateForm(request.POST)
        if form.is_valid():
            form.save()
            save_sql_queries(connections['default'].queries[-1], 'drug')
            config = SiteConfiguration.get_solo()
            if config.sync_data_realtime:
                
                publish()

            messages.success(request, "Drug has been added successfully")
            return redirect(request.META['HTTP_REFERER'])
    context = {
        'drugs': Drug.objects.all().order_by('-created_at')
    }
    return render(request, "mainapp/add-drug.html", context)

@login_required(login_url='login')
def update_drug(request, id):
    drug = Drug.objects.get(id=id)
    try:
        drug.trade_name = request.POST.get('trade_name', drug.trade_name)
        drug.generic_name = request.POST.get('generic_name', drug.generic_name)
        drug.note = request.POST.get('note', drug.note)
        drug.save()
        save_sql_queries(connections['default'].queries[-1], 'drug')
        config = SiteConfiguration.get_solo()
        if config.sync_data_realtime:
            
            publish()

        messages.success(request, "Drug has been updated")
    except Exception as e:
        messages.error(request, "Sorry something went wrong")
    
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def delete_drug(request,id):
    drug = Drug.objects.get(id=id)
    drug.delete()
    save_sql_queries(connections['default'].queries[-1], 'drug')
    config = SiteConfiguration.get_solo()
    if config.sync_data_realtime:
        
        publish()

    messages.success(request, "Drug has been deleted")
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='login')
def reports(request):
    return render(request, "mainapp/reports.html")

@login_required(login_url='login')
def doctor_settings(request):
    return render(request, "mainapp/doctor-settings.html")

@login_required(login_url='login')
def prescription_settings(request):
    return render(request, "mainapp/prescription-settings.html")

@login_required(login_url='login')
def sync_data(request):
    return render(request,"mainapp/sync_data.html")

@login_required(login_url='login')
def process(request):
    publish()
    messages.success(request,"Data Synchronisation has started.")
    return redirect('home')
