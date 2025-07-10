from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
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

""""
| **HTTP Method** | **URL Pattern** | **Action** | **ViewSet Method** | **Description**                     |
| --------------- | --------------- | ---------- | ------------------ | ----------------------------------- |
| `GET`           | `/post/`        | `list`     | `get_queryset()`   | List all posts                      |
| `POST`          | `/post/`        | `create`   | `create()`         | Create a new post                   |
| `GET`           | `/post/{pk}/`   | `retrieve` | `get_object()`     | Retrieve a single post by public ID |
"""
    
    
"""
## ✅ Common ViewSet Methods and What They Do
| Method                                   | What It Does                                                     |
| ---------------------------------------- | ---------------------------------------------------------------- |
| `create(self, request)`                  | Handles **POST** requests to create a new object.                |
| `update(self, request, pk=None)`         | Handles **PUT** requests for full updates (all fields required). |
| `partial_update(self, request, pk=None)` | Handles **PATCH** requests for partial updates.                  |
| `list(self, request)`                    | Handles **GET** requests to list all objects.                    |
| `retrieve(self, request, pk=None)`       | Handles **GET /posts/{id}/** to retrieve one object.             |
| `destroy(self, request, pk=None)`        | Handles **DELETE /posts/{id}/** to delete an object.             |
| `get_queryset(self)`                     | Tells DRF which queryset to use.                                 |
| `get_object(self)`                       | Tells DRF how to retrieve a single object.                       |
| `perform_create(self, serializer)`       | Optional hook: customize saving during create.                   |
| `perform_update(self, serializer)`       | Optional hook: customize saving during update.                   |


> If you don’t define some of these, DRF will use default behavior — but you can override them to customize.

A **ViewSet** is like a toolbox of actions related to one type of object — for example, *posts*.

Instead of writing a different view (function or class) for every action like *create a post*, *edit a post*, *get a post*, etc., you put all of those into one ViewSet. It helps you organize your code and saves you from repeating things.

### 2. **What is a Router?**

In Django, **URLs** determine what gets called when someone visits a specific path — like `/post/` or `/post/1/`.

In DRF, you use a **router** to automatically create all those URL patterns for a ViewSet. You register your ViewSet like this:


router.register(r'post', PostViewSet, basename='post')


That tells Django:

> "Please create all necessary URLs for managing posts using the methods in `PostViewSet`."
**Summary: What’s Happening Overall**

* You write a `PostViewSet` class with all the logic for handling posts.
* You register it with a router using `router.register()`.
* The router creates all the needed URLs and maps them to the methods in your ViewSet.
* When someone visits `/post/` or `/post/123/`, Django knows exactly what method to run (`create`, `update`, etc.).
"""