from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.user.models import User
from core.user.serializers import UserSerializer
from core.comment.models import Comment
from core.post.models import Post

class CommentSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(queryset= User.objects.all(), slug_field= 'public_id',)
#SlugRelatedField is used when you want to represent a related object #using a readable field (like a username,
# slug, or in this case public_id) instead of its database ID.input: It will accept "public_id" as the value.
# Output: It will show "public_id" instead of the full user object. queryset= User.objects.all() Provides the 
# list of valid User instances this field can accept #(for validation during deserialization).
# slug_field= 'public_id' Uses the 'public_id' field of the User model to represent the user instead of the 
# default primary key (id).
    post = serializers.SlugRelatedField(queryset = Post.objects.all(), slug_field ='public_id')
#A DRF field that represents the related `Post` model using its `public_id` instead of the default PK.
#`queryset`: allows validation by fetching from Post model.
#`slug_field='public_id'`: uses the `public_id` field as the lookup key in input/output.


    def validate_author(self, value):
        if self.context["request"].user != value: #In DRF serializers, context is a dictionary passed when 
#initializing the serializer. self.context["request"] gives access to the current HTTP request object.
            raise ValidationError("You can't create comment for another user")
        return value
    
    def validate_post(self, value):
## If we're updating an existing instance, keep its original value. 
#self.instance refers to the existing object being updated.When creating a new object, self.instance is None.
#value is the new value provided by the user (typically through the API request) for the field you're validating.
#It's passed automatically to the validate_<field_name> method by DRF.
        if self.instance:
            return self.instance.value
        # If creating a new instance, use the provided value
        return value
    
    
    def update(self, instance, validated_data):
        if not instance.edited:
        # If the object hasn't been marked as edited yet  Mark it as edited before updating
            validated_data['edited']= True
        # Call the default update method to apply the changes
        instance = super().update(instance, validated_data)
        return instance
# '''update method: This is part of a Django REST Framework serializer. It's called when you use the serializer 
# to update an existing object (e.g., via a PUT or PATCH request). validated_data: A dictionary of cleaned and 
# validated data that was submitted via the API request. super().update(...): Calls DRF’s built-in update logic 
# to save changes to the database.'''

    
    def to_representation(self, instance):
        rep = super().to_representation(instance) #Gets the default serialized representation of the model instance
#using the parent class. Often used as a base to modify or enrich the output before returning the final response.
        author = User.objects.get_object_by_public_id(rep["author"])#Retrieves the User instance using a custom 
#manager method `get_object_by_public_id()`  Looks up the user based on the public_id present in the serialized
# `author` field.
        rep["author"] = UserSerializer(author).data #Replaces the default author field (e.g., just an ID or 
#public_id) with full serialized user data. Useful for embedding detailed author info directly into the response.
        return rep
    
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'body', 'edited', 'created', 'updated']
        read_only_fields = ["edited"]