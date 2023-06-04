from rest_framework import serializers
from .models import PatientEngagement
from patient.models import PatientSchedule

from rest_framework import status

from api.custom_exception import CustomException

class PatientEngagementSerializer(serializers.Serializer):
    schedule_id = serializers.IntegerField()
    temperature = serializers.FloatField()
    pulse = serializers.CharField(max_length=10)
    upper_blood_pressure = serializers.FloatField()
    lower_blood_pressure = serializers.FloatField()
    oxygen_saturation = serializers.CharField(max_length=10)
    respiratory_rate = serializers.CharField(max_length=10)
    height = serializers.FloatField()
    weight = serializers.FloatField()
    engagement_doc = serializers.FileField()

    
    def create(self, validated_data):
        schedule: PatientSchedule

        try:
            schedule = PatientSchedule.objects.get(id=validated_data.get('schedule_id'))
            return PatientEngagement.objects.create(
                schedule=schedule,
                temperature=validated_data.get('temperature'),
                pulse=validated_data.get('pulse'),
                upper_blood_pressure=validated_data.get('upper_blood_pressure'),
                lower_blood_pressure=validated_data.get('lower_blood_pressure'),
                oxygen_saturation=validated_data.get('oxygen_saturation'),
                respiratory_rate=validated_data.get('respiratory_rate'),
                height=validated_data.get('height'),
                weight=validated_data.get('weight'),
                engagement_doc=validated_data.get('engagement_doc')
            )
        
        except PatientSchedule.DoesNotExist:
            raise CustomException(detail='Schedule does not exist', code=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            raise CustomException(detail=str(e))

    
    def update(self, instance, validated_data):
        pass