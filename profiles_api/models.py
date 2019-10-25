from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserProfileManager(BaseUserManager):
    """
    Manager for user profile
    """
    def create_user(self, username, email, password=None):
        """
        Create a new normal user profile
        """
        if not email:
            raise ValueError('All users must have an email address')
        if not username:
            raise ValueError('All users must have an username')

        # normalize email (all in lowercase)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        # encrypted password
        user.set_password(password)
        # save user in db
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """
        Create a superuser profile
        """
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser):
    """
    Create new authentication user model for normal users
    """
    email = models.EmailField('Correo electronico', max_length=100,
                              unique=True)
    username = models.CharField('Nombre de usuario', max_length=50)
    first_name = models.CharField('Nombre(s)', max_length=100)
    last_name = models.CharField('Apellido paterno', max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField('Fecha de registro', auto_now_add=True)
    last_login = models.DateTimeField('Último login', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserProfileManager()

    def has_perm(self, perm, obj=None):
        """
        Admin permissions for users
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        User has permissions only if is active
        """
        return self.is_active

    def get_full_name(self):
        """
        Retrieve full name of user in history
        """
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        """
        Return username and email for represent users in admin
        """
        return self.email
