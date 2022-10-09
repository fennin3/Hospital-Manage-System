import os, pika, json, django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE",'hms.settings')

django.setup()
from mainapp.models import (Appointment, Doctor, Patient, Prescription)



User = get_user_model()

params = pika.URLParameters('amqps://xregxoau:gqcHbeVpVyMOUbIT6Xp27DoxtBoFsCfb@jackal.rmq.cloudamqp.com/xregxoau')
connection = pika.BlockingConnection(params)

channel = connection.channel()


channel.queue_declare(queue='users', durable=True)


def callback(ch, method, properties, body):
    data = json.loads(body)
    message_type = properties.content_type
    if data['who'] == 'node1':
        queries = data['queries']
        for query in queries:
            data = json.loads(query)
    else:
        print(f"Skipping Now.. Same Node [{data['who']}]")


channel.basic_consume(queue='users', on_message_callback=callback, auto_ack=True)

print("Started Consuming")

channel.start_consuming()

channel.close()



# if message_type == 'user':
        #     user = User.objects.create(
        #         email=data['email'],
        #         username=data['username'],
        #         first_name=data['first_name'],
        #         last_name=data['last_name'],
        #     )
        #     user.set_password(data['password'])
        #     user.save()
        # elif message_type == 'appt':
        #     appt = Appointment.objects.create(
        #         patient = data['patient'],
        #         date = data['date'],
        #         time = data['time'],
        #         brief = data['brief']
        #     )
        #     appt.save()
        # elif message_type == 'appt_update':
        #     appt = Appointment.objects.get(id=data['id'])
        #     appt.status = data['value']
        #     appt.save()

        # elif message_type == 'prescription':
        #     patient = Patient.objects.get(id=data['patient'])
        #     doctor = Doctor.objects.get(id=data['doctor'])
        #     prescription = Prescription.objects.create(
        #         patient = Patient.objects.get(id=patient),
        #         doctor = doctor,
        #         drug_list = data['drug_list'],
        #         test_list = data['test_list']
        #     )
        #     prescription.save()
        # elif message_type == 'new_patient':
        #     patient = Patient.objects.create(
        #         first_name = data['first_name'],
        #         last_name = data['last_name'],
        #         dob = data['dob'],
        #         mobile_number = data['mobile_number'],
        #         email = data['email'],
        #         marital_status = data['marital_status'],
        #         sex = data['sex'],
        #         blood_group = data['blood_group'],
        #         weight = data['weight'],
        #         height = data['height'],
        #         address = data['address'],
        #         avatar = data['avatar']
        #     )