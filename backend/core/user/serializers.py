from rest_framework import serializers
from core.user.models import User
from core.abstract.serializers import AbstractSerializer

class UserSerializer(AbstractSerializer):
    
    class Meta: # an inner class used to configure behavior for Django or DRF classes — like linking a serializer to a model, setting fields, or defining model options
        model = User #tells the serializer to use the User model
        fields = ['id', 'username', 'first_name',
                  'last_name', 'bio', 'avatar', 'email',
                  'is_active', 'created', 'updated'] # include only the listed fields in the serialized output — controlling what data is exposed via the API.
        read_only_field = ['is_active',]