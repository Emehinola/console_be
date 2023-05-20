from rest_framework import serializers
from patient.models import Patient, PatientSchedule
from patient.api.helper import isLessThan, isEqual

import datetime



class PatientRegistrationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = '__all__'
        # exclude = ['image']

    def get_image_url(self, instance):
        return instance.image_url # return image url
    
    def get_full_name(self, instance):
        return instance.full_name
        
    def validate_email(self, email):

        if(Patient.objects.filter(email=email).exists()):
            raise serializers.ValidationError('Patient with this email already exists')
        
        else:
            return email
        

class PatientScheduleSerializer(serializers.ModelSerializer):
    patient = PatientRegistrationSerializer()

    class Meta:
        model = PatientSchedule
        fields = '__all__'


    def validate_appointment_date(self, data):
        today: datetime.date = datetime.date.today()

        if (isLessThan(data, today) or isEqual(data, today)):
            raise serializers.ValidationError("Appointment date must be greater than today's date")
        
        else:
            return data
        

    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)