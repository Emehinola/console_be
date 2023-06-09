# Generated by Django 4.1.5 on 2023-05-20 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_patient_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.CharField(max_length=200)),
                ('appointment_date', models.DateTimeField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient', to='patient.patient')),
            ],
            options={
                'verbose_name_plural': 'Patient schedules',
            },
        ),
    ]
