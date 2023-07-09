from rest_framework import serializers
from ..models import ConsoleUser
from django.db.models import Q


# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     """Customizes JWT default Serializer to add more information about user"""
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['name'] = user.name
#         token['email'] = user.email
#         token['is_superuser'] = user.is_superuser
#         token['is_staff'] = user.is_staff

#         return token


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    # email = serializers.EmailField(read_only=True)

    class Meta:
        model = ConsoleUser
        exclude = ['is_staff', 'is_active', 'is_superuser']
        # fields = '__all__' # include all fields
    

    def validate(self, data):
        
        queryset = ConsoleUser.objects.filter(Q(email=data['email']) | Q(username=data['username']))

        if (queryset.exists()): # id != None for update
            raise serializers.ValidationError('Email/username already taken')

        if (len(data['password']) < 8): raise serializers.ValidationError('Password must be atleast 8 character long')
        
        return data
        
        
    def get_full_name(self, userObj):
        return f'{userObj.first_name} {userObj.last_name}'
    

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsoleUser
        exclude = ['password', 'is_staff', 'is_active', 'is_superuser']

    def update(self, instance, validated_data):
        
        # optional implementation
        if not ConsoleUser.objects.filter(id=instance.id).exists():
            raise serializers.ValidationError('User does not exist')
        
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.phone = validated_data['phone']
        instance.nationality = validated_data['nationality']
        instance.ethnicity = validated_data['ethnicity']
        instance.lga = validated_data['lga']
        instance.religion = validated_data['religion']
        instance.place_of_pry_ass = validated_data['place_of_pry_ass']
        instance.rank = validated_data['rank']
        instance.position = validated_data['position']
        instance.garrison = validated_data['garrison']
        instance.division = validated_data['division']
        instance.platoon = validated_data['platoon']
        instance.unit = validated_data['unit']

        instance.save()

        return instance
    