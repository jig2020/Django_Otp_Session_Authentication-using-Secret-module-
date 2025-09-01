from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime, timezone
from common.models import BaseModel
import uuid


class TokenType(models.TextChoices):
    PASSWORD_RESET = ("PASSWORD_RESET",)
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, fullname, password, **extra_fields):
        if not email:
            raise ValueError('Email must set')
        user= self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save()
        return user 
    
    def create_superuser(self, email, fullname, password, **extra_fields):
        #create and save the superuser with the given email, fullname and password
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True")
        user=self.create_user(email,fullname,password, **extra_fields)
        user.save()
        
        
class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    #is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']
    objects = CustomUserManager()
    
#a manager is the middle man between the app and the database

#pending user this table will be used to keep track of the information submitted

class PendingUser(BaseModel):
    email = models.EmailField()
    fullname = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
#we need a method to check if verification code is valid or not
    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60
        now = datetime.now(timezone.utc)
        
        timediff = now - self.created_at
        timediff = timediff.total_seconds()
        
        if timediff > lifespan_in_seconds:
            return False
        return True
    
    
class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=100, choices=TokenType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} {self.token}"
    
    #we need a method to check if token is valid or not
    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60  #20min
        now = datetime.now(timezone.utc)
        
        timediff = now - self.created_at
        timediff = timediff.total_seconds()
        
        if timediff > lifespan_in_seconds:
            return False
        return True
    
    def reset_user_password(self, raw_password: str):
        self.user: User
        self.user.set_password(raw_password)
        self.user.save()