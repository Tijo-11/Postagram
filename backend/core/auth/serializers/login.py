from rest_framework_simplejwt.serializers import TokenObtainPairSerializer #built-in serializer in Simple JWT used to authenticate users and return both access and refresh tokens — typically used for login.
from rest_framework_simplejwt.settings import api_settings # gives access to all Simple JWT configuration options (like token lifetimes, auth header types, etc.) defined in your Django settings — useful if you need to reference or override them in custom logic.
from django.contrib.auth.models import update_last_login #update_last_login function, which updates the last_login field on the user model — commonly used after successful login to track when the user last authenticated.

from core.user.serializers import UserSerializer

class LoginSerializer(TokenObtainPairSerializer): # defines a custom login serializer by extending Simple JWT's TokenObtainPairSerializer, allowing you to customize the login behavior (e.g. modify the token response or add extra validations) while still leveraging JWT token generation.
    def validate(self, attrs):
        data = super().validate(attrs) #overrides the validate method to customize login behavior.It first calls the parent (super()) method to perform standard validation (like checking username/email and password), and returns the default JWT token data, which can then be modified or extended.
        
        refresh = self.get_token(self.user) #This generates a new refresh token (and access token) for the authenticated user (self.user) using Simple JWT's built-in method. The method get_token is a class method of TokenObtainPairSerializer. self.user is set during validation when authentication succeeds — it represents the currently logged-in user.
                                            #Passing it to get_token() tells Simple JWT to generate a token specifically for that user — tying the JWT to their identity.
        
        data['user'] = UserSerializer(self.user).data #This adds the serialized user info (like username, email, etc.) to the token response by converting the authenticated user (self.user) into a dictionary using UserSerializer.
                                                        #It lets the client receive both tokens and user details in the same response after login.
        data['refresh'] = str(refresh)   #This converts the refresh token object into a string and adds it to the response dictionary — making it JSON-serializable so it can be returned to the client.
                                            #refresh is the actual refresh token object. refresh can be used directly and safely converted to string:
        data['access'] = str(refresh.access_token) #refresh.access_token is a derived access token generated from that refresh token.refresh.access_token is an attribute, not a method — it's provided by the RefreshToken class to quickly get a valid access token tied to that refresh token:
        
        if api_settings.UPDATE_LAST_LOGIN: #UPDATE_LAST_LOGIN is a constant defined in Simple JWT’s default settings. It follows the convention of using all uppercase for config settings (like DEBUG, TOKEN_LIFETIME, etc.). This line checks if the setting is enabled, and if so, updates the user's last_login timestamp.
            update_last_login(None, self.user)
            
        return data #be wary of indentation, don't keep return inside if
        
        #You inherit from AbstractBaseUser, and this built-in Django class already includes the last_login field
            