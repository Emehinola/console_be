from django.db import models
from django.contrib.auth.models import User

class ConsoleUser(User):
    phone = models.CharField(max_length=15)
    nationality = models.CharField(max_length=50)
    ethnicity = models.CharField(max_length=50)
    religion = models.CharField(max_length=50) 
    lga = models.CharField(max_length=50)
    place_of_pry_ass = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    garrison = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    platoon = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.username
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)