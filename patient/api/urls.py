from django.urls import path
from patient import views

urlpatterns = [
    path('register/', views.register_patient, name='register-patient'),
    path('all/', views.get_patients, name='get-patients'),
    path('get-patient/', views.get_patient_by_email, name='get-patient')
]