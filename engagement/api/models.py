from django.db import models
from patient.models import PatientSchedule

# Create your models here.
class PatientEngagement(models.Model):
    
    schedule = models.ForeignKey(PatientSchedule, on_delete=models.CASCADE)
    temperature = models.FloatField(max_length=10)
    pulse = models.CharField(max_length=10)
    upper_blood_pressure = models.FloatField(max_length=10)
    lower_blood_pressure = models.FloatField(max_length=10)
    oxygen_saturation = models.CharField(max_length=10)
    respiratory_rate = models.CharField(max_length=10)
    height = models.FloatField(max_length=10)
    weight = models.FloatField(max_length=10)
    engagement_doc = models.FileField(upload_to='engagements-docs')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Patient Engagements'

    def __str__(self) -> str:
        return f"{self.schedule.patient.full_name}"