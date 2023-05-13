from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from patient.api.serializers import PatientRegistrationSerializer
from patient.models import Patient

default_response: dict = {'statusCode': status.HTTP_400_BAD_REQUEST, 'message': None, 'data': None}


# Create your views here.
@api_view(['POST'])
def register_patient(request):
    if(request.method != 'POST'): return #
    response: dict = {}

    serializer = PatientRegistrationSerializer(data=request.data)

    if(serializer.is_valid()):
        serializer.save()

        response['statusCode'] = status.HTTP_201_CREATED
        response['message'] = 'Patient registration successful'
        response['data'] = serializer.data
    
    else:
        response['statusCode'] = status.HTTP_400_BAD_REQUEST
        response['message'] = 'Patient registration failed'
        response['errors'] = serializer.errors

    return Response(data=response, status=response['statusCode'])


@api_view(['GET'])
def get_patients(request):
    if(request.method != 'GET'): return #
    
    response: dict = {'statusCode': status.HTTP_400_BAD_REQUEST, 'data': []}
    patients = Patient.objects.all()

    try:
        serializer = PatientRegistrationSerializer(patients, many=True)
        response['statusCode'] = status.HTTP_200_OK
        response['data'] = serializer.data
    except:
        pass

    return Response(response, status=response['statusCode'])


@api_view(['GET'])
def get_patient_by_email(request):
    if(request.method != 'GET'): return #

    response: dict = {'statusCode': status.HTTP_404_NOT_FOUND, 'message': 'Not patient found', 'data': None}
    patient: Patient = None

    try:
        patient = Patient.objects.get(email=request.GET.get('email'))
        serializer = PatientRegistrationSerializer(patient)

        response['statusCode'] = status.HTTP_200_OK
        response['message'] = 'Patient found'
        response['data'] = serializer.data

    except Patient.DoesNotExist:
        pass

    return Response(response, status=response['statusCode'])


@api_view(['PUT'])
def update_patient(request):
    if(request.method != 'PUT'): return #

    response: dict = default_response
    patient: Patient = None

    try:
        patient = Patient.objects.get(email=request.GET.get('email'))

    except Patient.DoesNotExist:
        response['statusCode'] = status.HTTP_404_NOT_FOUND
        response['message'] = 'Patient not found'

    serializer = PatientRegistrationSerializer(patient)

    if(serializer.is_valid()):
        serializer.save()
        response['statusCode'] = status.HTTP_200_OK
        response['message'] = 'Patient details updated successfully!'
        response['data'] = serializer.data

    return Response(response, status=response['statusCode'])