from rest_framework import serializers
from api.models import ConsoleUser

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = ConsoleUser
        fields = '__all__' # include all fields

    def get_full_name(self, userObj):
        return f'{userObj.firstName} {userObj.lastName}'