from rest_framework import serializers
from core.user.models import User

class UserSerializer(serializers.ModelSerializer):#serializers.ModelSerializer is a Django REST Framework class that auto-generates serializer fields from a model — simplifying conversion between model instances and JSON.
    id = serializers.UUIDField(source='public_id', read_only= True, format='hex') #creates a serializer field id that pulls its value from the model's public_id field (source='public_id'), formats the UUID as a hex string (format='hex') for easy readability in JSON. 
    created = serializers.DateTimeField(read_only = True)
    updated = serializers.DateTimeField(read_only = True)
    
    class Meta: # an inner class used to configure behavior for Django or DRF classes — like linking a serializer to a model, setting fields, or defining model options
        model = User #tells the serializer to use the User model
        fields = ['id', 'username', 'first_name',
                  'last_name', 'bio', 'avatar', 'email',
                  'is_active', 'created', 'updated'] # include only the listed fields in the serialized output — controlling what data is exposed via the API.
        read_only_field = ['is_active',]