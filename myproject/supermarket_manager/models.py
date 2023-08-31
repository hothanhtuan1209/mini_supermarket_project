from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from .constants import STATUS_CHOICES


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

        if isinstance(self.permission_name, str):
            return self.permission_name
        else:
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


class Account(models.Model):
    """
    A class representing user accounts.

    Attributes:
        account_id (CharField): The unique identifier for the account.
        user_name (CharField): The name of the user.
        login_name (CharField): The login name of the user.
        password (CharField): The password for the account.
        role_id (ForeignKey): The role associated with the account.
        birth_day (DateField): The user's birth date.
        address (CharField): The user's address.
        email(CharField): The user's email
        phone_number (CharField): The user's phone number.
        gender (CharField): The gender of the user.
        status (CharField): The status of the account.
    """

    account_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    login_name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=30, validators=[MinLengthValidator(8)])
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    birth_day = models.DateField()
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(
        validators=[RegexValidator(r"^0\d{9}$")], max_length=10
    )

    GENDER_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Other")]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="A")

    def __str__(self):
        """
        Return a string representation of the Account object.
        """

        if isinstance(self.user_name, str):
            return self.user_name
        else:
            return str(self.user_name)


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
