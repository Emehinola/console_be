from django.db import models
from django.core.exceptions import ValidationError

from console_be.settings import HOST


def validate_age(age):
    if(int(age) < 18):
        raise ValidationError('Age must be greater than 18')

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    image = models.ImageField(upload_to='patient-images', blank=True)
    group_type = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=5)
    genotype = models.CharField(max_length=5)
    age = models.CharField(max_length=3, validators=[validate_age])
    sex = models.CharField(max_length=10)
    social_handle = models.CharField(max_length=50, blank=True)
    rank = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    garrison = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    platoon = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    place_of_pry_assignment = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Patients'

    @property # treats method as property
    def full_name(self):
        return f"{self.first_name} {self.middle_name}, {self.last_name}"
    
    @property
    def image_url(self):
    
        try:
            return HOST + '/' + str(self.image)
        
        except:
            return ""
        
    def save(self, *args, **kwargs):
        if(Patient.objects.filter(email=self.email).exists()):
            raise ValidationError('Patient with email already exists')

        super().save(*args, **kwargs)
        
