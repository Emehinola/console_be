from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from django.urls import reverse

import requests

from console_be import settings
from . import serializers as acctSerializer
from ..models import ConsoleUser


@api_view(['POST']) # post request
def create_account(request):
    if(request.method != 'POST'): return

    response_data: dict = {}

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
        data['refreshTken'] = response.json()['refresh']
    else:
        data['message'] = 'Incorrect username or password'

    return Response(data=data, status=response.status_code)


@api_view(['GET'])
def get_user(request):
    token_str = request.META.get('HTTP_AUTHORIZATION', None)

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