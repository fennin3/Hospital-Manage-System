# Generated by Django 4.1 on 2022-08-16 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_doctor_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/avatars/'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='vat',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
    ]
