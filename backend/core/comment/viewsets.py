from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import status

from core.abstract.viewsets import AbstractViewSet
from core.comment.models import Comment
from core.comment.serializers import CommentSerializer
from core.auth.permissions import UserPermission

class CommentViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes = UserPermission
    serializer_class = CommentSerializer
    
    
    def get_queryset(self):
        if self.request.user.is_superuser:
#request is an HTTP request object that contains all the information about the current API request,
#HTTP method (GET, POST, etc.)Data sent by the user,Headers,User making the request (after authentication)
#In a DRF view or serializer, self.request is available because DRF attaches it to the class when handling 
# the request. user os a property of the request object.
            return Comment.objects.all()
        
        post_pk = self.kwargs['post_pk']
# Get the 'post_pk' value from the URL — the ID of the parent post in a nested route like /post/<post_pk>/comment/
#post_pk = self.kwargs['post_pk']. kwargs (short for keyword arguments) are used to pass dynamic parts of the URL 
# into your view functions or classes.
        if post_pk is None:
            return Http404
        queryset = Comment.objects.filter (post__public_id = post_pk)
        
        return queryset
    
    
    def get_object(self):
        obj = Comment.objects.get_object_by_public_id(self.kwargs['pk']) #get_object_by_public_id is a method defined 
        #custom abstract model
        #self.kwargs['pk'] gets the value of the pk (primary key) from the URL.
        self.check_object_permissions(self.request, obj) #This method is provided by Django REST Framework (DRF).
        #It’s defined in the DRF class: rest_framework.views.APIViews
        #Since DRF ViewSets and APIViews inherit from APIView, they all get access to this method.
        #It calls all your configured object-level permission classes,
        #If the user does not have permission, it raises: PermissionDenied (HTTP 403)
        # Here, pk is represented by comment_pk. /api/post/post_pk/comment/comment_pk/
        return obj
# In Django REST Framework (DRF), the `create(self, request, *args, **kwargs)` method includes `request` as a
# parameter because DRF calls this method automatically when a POST request is made to the API. Since DRF is 
# handling the request, it passes the `request` object directly to `create()`, so you use it as a function argument.
# On the other hand, methods like `get_object(self)` are usually helper methods that you define and call yourself 
# inside the class. Because you're calling them internally, you don't need to pass `request` as an argument—instead,
# you can simply access it using `self.request`, which DRF has already made available on the class. So, in short: 
#  `create()` gets `request` as a parameter because DRF calls it for you, while `get_object()` uses `self.request`
#   because you call it yourself.

    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data= request.data)
#get_serializer() is a helper method provided by Django REST Framework that comes from the base classes like 
# GenericAPIView and ViewSet. This line creates a serializer instance using the data sent in the request 
# (e.g., from a form or JSON body). So instead of doing this manually: serializer = MySerializer(data=request.data)
#serializer = self.get_serializer(data=request.data) And DRF figures out which serializer to use.
#It's cleaner and more reusable. Works even if you're using different serializers in different actions.
#DRF handles passing extra context (like request, view, etc.) automatically.
        serializer.is_valid(raise_exception =True) #is_valid() is a Django REST Framework (DRF) method.
        self.perform_create(serializer)
#perform_create() is a hook method provided by Django REST Framework in views like CreateAPIView and ModelViewSet.
#When you call serializer.save(), you might want to add extra logic — like attaching the current user, modifying data,
# or triggering side effects. Instead of writing that logic directly in the create() method, DRF gives you a clean place 
# to do it: perform_create().
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        
            

            
    