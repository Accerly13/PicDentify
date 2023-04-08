from django.db import models

# Create your models here.
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.

now = timezone.now()


class MyUserManager(BaseUserManager):
    def create_user(self, admin_id, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        user = self.model(admin_id=admin_id, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, admin_id, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(admin_id, username, password=password, **extra_fields)
    

class AdminUser(AbstractBaseUser, PermissionsMixin):
    admin_id = models.PositiveIntegerField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'admin'

class AdminKey(models.Model):
    key_id = models.AutoField(primary_key=True, unique=True)
    admin_key = models.CharField(max_length=50, verbose_name='admin_key')

    class Meta:
        db_table = "admin_key"
    