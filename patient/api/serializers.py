from rest_framework import serializers
from patient.models import Patient, PatientSchedule
from patient.api.helper import isLessThan, isEqual
from api.custom_exception import CustomException

import datetime



class PatientSerializer(serializers.ModelSerializer):
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
    patient = PatientSerializer(read_only=True, many=False)


    class Meta:
        model = PatientSchedule
        fields = '__all__'


    def validate_appointment_date(self, data):
        today: datetime.date = datetime.date.today()

        if (isLessThan(data, today) or isEqual(data, today)):
            raise serializers.ValidationError("Appointment date must be greater than today's date")
        
        else:
            return data
        
    
    def validate(self, validated_data):

        try:

            schedule_exists: bool = PatientSchedule.objects.filter(patient=validated_data['patient']).exists()
            is_future_date_or_today: bool = not isLessThan(validated_data['appointment_date'], datetime.date.today()) and not isEqual(validated_data['appointment_date'], datetime.date.today())

            if schedule_exists & is_future_date_or_today:
                raise CustomException(detail="This patient currently has a pending appointment")
        
        except Exception as e:
            raise CustomException(str(e))

        return validated_data
        

    def is_valid(self, *, patient: Patient = None, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)
    

    def create(self, validated_data):
        return super().create(validated_data)
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)