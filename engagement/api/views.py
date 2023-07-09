from django.shortcuts import render, get_object_or_404

from patient.models import Patient, PatientSchedule

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser

from api.response_manager import StandardResponseManager
from .serializer import PatientEngagementSerializer

from .models import PatientEngagement


@api_view(['POST'])
@parser_classes([MultiPartParser])
def create_engagement(request):
    if request.method != 'POST': return #
    response = StandardResponseManager()

    try:
        request.data['engagement_doc'] = request.FILES.get('engagement_doc') # set file
        serializer = PatientEngagementSerializer(data=request.data)

        if(serializer.is_valid()):
            serializer.save()

            response.message = "Engagement created successfully"
            response.statusCode = status.HTTP_200_OK
        
        else:
            response.errors = serializer.errors
            response.message = "Failed to create engagement"

    except Exception as e:
        response.errors = str(e)
        response.message = "Failed to create engagement"

    return Response(response.get_response(), status=response.statusCode)



@api_view(['GET'])
def get_all_engagements(request):
    if request.method != 'GET': return #

    response: StandardResponseManager = StandardResponseManager()

    try:
        engagements = PatientEngagement.objects.all()
        serializer = PatientEngagementSerializer(engagements, many=True)

        response.data = serializer.data
        response.message = "Schedules fecthed successfully"
        response.statusCode = status.HTTP_200_OK

    except Exception as e:
        response.message = "Failed to fetch schedules"
        response.errors = f"Something went wrong: {e}"

    return Response(response.get_response(), status=response.statusCode)


@api_view(['GET'])
def get_engagement_by_id(request, pk=None):

    if(request.method != 'GET'): return #
    
    try:
        engagement = PatientEngagement.objects.get(pk=pk)
    except:
        return StandardResponseManager.not_found()
    
    serializer = PatientEngagementSerializer(engagement)
    response = StandardResponseManager(
            message='Engagments fetched successfully', 
            statusCode=status.HTTP_200_OK, 
            data=serializer.data
        )

    return Response(response.get_response(), status=response.statusCode)




@api_view(['GET'])
def get_engagement_by_schedule_id(request, schedule_id=None):
    # pk = patient id

    if(request.method != 'GET'): return #

    schedule: PatientSchedule = None
    engagement: PatientEngagement = None

    try:
        schedule = PatientSchedule.objects.get(id=schedule_id)
        engagement = PatientEngagement.objects.get(schedule=schedule)

        serializer = PatientEngagementSerializer(engagement)

        response = StandardResponseManager(
            message='Engagement fetched successfully', 
            statusCode=status.HTTP_200_OK, 
            data=serializer.data
        )

        return Response(response.get_response(), status=status.HTTP_200_OK)

    except PatientSchedule.DoesNotExist:
        return StandardResponseManager.not_found(message="Schedule with this id does not exist")
    
    except PatientEngagement.DoesNotExist:
        return StandardResponseManager.not_found(message="Engagement not found")

