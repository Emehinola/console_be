from django.urls import path
from engagement.api import views

urlpatterns = [
    path('create-engagement/', views.create_engagement, name='create-engagement'),
    path('patient-engagements/', views.get_all_engagements, name='patient-engagement'),
    path('get-engagement/<int:pk>/', views.get_engagement_by_id, name='get-engagement-by-id'),
    path('get-engagement-by-scheduleid/<int:schedule_id>/', views.get_engagement_by_schedule_id, name='engagement-by-schedule-id')
]