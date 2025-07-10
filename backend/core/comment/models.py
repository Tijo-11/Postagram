from django.db import models
from core.abstract.models import AbstractModel, AbstractManager

class CommentManager(AbstractManager):
    pass

class Comment(AbstractModel):
    post = models.ForeignKey("core_post.Post", on_delete=models.PROTECT) ## Creates a foreign key relationship to the Post model; PROTECT prevents deletion of a Post if any related object (like a comment) exists.
    author = models.ForeignKey("core_user.User", on_delete= models.PROTECT)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    
    objects= CommentManager() # Replaces the default model manager with a custom one (CommentManager) that can include extra query methods 
    
    def __str__(self):
        return self.author.name