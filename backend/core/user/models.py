import uuid

from django.db import models #This line imports Django's models module, which provides classes and tools to define and interact with database tables using Django's Object-Relational Mapping (ORM).
from django.contrib.auth.models  import AbstractBaseUser, BaseUserManager, PermissionsMixin #This line imports essential Django classes used to create a custom user model, AbstractBaseUser: Provides core user authentication features (like password)., BaseUserManager: Helps manage user creation (e.g., create_user, create_superuser), PermissionsMixin: Adds permission handling (like groups and is_superuser).
from django.core.exceptions import ObjectDoesNotExist  #an exception raised when a database query fails to find a matching object (e.g., Model.objects.get() with no result).
from django.http import Http404 # from the http module inside the Django package. 
from core.abstract.models import AbstractModel, AbstractManager

class UserManager(BaseUserManager, AbstractManager):
    def get_object_by_public_id(self, public_id):#This method tries to find and return an object with the given public_id; if found, it returns the matching instance.
        try:
            instance = self.get(public_id = public_id)
            return instance
        except(ObjectDoesNotExist, ValueError, TypeError):
            return Http404
    
    def create_user(self, username, email, password=None, **kwargs): #pasword=None means means the password is optional when calling create_user. This allows flexibility — if no password is passed, the method can still run (e.g., for inactive users or external auth), and you can handle it manually inside the function.
        """Create and return a `User` with an email, phone
           number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise TypeError('User must have an password') #Remove the check if password should be optional, , it is confusing
        user = self.model(username=username,
           email=self.normalize_email(email), **kwargs)
        user.set_password(password) #Hashes the plain-text password and stores it securely — never saves the raw password directly.
        user.save(using=self._db) # Saves the user to the correct database connection used by the manager — helpful in multi-database setups.
        
        return user
    def create_superuser(self, username, email, password, **kwargs):
        """ Create and return a `User` with superuser (admin) permissions. """
        if password is None:
            raise TypeError ('Superusers must have a password ')
        if email is None:
            raise TypeError('Superusers must have an email')
        if username is None:
            raise TypeError('Superusers must have a username')
        
        user = self.create_user( username, email, password, **kwargs) #self.create_user(...) is a call to your own method create_user, likely from inside create_superuser or another method in UserManager. It reuses your user creation logic to avoid duplicating code.
        user.is_superuser= True #**kwargs lets you pass extra keyword arguments like first_name, last_name, is_staff, etc.
        user.is_staff = True #*args is for positional arguments, which isn’t useful here. You want to pass named fields like first_name='John', not position-based ones like 'John'
        user.save(using=self._db)
        
        return user   

class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index= True, max_length=255, unique=True) #A database index is like a lookup table that speeds up searches, filtering, and joins involving that field.
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True)
    
    USERNAME_FIELD = 'email' #Tells Django to use email as the unique identifier for login instead of the default username. Only the email will be used for login — not the username.
    REQUIRED_FIELDS = ['username'] #Tells Django that username must be provided when creating a superuser via createsuperuser.
    
    
    objects = UserManager() #sets UserManager as the custom manager for your user model. UserManager is typically a subclass of BaseUserManager
    
    def __str__(self):
        return f"{self.email}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}" #@property turns a method into a read-only attribute, letting you access it like a variable (e.g., user.name instead of user.name()
    

