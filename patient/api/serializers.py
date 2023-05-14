from rest_framework import serializers
from patient.models import Patient

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