from rest_framework.response import Response #This imports DRF's Response class, which is used to return 
#structured HTTP responses (like JSON) from API views, along with status codes and headers.
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rest_framework import status #This imports HTTP status codes 
from rest_framework_simplejwt.tokens import RefreshToken # allows you to manually generate access and 
#refresh tokens for a user — typically used after login or account creation.
from core.auth.serializers import RegisterSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class RegisterViewSet(ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    def create(self, request, *args, **kwargs):
        # *args: Collects positional arguments as a tuple., **kwargs: Collects keyword arguments as a dictionary
        # They're included to support flexibility — letting Django REST Framework pass extra parameters 
        # (like view-specific options or 
        # routing details) without causing errors. Even if you don't use them directly, including them ensures 
        # compatibility with the DRF base class you're overriding
        serializer = self.serializer_class(data=request.data) #creates a serializer instance using incoming 
        #request data (request.data) — preparing it for validation and object creation or update.
        serializer.is_valid(raise_exception= True)#This validates the incoming data; if invalid, it automatically
        #raises a 400 Bad Request with error details —
        user = serializer.save() #This creates and saves a new user instance using the validated data from the 
        #serializer — calling its create() or update() method under the hood.
        refresh = RefreshToken.for_user(user) #Generates a new refresh token (and linked access token) for 
        #the given user
        
        res = { #This creates a response dictionary res containing:
            "refresh": str(refresh), #the refresh token as a string (used to get new access tokens)
            "access" :str(refresh.access_token),#the access token as a string (used to authenticate API
            #requests)
        }
        return Response({
            "user":serializer.data, #This includes the serialized user data (like username, email, etc.) in 
            #the API response — it's the newly created or logged-in user's details, structured as JSON.password will not appear in the serialized response (serializer.data), because it's write-only.
            "refresh":res["refresh"],
            "access": res["access"],
        }, status= status.HTTP_201_CREATED)
        

        
    


