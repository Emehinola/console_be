from rest_framework.exceptions import PermissionDenied
from rest_framework import status

class CustomException(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'Invalid'
    default_detail = 'An unknown error occurred'


    def __init__(self, detail=None, code=None):
        self.detail = detail

        if(code is not None):
            self.status_code = code
            
        # super().__init__(detail, code)