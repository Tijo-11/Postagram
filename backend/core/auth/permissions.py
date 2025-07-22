"""We want anonymous users to be able to read the posts on the API without necessarily being 
authenticated. While it’s true that there is the AllowAny permission, it’ll surely conflict with the 
IsAuthenticated permission. Thus, we need to write a custom permission"""

from rest_framework.permissions import BasePermission, SAFE_METHODS #BasePermission: A base class in DRF used to 
#define custom permission logic.SAFE_METHODS: A tuple ('GET', 'HEAD', 'OPTIONS') representing HTTP methods that 
# are read-only and considered safe.These are typically used to write permissions that allow read-only access 
# to unauthenticated users but restrict write actions

class UserPermission(BasePermission):
    
    def has_object_permission(self, request, view, obj): #It checks whether the current user (request.user) 
        #has permission to perform the action on the specific object (obj) being accessed, often used to enforce
        # per-object permissions like ownership.view refers to the DRF view (usually a ViewSet or APIView) that 
        # is handling the current request. It gives you access to the context of the request, including:view.
        # action (e.g., 'retrieve', 'update', 'destroy'),view.get_serializer_class(),view.queryset,view.kwargs, 
        # etc.You can use view to apply permission logic conditionally based on what the view is doing or which 
        # action is being performed.
        
        if request.user.is_anonymous:           #request is the HTTP request object that Django receives. 
            #request.user is automatically set by Django’s authentication middleware.
            return request.method in SAFE_METHODS #It represents the currently authenticated user making 
        #the request.If the user is not authenticated, request.user is set to an AnonymousUser object.
        
        if view.basename in ["post"]: #view.basename refers to the base name given to a viewset when 
            #registering it with a router. This checks if the current view (i.e., the one handling the request) has a base name of "post"
           
            return bool (request.user and request.user.is_authenticated) #This line checks if the request.user
        #exists and is authenticated, returning True only if the user is logged in
        
        #request.user.is_authenticated alone often works because Django assigns an AnonymousUser object to 
        # request.user when the user isn’t logged in, and that object still has the .is_authenticated attribute
        # (which returns False)This is extra-safe coding. request.user should always be present in a properly 
        # configured Django app. But in some edge cases — such as misconfigured middleware or non-authenticated 
        # views — request.user might be None. So adding request.user and avoids potential AttributeError if for 
        # some reason request.user is unexpectedly None.It's defensive programming. While 
        # request.user.is_authenticated is usually enough, including request.user and ensures the code doesn't
        # break in rare edge cases.
        
        return False
    
    def has_permission(self, request, view):#It checks general-level access before any specific object-level 
        #permissions. request: The incoming HTTP request (contains user, method, data, etc.).view: The view
        # being accessed (lets you customize permissions per view type).
#Used for Checking if a user can access the view at all (e.g., listing posts, creating a new one). 
# Unlike has_object_permission, this runs before the object is retrieved.
        
        if view.basename in ['post']: #Writing ['post'] as a list allows you to easily check multiple values 
            #using the in keyword:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS
            return bool(request.user and request.user.is_authenticated)
        return False
    
""" Django permissions usually work on two levels: on the overall endpoint (has_permission) and 
on an object level (has_object_permission).A great way to write permissions is to always deny by default; 
that is why we always return False 
at the end of each permission method. And then you can start adding the conditions. Here, in all the 
methods, we are checking that anonymous users can only make the SAFE_METHODS requests — 
GET, OPTIONS, and HEAD"""