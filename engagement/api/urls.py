from django.urls import path
from engagement.api import views

urlpatterns = [
    path('create-engagement/', views.create_engagement, name='create-engagement'),
    path('patient-engagements/', views.patient_engagement, name='patient-engagement')
]