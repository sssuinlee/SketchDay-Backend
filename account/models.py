from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, auth_email, name, birth, password=None, **extra_fields):
        if not(name):
            raise ValueError('Name required')
        if not(auth_email):
            raise ValueError('Email required')

        auth_email = self.normalize_email(auth_email)
        validate_email(auth_email)
        
        user, created = self.model.objects.get_or_create(
            auth_email = auth_email,
            name = name,
            birth = birth
        )

        if (created and password):
            user.set_password(password)
            user.save(using=self._db)

        return user

    def create_superuser(self, auth_email, name, birth, password):
        user = self.create_user(auth_email=auth_email, name=name, birth=birth, password=password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user
    
    def __str__(self):
        return self.auth_email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser and self.is_staff


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auth_email = models.CharField(unique=True, max_length=50)
    name = models.CharField(unique=False, max_length=30)
    birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'auth_email'