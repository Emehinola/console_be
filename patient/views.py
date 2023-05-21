from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from api.custom_pagination import CustomPagination
from api.response_manager import StandardResponseManager

from console_be.settings import HOST
from patient.api.serializers import PatientSerializer, PatientScheduleSerializer
from patient.models import Patient, PatientSchedule


default_response: dict = {'statusCode': status.HTTP_400_BAD_REQUEST, 'message': None, 'data': None}


# Create your views here.
@api_view(['POST'])
@parser_classes([MultiPartParser])
def register_patient(request):

    if(request.method != 'POST'): return #
    
    response: StandardResponseManager = StandardResponseManager()

    data = request.data
    data['image'] = request.FILES.get('image')

    serializer = PatientSerializer(data=request.data)

    try:
        if(serializer.is_valid()):
            serializer.save()

            response.statusCode = status.HTTP_201_CREATED
            response.message = 'Patient registration successful'
            response.data = serializer.data
    
        else:
            response.message = 'Patient registration failed'
            response.errors = serializer.errors
    
    except Exception as error:
        response.errors = str(error)

    return Response(data=response.get_response(), status=response.statusCode)


@api_view(['GET'])
def get_patients(request):

    if(request.method != 'GET'): return #

    paginator = CustomPagination()
    
    response: dict = {'statusCode': status.HTTP_400_BAD_REQUEST, 'data': []}
    patients = Patient.objects.all()

    try:
        paginated_patients = paginator.paginate_queryset(patients, request=request)

        serializer = PatientSerializer(paginated_patients, many=True)
        response['statusCode'] = status.HTTP_200_OK
        response['data'] = serializer.data

    except:
        pass

    return paginator.get_paginated_response(response, statusCode=response['statusCode'])


@api_view(['GET'])
def get_patient_by_email(request):
    
    if(request.method != 'GET'): return #

    response: dict = {'statusCode': status.HTTP_404_NOT_FOUND, 'message': 'Not patient found', 'data': None}
    patient: Patient = None

    try:
        patient = Patient.objects.get(email=request.GET.get('email'))
        serializer = PatientSerializer(patient)

        response['statusCode'] = status.HTTP_200_OK
        response['message'] = 'Patient found'
        response['data'] = serializer.data

    except Patient.DoesNotExist:
        pass

    return Response(response, status=response['statusCode'])


@api_view(['PUT'])
def update_patient(request):
    if(request.method != 'PUT'): return #

    response: StandardResponseManager = StandardResponseManager()
    patient: Patient = None

    try:
        patient = Patient.objects.get(email=request.data.get('email'))

        serializer = PatientSerializer(patient, data=request.data)

        if(serializer.is_valid()):
            serializer.save()

            response.statusCode = status.HTTP_200_OK
            response.message = 'Patient details updated successfully!'
            response.data = serializer.data

        else:
            response.statusCode = status.HTTP_400_BAD_REQUEST
            response.message = 'Unable to update patient'
            response.errors = serializer.errors

    except Patient.DoesNotExist:
        response.statusCode = status.HTTP_404_NOT_FOUND
        response.message = 'Patient not found'
        response.errors = 'Patient not found'

    except Exception as e:
        response.statusCode = status.HTTP_400_BAD_REQUEST
        response.message = str(e)


    return Response(response.get_response(), status=response.statusCode)


@api_view(['DELETE'])
def delete_patient(request):

    if(request.method != 'DELETE'): return #
    
    response: StandardResponseManager = StandardResponseManager()
    patient: Patient = None

    try:
        patient = Patient.objects.get(email=request.data['email'])
        patient.delete()

        response.statusCode = status.HTTP_200_OK
        response.message = 'Patient deleted successfully'

    except Patient.DoesNotExist:
        response.statusCode = status.HTTP_404_NOT_FOUND
        response.message = 'Patient not found'
        response.errors = response.message

    return Response(response.get_response(), status=response.statusCode)


""" PATIENT SCHEDULES VIEWS """

@api_view(['POST'])
def create_appointment(request):
    if(request.method != 'POST'): return #

    response: StandardResponseManager = StandardResponseManager(message = "Falied to create appointment")
    patient: Patient = None

    try:
        patient = Patient.objects.get(email=request.data['patient_email'])

        request.data['patient'] = patient.id
        serializer = PatientScheduleSerializer(data=request.data)

        if(serializer.is_valid(patient=patient)):
            serializer.save()

            response.statusCode = status.HTTP_201_CREATED
            response.message = "Appointment created successfully"
            
        else:
            response.statusCode = status.HTTP_400_BAD_REQUEST
            response.errors = serializer.errors

    except Patient.DoesNotExist:
        response.errors = "Patient does not exist"

    except Exception as e:
        response.errors = str(e)
    

    return Response(response.get_response(), status=response.statusCode)

    


@api_view(['GET'])
def get_appointments(request):
    if(request.method != 'GET'): return #

    response: StandardResponseManager = StandardResponseManager()
    patients = []

    try:
        patients = PatientSchedule.objects.all()
        serializer = PatientScheduleSerializer(patients, many=True)

        response.data = serializer.data
        response.message = "Patient schedules fetched successfully"
        response.statusCode = status.HTTP_200_OK

    except:
        response.errors = "Unable to fetch schedules"
        response.message = "Unable to fetch schedules"

    return Response(response.get_response(), status=response.statusCode)



@api_view(['GET'])
def get_patient_appointment(request):
    if(request.method != 'GET'): return #

    response: StandardResponseManager = StandardResponseManager()
    schedule: PatientSchedule = None
    patient: Patient = None

    try:
        patient = Patient.objects.get(email=request.data['email'])
        schedule = PatientSchedule.objects.get(patient=patient)
        serializer = PatientScheduleSerializer(schedule)

        response.data = serializer.data
        response.message = "Patient schedule fetched successfully"
        response.statusCode = status.HTTP_200_OK

    except PatientSchedule.DoesNotExist:
        response.errors = "Schedule not found"
        response.message = "Schedule not found"
        response.statusCode = status.HTTP_404_NOT_FOUND

    except Patient.DoesNotExist:
        response.errors = "Patient not found"
        response.message = "Patient not found"
        response.statusCode = status.HTTP_404_NOT_FOUND

    except:
        response.errors = "Unable to fetch schedule"
        response.message = "Unable to fetch schedule"

    return Response(response.get_response(), status=response.statusCode)
