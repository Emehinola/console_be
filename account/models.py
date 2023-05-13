from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
    
class UserManager(BaseUserManager):
    
    def create_user(self, email, password, **kwargs):

        username = kwargs.get('username', None)

        if(username != None):
            if(ConsoleUser.objects.filter(username=username)).exists():
                raise ValueError('Username already taken')
        else:
            raise ValueError('Please provide a valid username')
        
        if not email:
            raise ValueError(_('The email must be set'))
                
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password, **kwargs):
        if not email:
            raise ValueError(_('The email must be set'))
        
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if (kwargs.get('is_staff')) is not True:
            raise ValueError(_('is_staff = True is False'))
        if (kwargs.get('is_superuser')) is not True:
            raise ValueError(_('is_superuser = True is False'))
        
        return self.create_user(email, password, **kwargs)
    
class ConsoleUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    nationality = models.CharField(max_length=50)
    ethnicity = models.CharField(max_length=50)
    religion = models.CharField(max_length=50) 
    lga = models.CharField(max_length=50)
    place_of_pry_ass = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    garrison = models.CharField(max_length=50)
    division = models.CharField(max_length=50)
    platoon = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)

    # permission/role
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()


    def __str__(self) -> str:
        return self.username
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)