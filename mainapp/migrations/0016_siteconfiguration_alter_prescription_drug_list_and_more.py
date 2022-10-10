# Generated by Django 4.0.8 on 2022-10-09 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_prescription'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sync_data_realtime', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
        migrations.AlterField(
            model_name='prescription',
            name='drug_list',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='test_list',
            field=models.JSONField(default=dict),
        ),
    ]
