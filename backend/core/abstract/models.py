"""An abstract class can be considered a blueprint for other classes. It usually contains a set of methods 
or attributes that must be created within any child classes built from the abstract class.
 In this file, we will write two classes: AbstractModel and AbstractManager.
 The AbstractModel class will contain fields such as public_id, created, and updated. 
On the other side, the AbstractManager class will contain the function used to retrieve an object 
by its public_id field"""

from django.db import models
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class AbstractManager(models.Manager): #models.Manager is Django’s base class for model managers — it provides
    #the interface through which database query operations are made (like User.objects.all() or 
    # User.objects.create())
    def get_object_by_public_id(self, public_id): #Tries to retrieve an object with the given public_id.
        try:
            instance = self.get(public_id = public_id) #The public_id is typically passed through the ViewSet — 
            #often extracted from the URL (self.kwargs['pk']), then used in the ORM query like:
            # User.objects.get_object_by_public_id(public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404
        

class AbstractModel(models.Model):
    public_id= models.UUIDField(db_index=True, unique=True, default= uuid.uuid4, editable=False) #uuid is Python's
    #built-in module for generating universally unique identifiers (UUIDs). uuid.uuid4() creates a random UUID 
    # (version 4
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) # auto_now_add=True sets the timestamp only once when the object 
    #is created, while auto_now=True updates it automatically every time the object is saved.
    
    objects = AbstractManager() #assigns your custom manager (AbstractManager) to the model, enabling custom query
    #methods (like get_object_by_public_id) through Model.objects.
    
    class Meta:
        abstract = True #class Meta: abstract = True marks the model as abstract, meaning Django won't create 
        #a database table for it — it's meant to be inherited by other models to reuse common fields or logic.