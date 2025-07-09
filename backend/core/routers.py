from rest_framework import routers # Routers allow you to quickly declare all of the common routes for a given controller
from core.user.viewsets import UserViewSet
from core.auth.viewsets import RegisterViewSet, LoginViewSet, RefreshViewSet



router = routers.SimpleRouter() #Creates a simple DRF router that automatically maps URLs to your viewsets — handling routes like list, retrieve, etc., without needing to define them manually.        

##############USER #############
router.register(r'user', UserViewSet, basename='user')




############Auth#################
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename= 'auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')


"""In Django REST Framework (DRF), a router automatically generates URL patterns for viewsets, saving you from 
writing them manually. SimpleRouter is a basic router that maps standard HTTP methods (GET, POST, PATCH, DELETE, etc.) 
to the appropriate viewset actions like list(), retrieve(), create(), and so on.
r'user': The URL prefix (e.g., /user/, /user/<id>/).
UserViewSet: The viewset class that handles the logic for those routes.
basename='user': The name used to reverse URLs (e.g., user-list, user-detail).
urlpatterns = [ *router.urls ]injects all the auto-generated URLs from the router into your app’s urlpatterns, so the viewset is 
fully wired to RESTful routes.  To register a route for a viewset, the register() method needs two arguments
The prefix: Representing the name of the endpoint, basically and
The viewset: Only representing a valid viewset class.
The basename argument is optional but it’s a good practice to use one, as it helps for readability and 
also helps Django for URL registry purposes.
"""
urlpatterns = [
    *router.urls
] # this should be at end