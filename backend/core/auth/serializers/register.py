from rest_framework import serializers
from core.user.serializers import UserSerializer
from core.user.models import User

class RegisterSerializer(UserSerializer):
    """
    Registration serializer for requests and user creation.
    Making sure the password is at least 8 characters
       long, and no longer than 128 and can't be read by the user
    """
    password = serializers.CharField(max_length= 128, min_length=8, write_only = True, required =True)
    class Meta:#an inner class used to configure behavior for Django or DRF classes — like linking a serializer to a model, setting fields, or defining model options
        model = User
         # List of all the fields that can be included in a request or a response
        fields= ['id', 'bio', 'avatar', 'email',
                 'username', 'first_name', 'last_name','password']
    
    def create(self, validated_data):#validated_data is a dictionary of cleaned, validated input data provided by the serializer after calling .is_valid()
        # Use the `create_user` method  wrote earlier for the UserManager to create a new user.
        return User.objects.create_user(**validated_data)
    
    #RegisterSerializer is a subclass of UserSerializer. as we don’t need to rewrite fields again.
    # Here, we don’t need to revalidate fields such as email or password. As we declared these fields 
    #with some conditions, Django will automatically handle their validation.
        