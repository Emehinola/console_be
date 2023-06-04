from django.shortcuts import render

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
def patient_engagement(request):
    if request.method != 'GET': return #

    response: StandardResponseManager = StandardResponseManager()

    try:
        engagements = PatientEngagement.objects.all()
        serializer = PatientEngagementSerializer(engagements)

        response.data = serializer.data
        response.message = "Schedules fecthed successfully"
        response.statusCode = status.HTTP_200_OK

    except Exception as e:
        response.message = "Failed to fetch schedules"
        response.errors = f"Something went wrong: {e}"

    return Response(response.get_response(), status=response.statusCode)