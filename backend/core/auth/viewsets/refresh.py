from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView # imports TokenRefreshView, a built-in view from Simple JWT that handles refreshing access tokens using a valid refresh token — typically used at the endpoint /api/token/refresh/.
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import viewsets #This imports DRF's viewsets module, which provides powerful classes like 
#ModelViewSet that bundle common logic for CRUD operations (create, retrieve, update, delete) into a single view.
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class RefreshViewSet(viewsets.ViewSet, TokenRefreshView): #viewsets.ViewSet is used to make it compatible 
    #with DRF's router system and organize token-refresh functionality inside a class-based view structure.
    permission_classes =(AllowAny,)
    http_method_names = ['post']
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) #get_serializer is not a method of the serializer 
        #class — it's a method provided by Django REST Framework’s view or viewset class.
        try:
            serializer.is_valid(raise_exception= True)
        except TokenError as e:
            raise InvalidToken
        return Response (serializer.validated_data, status= status.HTTP_200_OK)

