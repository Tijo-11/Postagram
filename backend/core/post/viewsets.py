from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action 
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerializer
from core.auth.permissions import UserPermission

#methods for deletion (destroy()), and updating  (update()) are already available by default in the ViewSet class

class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'put', 'delete', 'patch')
    permission_classes = (UserPermission,)
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication] #Your viewset uses permission_classes = (IsAuthenticated,), which requires a valid authenticated user. If authentication fails (due to the wrong authentication classes), DRF returns the "Authentication credentials were not provided." error.
    #you’re likely using a token-based authentication system like rest_framework_simplejwt or DRF’s TokenAuthentication. These require JWTAuthentication or TokenAuthentication in your authentication_classes, not SessionAuthentication or BasicAuthentication.

    def get_queryset(self):
        return Post.objects.all() #Django ORM (Object-Relational Mapper) query that retrieves all rows from the Post table as Python objects.
    
    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk']) #self.kwargs is a dictionary of URL parameters captured by Django’s router/view.'pk' is usually the primary key or public ID passed in the URL (like /posts/<pk>/).
                            #self.kwargs['pk'] extracts that value and passes it to the custom method. kwargs helps access dynamic values from the URL.
        self.check_object_permissions(self.request,obj) #method from Django REST Framework's ViewSet that Checks if the current user has permission to interact with a specific object (obj), Uses your defined permission_classes (like IsOwner, IsAdminUser, etc.) Raises a PermissionDenied error (403) if the user isn’t allowed access
                                                        #In short: it enforces object-level permission checks.
        return obj #if the user has permission, the object is returned; otherwise, a PermissionDenied error is raised
    
    def create(self, request, *args, **kwargs): #*args and **kwargs allow the method to accept extra positional and keyword arguments, ensuring compatibility with parent class methods
        serializer = self.get_serializer(data= request.data) # self.get_serializer method in Django REST Framework's ViewSet that returns an instance of the serializer class associated with the view, optionally populated with data, context, or arguments.
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) #self.perform_create is a method in Django REST Framework used to handle the actual saving logic when creating an object—typically called after serializer validation in create()
        return Response( serializer.data, status= status.HTTP_201_CREATED)
    
#URL Patterns Generated

# 
# | **HTTP Method** | **URL Pattern** | **Action** | **ViewSet Method** | **Description**                     |
# | --------------- | --------------- | ---------- | ------------------ | ----------------------------------- |
# | `GET`           | `/post/`        | `list`     | `get_queryset()`   | List all posts                      |
# | `POST`          | `/post/`        | `create`   | `create()`         | Create a new post                   |
# | `GET`           | `/post/{pk}/`   | `retrieve` | `get_object()`     | Retrieve a single post by public ID |

#  DRF provides a decorator called action. This decorator helps make methods on a ViewSet class 
# routable. The action decorator takes two arguments:
#  • detail: If this argument is set to True, the route to this action will require a resource lookup 
# field; in most cases, this will be the ID of the resource
#  • methods: This is a list of the methods accepted by the action
    @action(methods=['post'], detail= True) #this creates a POST endpoint for a specific object (detail=True means it acts on a single instance, not a list).
    def like(self, request, *args, **kwargs): #handles a request to like a specific object, with arguments passed from the URL and router.
        #*args and **kwargs are flexible arguments automatically passed by Django/DRF — kwargs often includes the object’s ID (e.g., pk).
        post = self.get_object() #Retrieves the object (e.g., a Post) that this view is acting on, using the ID from the URL; provided by DRF's GenericViewSet or ModelViewSet.
        #self.get_object() is a built-in DRF method It uses the lookup field (e.g., pk, slug, or public_id) from the URL to fetch the object from the database.
        user = self.request.user() #request.user  Refers to the currently authenticated user making the request; available through Django’s authentication system.
        
        user.like(post) #calling a custom method named like() defined on the User model
        serializer = self.serializer_class(post)  # Creates a serializer instance using the given post object to prepare it for JSON response (read-only by default).
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        post= self.get_object()
        user = self.request.user()
        user.remove_like(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status = status.HTTP_200_OK)
# The self.get_object() method will automatically return the concerned post using the 
# ID passed to the URL request, thanks to the detail attribute being set to True.
#  we also retrieve the user making the request from the self.request object. This 
# is done so that we can call the remove_like or like method added to the User model.
#Like a post with the following endpoint: api/post/post_pk/like/.
#Remove the like from a post with the following endpoint: api/post/post_pk/remove_like/
        