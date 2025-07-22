from rest_framework import routers # Routers allow you to quickly declare all of the common routes for a given 
#controller
from core.user.viewsets import UserViewSet
from core.auth.viewsets import RegisterViewSet, LoginViewSet, RefreshViewSet
from core.post.viewsets import PostViewSet
from core.comment.viewsets import CommentViewSet
from rest_framework_nested import routers#The Django ecosystem has a library called drf-nested-routers, which helps
#write routers to create nested resources in a Django project



router = routers.SimpleRouter() #Creates a simple DRF router that automatically maps URLs to your viewsets — 
#handling routes like list, retrieve, etc., without needing to define them manually.        

##############USER #############
router.register(r'user', UserViewSet, basename='user')




############Auth#################
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename= 'auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

#######POST ##########
router.register(r'post', PostViewSet, basename='post')
# Creates a nested route under 'post', so we can access related resources like /post/{post_id}/comments/

posts_router = routers.NestedSimpleRouter(router, r'post', lookup='post')

#routers.NestedSimpleRouter: A DRF extension (from drf-nested-routers) that allows you to create nested URLs 
# — useful when one resource belongs to another (like comments inside a post).router: The parent router
# (already defined earlier in your code). r'post': The base path for the nested route (e.g., /post/).
#lookup='post': The name used in the URL to refer to the parent object's ID. It will generate URLs like:
#/post/<post_id>/comments/

posts_router.register(r'comment', CommentViewSet, basename= 'post-comment')
# Registers the CommentViewSet under the nested post route
# This allows URLs like /post/{post_id}/comment/ to access comments for a specific post
#basename='post-comment': A unique name used by DRF for naming routes (used internally, like in reverse lookups
# or for linking in the API). r'comment': This adds the /comment/ sub-path under each post. So it creates URLs 
# like /post/1/comment/.
#posts_router: The nested router created earlier for the /post/ path.
urlpatterns =[
    *router.urls, # Includes all top-level routes like /post/, /user/, etc.
    *posts_router.urls # Includes all nested routes like /post/{post_id}/comment/
]



"""In Django REST Framework (DRF), a router automatically generates URL patterns for viewsets, saving you from 
writing them manually. SimpleRouter is a basic router that maps standard HTTP methods (GET, POST, PATCH, DELETE,
etc.) 
to the appropriate viewset actions like list(), retrieve(), create(), and so on.
r'user': The URL prefix (e.g., /user/, /user/<id>/).
UserViewSet: The viewset class that handles the logic for those routes.
basename='user': The name used to reverse URLs (e.g., user-list, user-detail).
urlpatterns = [ *router.urls ]injects all the auto-generated URLs from the router into your app’s urlpatterns,
so the viewset is 
fully wired to RESTful routes.  To register a route for a viewset, the register() method needs two arguments
The prefix: Representing the name of the endpoint, basically and
The viewset: Only representing a valid viewset class.
The basename argument is optional but it’s a good practice to use one, as it helps for readability and 
also helps Django for URL registry purposes.
"""
urlpatterns = [
    *router.urls
] # this should be at end