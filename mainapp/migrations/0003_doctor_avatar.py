# Generated by Django 4.1 on 2022-08-16 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_schedule_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='avatar',
            field=models.ImageField(null=True, upload_to='media/avatars/'),
        ),
    ]
