from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.abstract.serializers import AbstractSerializer
from core.post.models import Post, PostMedia
from core.user.models import User

class PostMediaSerializer(AbstractSerializer):
    file = serializers.FileField() #Defines a serializer field to handle uploaded files in API requests.
    
    class Meta:
        model = PostMedia
        fields = ['id', 'file', 'is_video', 'updated',  'created']
        read_only_fields= ['id', 'created', 'updated'],  
        
class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(#SlugRelatedField represents a related object using a specific field (slug) instead of its ID
        queryset= User.objects.all(), # specifies valid user instances that can be assigned
                                          slug_field= 'public_id') #uses the user's public_id to identify them in API input/output.
    
    media= PostMediaSerializer(many=True, required=False, allow_null=True)
    #This method ensures that the author of a post matches the currently logged-in user;
#if not, it raises a ValidationError to prevent users from creating posts on behalf of others.
    
    def validate_author(self, value):
        if self.context["request"].user !=value:
            raise ValidationError("You can't create post for another user")
    
    def validate_media(self,value):
        if value and len(value)>10: # if media is there, compare length of media files
            raise ValidationError("Can not upload more than 10 files")
        return value
    def create(self, validated_data):
        """Handle creation of Post and associated media."""
        media_data = validated_data.pop('media', []) #Extracts and removes the 'media' field from validated_data;
        post = Post.objects.create_post(
            author=validated_data['author'],
            body=validated_data['body'],
            media_files=[data['file'] for data in media_data] if media_data else None
        )
        return post

    def update(self, instance, validated_data):
    #Handle updating Post and associated media.
        media_data = validated_data.pop('media', None)
        instance = super().update(instance, validated_data)

        if media_data is not None:
            existing_media = {media.id: media for media in instance.media.all()}
        for data in media_data:
            media_id = data.get('id')
            if media_id and media_id in existing_media:
                # Update existing media file
                media = existing_media[media_id]
                media.file = data['file']
                media.is_video = data['file'].name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))
                media.save()
            else:
                # Create new media file
                PostMedia.objects.create(
                    post=instance,
                    file=data['file'],
                    is_video=data['file'].name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))
                )
        return instance

    def to_representation(self, instance):
        """Customize the serialized output to include media."""
        representation = super().to_representation(instance)
        representation['media'] = PostMediaSerializer(instance.media.all(), many=True).data
        return representation

    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'edited', 'created', 'updated', 'media']
        read_only_fields = ['edited']
        
        
#Add comments from create method onwards

""" SlugRelatedField  is used to represent the target of the relationship 
using a field on the target. Thus, when creating a post, public_id of the author will be passed in 
the body of the request so that the user can be identified and linked to the post."""
    