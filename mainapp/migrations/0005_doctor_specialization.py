# Generated by Django 4.1 on 2022-08-16 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_doctor_avatar_alter_doctor_vat'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='specialization',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
