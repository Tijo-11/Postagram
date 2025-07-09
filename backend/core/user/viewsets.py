from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from core.abstract.viewsets import AbstractViewSet

from core.user.serializers import UserSerializer
from core.user.models import User

class UserViewSet(AbstractViewSet): # viewsets.ModelViewSet is a Django REST Framework class that provides default CRUD operations (list, create, retrieve, update, delete) for a model — all in one place.
    http_method_names = ('patch', 'get') #This restricts the viewset to accept only GET (read) and PATCH (partial update) HTTP methods — blocking others like POST, PUT, DELETE.
    permission_classes = (IsAuthenticated) #This allows any user, authenticated or not, to access the view — no permission checks are enforced.
    serializer_class = UserSerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:#is_superuser is the actual attribute name of the User model in Django
            return User.objects.all()
        return User.objects.exclude(is_superuser =True) #Returns all users except superusers by filtering out records where is_superuser is True
    
    def get_object(self):
        obj= User.objects.get_object_by_public_id(self.kwargs['pk'])#kwargs holds the URL parameters captured by the view (e.g., from /users/<pk>/). So self.kwargs['pk'] fetches the value of pk from the URL. pk stands for primary key — typically the unique ID of a model instance (like id or public_id)
        self.check_object_permissions(self.request, obj)  #checks if the current user (self.request.user) has permission to access the given object (obj) — raises a 403 error if not allowed.
        return obj
    