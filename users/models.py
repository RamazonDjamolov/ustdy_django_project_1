from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


def time_default():
    return timezone.now() + timedelta(seconds=45)


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, theme_color=None):
        if CustomUser.objects.filter(email=email).exists():
            raise ValueError("A user with this email already exists.")
        if CustomUser.objects.filter(username=username).exists():
            raise ValueError("A user with this username already exists.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, theme_color=theme_color)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, theme_color=None):
        user = self.create_user(username, email, password, theme_color)
        user.theme_color = theme_color
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    theme_color = models.CharField(max_length=20, default="blue", null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True


class Code(models.Model):
    code_number = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='code_user')
    expired_data = models.DateTimeField(default=time_default)

    class Meta:
        db_table = 'code'
