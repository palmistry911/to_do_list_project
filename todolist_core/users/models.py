from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    phone = models.CharField(max_length=15, blank=True)
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Необходимо указать электронный адрес почты")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(verbose_name='email_adress', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='first_name', max_length=50)
    last_name = models.CharField(verbose_name='last_name', max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    phone = models.CharField(max_length=12, unique=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name'], name='unique_first_name_last_name')
        ]

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def is_staff(self):
        return self.is_admin
