# Generated by Django 4.1.5 on 2023-05-28 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0003_patientschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientEngagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_created=True)),
                ('temperature', models.FloatField(max_length=10)),
                ('pulse', models.CharField(max_length=10)),
                ('upper_blood_pressure', models.FloatField(max_length=10)),
                ('lower_blood_pressure', models.FloatField(max_length=10)),
                ('oxygen_saturation', models.CharField(max_length=10)),
                ('respiratory_rate', models.CharField(max_length=10)),
                ('height', models.FloatField(max_length=10)),
                ('weight', models.FloatField(max_length=10)),
                ('engagement_doc', models.FileField(upload_to='engagements-docs')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patientschedule')),
            ],
            options={
                'verbose_name_plural': 'Patient Engagements',
            },
        ),
    ]
