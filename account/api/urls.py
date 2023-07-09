from django.urls import path
from account.api import views

urlpatterns = [
    path('login/', view=views.new_login, name='login'),
    path('create-account/', view=views.create_account, name='create-account'),
    path('update-account/', view=views.update_user, name='update-account'),
    path('get-user/', view=views.get_user, name='get-user'),
]