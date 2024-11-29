from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Custom manager for User model where email is the unique identifier."""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    dni = models.CharField(max_length=10)
    birthdate = models.DateField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'telephone', 'address', 'dni', 'birthdate']

    objects = CustomUserManager()

    def __str__(self):
        return self.email