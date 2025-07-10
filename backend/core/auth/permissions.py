"""We want anonymous users to be able to read the posts on the API without necessarily being 
authenticated. While it’s true that there is the AllowAny permission, it’ll surely conflict with the 
IsAuthenticated permission. Thus, we need to write a custom permission"""

from rest_framework.permissions import BasePermission, SAFE_METHODS #BasePermission: A base class in DRF used to define custom permission logic.SAFE_METHODS: A tuple ('GET', 'HEAD', 'OPTIONS') representing HTTP methods that are read-only and considered safe.
                                                                    #These are typically used to write permissions that allow read-only access to unauthenticated users but restrict write actions
