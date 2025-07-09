from rest_framework import viewsets
from rest_framework import filters #This imports Django REST Framework’s built-in filtering classes (like SearchFilter, OrderingFilter) to enable features like search and ordering in your API views or viewsets.

class AbstractViewSet(viewsets.ModelViewSet): #This defines a reusable base viewset by extending ModelViewSet, which bundles common CRUD operations (list, create, retrieve, update, delete) into a single class — useful for shared behavior across multiple viewsets.
    filter_backends = [filters.OrderingFilter] #enables sorting of API results by specified fields using the ?ordering= query parameter (e.g., ?ordering=created or ?ordering=-username).
    ordering_fields = ['updated', 'created']
    ordering = ['-updated'] #sets the default sort order of query results to descending by the updated field (most recently updated items first).