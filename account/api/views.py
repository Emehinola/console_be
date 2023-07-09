from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from rest_framework_simplejwt.models import TokenUser

from django.contrib.auth.hashers import make_password

from django.urls import reverse

import requests

from console_be import settings
from . import serializers as acctSerializer
from ..models import ConsoleUser



# from users import serializers
# class CustomTokenObtainPairView(TokenObtainPairView):
#     # Replace the serializer with your custom
#     serializer_class = serializers.CustomTokenObtainPairSerializer


@api_view(['POST']) # post request
def create_account(request):
    if(request.method != 'POST'): return

    response_data: dict = {}
    request.data['password'] = make_password(request.data["password"]) # hash password

    serializer = acctSerializer.UserSerializer(data=request.data)

    if(serializer.is_valid()):
       serializer.save()

       response_data['statusCode'] = status.HTTP_201_CREATED
       response_data['success'] = True
       response_data['responseMessage'] = 'Account created successfully!'
       response_data['data'] = request.data

       return Response(response_data, status=status.HTTP_201_CREATED)

    else:
        response_data = serializer.errors

    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_request(request):
    data: dict = {}
    response = None
    url: str = settings.HOST + reverse('get_token')

    payload = {
        'email': request.POST.get('email'),
        'password': request.POST.get('password')
    }

    try:
        response = requests.post(url=url, data=payload)
    except:
        return Response(data={'error': 'Unknown error occurred'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    data['statusCode'] = response.status_code
    if(response.status_code == 200):
        data['message'] = 'Login successful!'
        data['accessToken'] = response.json()['access']
        data['refreshToken'] = response.json()['refresh']
    else:
        data['message'] = 'Incorrect username or password'

    return Response(data=data, status=response.status_code)


@api_view(['POST'])
def new_login(request):
    
    data: dict = {}

    try:
        user = ConsoleUser.objects.get(email=request.POST.get('email'))
    except ConsoleUser.DoesNotExist:
        data['status_code'] = status.HTTP_401_UNAUTHORIZED
        data['message'] = 'Incorrect username or password'

        return Response(data=data, status=data['status_code'])
            
    if(user.check_password(request.POST.get('password'))):
        token = get_token(user) 
        
        if(token != None):
            data['status_code'] = status.HTTP_200_OK
            data['message'] = 'Login successful!'
            data['access_token'] = token['access_token']
            data['refresh_token'] = token['refresh_token']
        
    else:
        data['status_code'] = status.HTTP_401_UNAUTHORIZED
        data['message'] = 'Incorrect username or password'

    return Response(data=data, status=data['status_code'])


# get token
def get_token(user: ConsoleUser):
    try:
        refresh = RefreshToken.for_user(user)

        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

    except:
        return None
    


@api_view(['GET'])
def get_user(request):
    token_str = request.META.get('HTTP_AUTHORIZATION', None)

    if(token_str == None): return Response(data={'error': 'Token is required'})

    if(request.method != 'GET'): return #
    user_id = None
    token = None

    try:
        token = AccessToken(token_str)
    except:
        return Response(data={'error': 'Token is invalid or expired!'})
    
    user_id = token['user_id']
    
    try:
        user = ConsoleUser.objects.get(id=user_id)
    except ConsoleUser.DoesNotExist:
        return Response(data={'error': 'User does not exist!'})

    serialiser = acctSerializer.UserSerializer(user)

    return Response(serialiser.data)


@api_view(['PUT'])
def update_user(request):
    if(request.method != 'PUT'): return #
    response_obj = {}
    user = None
    
    try:
        user = ConsoleUser.objects.get(id=request.data.get('id'))
    except ConsoleUser.DoesNotExist:
        return Response({'error': 'User does not exist'})
    
    serializer = acctSerializer.UpdateUserSerializer(user, data=request.data)

    if(serializer.is_valid()):
        serializer.save()

        response_obj['status'] = status.HTTP_200_OK
        response_obj['message'] = 'Account updated successfully'
        response_obj['data'] = serializer.data

    else:
        return Response(serializer.errors)


    return Response(data=response_obj)



class UserCustomView:

    @api_view(['POST'])
    def create_account(request):
        pass

    @api_view(['POST'])
    def login(request):
        pass

    @api_view(['POST'])
    def logout(request):
        pass

    @api_view(['GET'])
    def get_user(request, pk=None):
        pass

    @api_view(['POST'])
    def validate_email(request):
        pass

    @api_view(['POST'])
    def forgot_password(request):
        pass
