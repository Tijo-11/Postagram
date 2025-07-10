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
    