from rest_framework import status

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
            'message': self.message,
            'data': self.data,
            'errors': self.errors
        } # returns response