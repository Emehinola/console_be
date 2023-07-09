from rest_framework import status
from rest_framework.response import Response

class StandardResponseManager:

    statusCode: str
    message: str
    data: dict
    errors: any

    def __init__(self, statusCode=status.HTTP_400_BAD_REQUEST, message=None, data=None, errors=None):

        # instantiating
        self.statusCode = statusCode
        self.message = message
        self.data = data
        self.errors = errors

    def get_response(self):
        return {
            'statusCode': self.statusCode,
            'errors': self.errors,
            'message': self.message,
            'data': self.data
        } # returns response
    
    
    @classmethod
    def not_found(self, message="Not found"):
        return Response({"status_code": status.HTTP_404_NOT_FOUND, "error": message, "data": None}, status=status.HTTP_404_NOT_FOUND)