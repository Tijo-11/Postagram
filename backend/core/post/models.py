from core.abstract.models import AbstractModel, AbstractManager
from django.db import models
from django.core.exceptions import ValidationError
import os

# Validation function for video file size
def validate_video_size(value): #value is the file uploaded by the user — passed automatically by Django when the validator is called. It's usually an instance of UploadedFile, and it contains metadata like file size, name, etc.
    max_size = 25*1024 * 1024 #25 MB in bytes 
    if value.size>max_size: #When a user submits a file (via form, API, etc.), Django runs your validator on the uploaded file before saving it to the model
        raise ValidationError(f"Video file size can not exceed 25 MB")
    
#validation function for file extenstion
def validate_file_extension(value):
    valid_image_extensions= ['.jpg', 'jpeg', '.png', '.gif']
    valid_video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    ext = os.path.splitext(value.name)[1].lower() # Extracts and lowercases the file extension of the uploaded file.value.name: Gets the original file name (e.g., "video.mp4").
    if ext not in valid_image_extensions + valid_video_extensions:
        raise ValidationError("Unsupported file format. Allowed formats: JPG, JPEG, PNG, GIF, MP4, MOV, AVI, MKV.")
class PostManager(AbstractManager):
    def create_post(self, author, body, media_files=None):
        post = self.create(author=author, body=body)
        if media_files:
            media_count = len(media_files)
            if media_count > 10:
                raise ValidationError("Cannot upload more than 10 media files.")
            for file in media_files:
                is_video = os.path.splitext(file.name)[1].lower() in ['.mp4', '.mov', '.avi', '.mkv']
                PostMedia.objects.create(
                    post=post,
                    file=file,
                    is_video=is_video
                )
        return post

class Post(AbstractModel):
    author = models.ForeignKey(to="core_user.User",#creates a many-to-one relationship where each record links to a user from the core_user app, meaning multiple objects can share the same author.
                               on_delete=models.CASCADE) #means that if the referenced user (author) is deleted, all related objects (e.g., posts) will also be automatically deleted from the database.
    body = models.TextField()
    edited = models.BooleanField(default=False)
    
    objects= PostManager()
    
    def __str__(self):
        return f"{self.author.name}"
    
    def validate_media_count(self):
        """Ensure the post doesn't have more than 10 media files."""
        if self.media.count() > 10:
            raise ValidationError("A post cannot have more than 10 media files.")
    
    class Meta:
        db_table= "core.post" #explicitly sets the database table name for the model to "core.post" instead of Django’s default naming convention.
        
        """ not 
only can we use the Post.author syntax to access the user object but we can also access 
posts created by a user using the User.post_set syntax. The latter syntax will return a 
queryset object containing the posts created by the user because we are in a ForeignKey 
relationship, which is also a one-to-many relationship."""

# image field here
class PostMedia(AbstractModel): #Since the media files might be uploaded independently or might require auditability (when added, changed), it often makes sense to inherit from AbstractModel, even if the Post already has timestamps.
    post = models.ForeignKey(
        Post,
        related_name="media",
        on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to="post_media/",
        validators=[validate_file_extension, validate_video_size]
    )
    is_video = models.BooleanField(default=False)
    def clean(self):
        """Custom validation for media files."""
        super().clean()
        if self.is_video and self.file.size > 25 * 1024 * 1024:
            raise ValidationError("Video file size exceeds 25 MB limit.")
    class Meta:
        db_table = "core.post_media"

"""Apart from CASCADE as a value for the on_delete attribute on a ForeignKey relationship, 
you can also have the following:
 • SET_NULL: This will set the child object foreign key to null on delete. For example, if a user 
is deleted from the database, the value of the author field of the posts in relation to this user 
is set to None.
 • SET_DEFAULT: This will set the child object to the default value given while writing the 
model. It works if you are sure that the default value won’t be deleted.
 • RESTRICT: This raises RestrictedError under certain conditions.
 • PROTECT: This prevents the foreign key object from being deleted as long as there are objects 
linked to the foreign key object.
"""


    
    


