from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        if not extra_fields.get("nombre"):
            raise ValueError("El nombre es obligatorio")
        if not extra_fields.get("pais"):
            raise ValueError("El país es obligatorio")

        email = self.normalize_email(email)
        if self.model.objects.filter(email=email).exists():
            raise ValueError("Ya existe un usuario con ese email")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    pais = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'pais']

    objects = CustomUserManager()

    def __str__(self):
        return self.email