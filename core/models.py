from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['image', str(instance.userpro.id)+str(instance.nickname)+str(".")+str(ext)])

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Email address is must')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name


class Profile(models.Model):
    nickname = models.CharField(max_length=20)
    userpro = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userpro',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    friends = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='friends',
    )
    img = models.ImageField(blank=True, null=True, upload_to=upload_path)

    def __str__(self):
        return self.nickname


class Message(models.Model):

    message = models.CharField(max_length=200)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sender',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='receiver',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.message

class Tweet(models.Model):

    text = models.CharField(max_length=140)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='owner',
        on_delete=models.CASCADE
    )

    def Tweet_by(self):
        try:
            temp = Profile.objects.get(userpro=self.owner)
        except Profile.DoesNotExist:
            temp = None
            return

        return temp.nickname

    def __str__(self):
        return self.text


















