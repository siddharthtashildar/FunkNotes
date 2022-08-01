from django.db.models.deletion import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from shortuuid.django_fields import ShortUUIDField
import uuid

# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None,**other_fields):
        if not email:
            raise ValueError("User must have a email!")
        if not username:
            raise ValueError("User must have a username!")
        user=self.model(email=self.normalize_email(email),username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password,**other_fields):
        user=self.create_user(email=self.normalize_email(email),username=username,password=password, **other_fields)
        user.is_staff=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):

    email=models.EmailField(verbose_name="email", unique=True)
    username=models.CharField(verbose_name="username", unique=True , max_length=200)
    user_uuid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    objects=MyAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True






class NoteDatabase(models.Model):
    Note_user=models.ForeignKey("base.User",on_delete=models.CASCADE)
    noteID=ShortUUIDField(editable=False)
    name=models.CharField(max_length=200)
    content=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    is_locked=models.BooleanField(default=False)
    note_pin=models.CharField(verbose_name="Notepin" , max_length=60, null=True,blank=True) 

    def __str__(self):
        return str(self.name)

