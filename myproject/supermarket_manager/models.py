from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from .constants import (STATUS_CHOICES, GENDER_CHOICES)
import random
import string


class Permission(models.Model):
    """
    A class representing different permissions within the system.

    Attributes:
        permission_id (AutoField): The unique identifier for the permission.
        permission_name (CharField): The name of the permission.
        description (CharField): A description of the permission.
    """

    permission_id = models.AutoField(primary_key=True)
    permission_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="A")

    def __str__(self):
        """
        Return a string representation of the Permission object.
        """
        return str(self.permission_name)


class Role(models.Model):
    """
    A class representing different roles within the system.

    Attributes:
        role_id (AutoField): The unique identifier for the role.
        role_name (CharField): The name of the role.
    """

    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    permission = models.ManyToManyField(Permission, through="Role_Permission")

    def __str__(self):
        """
        Return a string representation of the Role object.
        """

        if isinstance(self.role_name, str):
            return self.role_name
        else:
            return str(self.role_name)


class AccountManager(BaseUserManager):
    """
    Custom manager for the Account model.

    This manager provides methods for creating user accounts and superuser accounts.

    Attributes:
        BaseUserManager: The base manager class provided by Django.
    """
    
    def create_user(self, email, user_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, user_name, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    """
    A class representing user accounts.

    Attributes:
        account_id (charField): The unique identifier for the account.
        user_name (CharField): The name of the user.
        password (TextField): The password for the account.
        role_id (ForeignKey): The role associated with the account.
        birth_day (DateField): The user's birth date.
        address (CharField): The user's address.
        email(CharField): The user's email
        phone_number (CharField): The user's phone number.
        gender (CharField): The gender of the user.
        status (CharField): The status of the account.
    """

    account_id = models.CharField(
        primary_key=True, max_length=5, unique=True
    )
    user_name = models.CharField(max_length=100)
    password = models.TextField(validators=[MinLengthValidator(8)])
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    birth_day = models.DateField()
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(
        validators=[RegexValidator(r"^0\d{9}$")], max_length=10
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="A")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['user_name', 'birth_day', 'address', 'phone_number', 'gender', 'status']
    USERNAME_FIELD = 'email'

    objects = AccountManager()


    def __str__(self):
        """
        Return a string representation of the Account object.
        """
        return str(self.user_name)
    
    def random_account_id(self):
        while True:
            account_id = ''.join(random.choices(string.digits, k=5))
            if not Account.objects.filter(account_id=account_id).exists():
                return account_id


class Role_Permission(models.Model):
    """
    A class representing the relationship between roles and permissions.

    Attributes:
        role_permission_id (AutoField): The unique identifier for the role-permission relationship.
        role_id (ForeignKey): The role associated with the relationship.
        permission_id (ForeignKey): The permission associated with the relationship.
    """

    role_permission_id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission_id = models.ForeignKey(Permission, on_delete=models.CASCADE)
