from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_superuser=True
        user.is_staff=True
        user.is_admin=True
        user.can_access_watch_temp = True;
        user.can_access_arrow_move = True;
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    can_access_watch_temp = models.BooleanField(default=False)
    can_access_arrow_move = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class ActivateToken(models.Model):
	user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
	key = models.CharField(max_length=255, unique=True)
	expire_time = models.DateTimeField()

