from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializers import UserSerializer

class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(#This field links the author to a user using a human-readable field (public_id) instead of the default ID//SlugRelatedField lets you represent a related object (like author) using a specific field (the “slug”) instead of the default primary key (ID).
        queryset = User.objects.all(), # allows validation by ensuring the provided public_id matches an existing user.
        slug_field= 'public_id' #tells it to use the user's public_id for both input and output instead of id
        #It's useful in APIs to make input/output more readable and secure by exposing public_id instead of the internal user ID.
    )
#  SlugRelatedField  is used to represent the target of the relationship 
# using a field on the target. Thus, when creating a post, public_id of the author will be passed in 
# the body of the request so that the user can be identified and linked to the post.
    def validate_author(self, value):
        if self.context['request'].user != value:
            raise ValidationError("You can't create a post for another user") #context is a dictionary provided by the serializer that includes extra info — like the current request — passed by the view. value is the user instance passed as the author field during validation. So the method checks: “Is the logged-in user (request.user) the same as the author provided in the data?”
        return value
    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'edited', 'created', 'updated']
        read_only_fields = ["edited"]
        
    def to_representation(self, instance):#to_representation(self, instance) is a method provided by Django REST Framework in serializers.Serializer. It defines how a model instance is converted into a Python dict (i.e. the output format for API responses). You can override it to customize the serialized output.
                                            #returns a dictionary
        rep = super().to_representation(instance) #calls the parent class's implementation of to_representation() to get the default serialized data.
        author = User.objects.get_object_by_public_id(rep["author"]) #It fetches the User object from the database using the public_id stored in rep["author"].  get_object_by_public_id is a custom method in User model's manager that returns a user based on their public_id.
        rep["author"] = UserSerializer(author).data #replaces the author field in rep with this serialized user info (e.g., name, email, etc.) and serializes into JSON
        
        return rep
    
        
# The validate_author method checks validation for the author field. Here, we want to make 
# sure that the user creating the post is the same user as in the author field. A context dictionary is 
# available in every serializer. It usually contains the request object that we can use to make some checks.

    def update(self, instance, validated_data):   #This update method overrides the default to automatically mark a post as edited the first time it's updated. If instance.edited is False, it sets 'edited': True in the validated_data. Then it calls the parent class’s update() method with the modified data and returns the updated instance.
        if not instance.edited:
            validated_data['edited']= True
        instance = super().update(instance, validated_data)
        return instance
        

        