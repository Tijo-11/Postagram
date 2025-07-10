from rest_framework.response import Response #This imports DRF's Response class, which is used to return structured HTTP responses (like JSON) from API views, along with status codes and headers.
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken #TokenError: A general error for problems with JWTs (e.g., malformed, expired, blacklisted). InvalidToken: A specific subclass of TokenError raised when a token fails validation (e.g., wrong signature, tampering, etc.).
                        #These are useful when customizing authentication flows or handling token-related errors in views or serializers.
from core.auth.serializers import LoginSerializer

class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer #r tells the view or viewset which serializer to use for processing input and formatting output
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    authentication_classes = [SessionAuthentication, BasicAuthentication] #This line tells Django REST Framework to use Session and Basic authentication for the view or viewset — allowing login via Django sessions (for browsers) or basic HTTP credentials (for tools like Postman).
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        
        try:
            serializer.is_valid(raise_exception= True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) #raises an InvalidToken exception using the first argument from a caught error e, passing along the error message to explain why the token is invalid.
        return Response(serializer.validated_data, status=status.HTTP_200_OK)   
    
    
"""authentication is the action of verifying the identity of a user, authorization is simply the action of 
checking whether the user has the rights or privileges to perform an action."""
    