from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
import random, string
from datetime import timedelta




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    ADMIN = 'admin'
    SCHOOL = 'school'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (SCHOOL, 'School')
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default=SCHOOL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def _str_(self):
        return self.email

class AccessKey(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    )
    key = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date_of_procurement = models.DateField(default=timezone.now)
    expiry_date = models.DateField()
    school_email = models.EmailField() 


    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_date = self.date_of_procurement + timedelta(days=30)
            self.school_email = self.user.email
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    def generate_key(self, length=16):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))

    def is_active(self):
        return self.status == 'active' and self.expiry_date >= timezone.now().date()

    def is_expired(self):
        return self.status == 'expired' or self.expiry_date < timezone.now().date()

    def revoke_key(self):
        self.status = 'revoked'
        self.save()


   



