from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from .models import (Role, Permission, Role_Permission, Account)
import re
from django.contrib.auth.hashers import make_password
from .constants import (
    ADDED,
    EXISTS,
    REQUIRED,
    INVALID_METHOD,
    UPDATED,
    NOT_FOUND,
    ASSIGN,
    NOT_FOUND_ROLE,
    EMAIL_EXISTS,
    PHONE_FORMAT,
    PASS_NOT_ENOUGH
)
import json


@csrf_exempt
def add_role(request):
    """
    View function to add a new role to the database.

    This function handles POST requests to add a new role to the database.
    The role name must be provided in the JSON data of the request.

    Returns a JSON response with a success message if the role is added successfully.
    Returns a JSON response with an error message if the role name already exists or if the request data is invalid.
    """

    if request.method == "POST":
        data = json.loads(request.body)
        role_name = data.get("role_name", None)

        if role_name is not None:
            try:
                role = Role(role_name=role_name)
                role.save()
                return JsonResponse({"message": ADDED}, status=201)
            except IntegrityError:
                return JsonResponse({"message": EXISTS}, status=400)
        return JsonResponse({"message": REQUIRED}, status=400)

    return JsonResponse({"message": INVALID_METHOD}, status=405)


def get_roles(request):
    """
    API endpoint to retrieve a list of roles from the database.

    This function handles GET requests to retrieve a list of roles from the database.

    Returns:
        JsonResponse: A JSON response containing the list of roles.
    """

    if request.method == "GET":
        roles = Role.objects.all()
        role_data = [
            {"role_id": role.role_id, "role_name": role.role_name} for role in roles
        ]
        return JsonResponse({"roles": role_data}, status=200)

    return JsonResponse({"message": INVALID_METHOD}, status=405)


@csrf_exempt
def update_role(request, role_id):
    """
    API endpoint to update the name of a role.

    Parameters:
        request: The HTTP request object.
        role_id: The id of the role to be updated.

    Returns:
        JsonResponse: A JSON response indicating the result of the update.
            - If the update is successful, returns a success message.
            - If the role does not exist, returns an error message with status 404.
            - If the role name is not provided or the request data is invalid, returns an error message with status 400.
            - If the request method is not PUT, returns an error message with status 405.
    """

    if request.method == "PUT":
        data = json.loads(request.body)
        role_name = data.get("role_name", None)

        if role_name is not None:
            try:
                role = Role.objects.get(role_id=role_id)
                role.role_name = role_name
                role.save()
                return JsonResponse({"message": UPDATED}, status=200)
            except IntegrityError:
                return JsonResponse({"message": EXISTS}, status=400)
            except Role.DoesNotExist:
                return JsonResponse({"message": NOT_FOUND}, status=404)
        return JsonResponse({"message": REQUIRED}, status=400)

    return JsonResponse({"message": INVALID_METHOD}, status=405)


@csrf_exempt
def delete_role(request, role_id):
    """
    API endpoint to delete a role from the database.

    Parameters:
        request: The HTTP request object.
        role_id (str): The ID of the role to be deleted.

    Returns:
        JsonResponse: A JSON response indicating the result of the delete operation.
    """

    if request.method == "DELETE":
        try:
            role = Role.objects.get(role_id=role_id)
            role.delete()
            return JsonResponse(status=204)
        except Role.DoesNotExist:
            return JsonResponse({"message": NOT_FOUND}, status=404)

    return JsonResponse({"message": INVALID_METHOD}, status=405)


@csrf_exempt
def add_permission(request):
    """
    API endpoint to add a new permission to the database.

    This function handles POST requests to add a new permission to the database.
    The permission name and description must be provided in the JSON data of the request.

    Returns:
        JsonResponse: A JSON response indicating the result of the add operation.
    """

    if request.method == "POST":
        data = json.loads(request.body)
        permission_name = data.get("permission_name", None)
        description = data.get("description", None)

        if permission_name is not None and description is not None:
            try:
                permission = Permission(
                    permission_name=permission_name, description=description
                )
                permission.save()
                return JsonResponse({"message": ADDED}, status=201)
            except IntegrityError:
                return JsonResponse({"message": EXISTS}, status=400)
        else:
            return JsonResponse({"message": REQUIRED}, status=400)

    return JsonResponse({"message": INVALID_METHOD}, status=405)


def get_permissions(request):
    """
    API endpoint to retrieve a list of permissions from the database.

    This function handles GET requests to retrieve a list of permissions from the database.

    Returns:
        JsonResponse: A JSON response containing the list of permissions.
    """

    if request.method == "GET":
        permissions = Permission.objects.all()
        permission_data = [
            {
                "permission_id": permission.permission_id,
                "permission_name": permission.permission_name,
                "description": permission.description,
                "status": permission.status,
            }
            for permission in permissions
        ]
        return JsonResponse({"permissions": permission_data}, status=200)

    return JsonResponse({"message": INVALID_METHOD}, status=405)


@csrf_exempt
def update_permission(request, permission_id):
    """
    API endpoint to update a permission in the database.

    This function handles PUT requests to update the information of a permission in the database.
    The permission ID should be provided in the URL.
    The updated permission data should be provided in the JSON data of the request.

    Parameter:
        permission_id (int): The ID of the permission to be updated.

    Returns:
        JsonResponse: A JSON response indicating the result of the operation.
    """

    if request.method == "PUT":
        try:
            permission = Permission.objects.get(permission_id=permission_id)
            data = json.loads(request.body)

            if "status" in data:
                if permission.status == "A":
                    permission.status = "D"
                else:
                    permission.status = "A"

            permission_name = data.get("permission_name", permission.permission_name)
            description = data.get("description", permission.description)

            permission.permission_name = permission_name
            permission.description = description
            permission.save()

            return JsonResponse({"message": UPDATED}, status=200)
        except Permission.DoesNotExist:
            return JsonResponse({"message": NOT_FOUND}, status=404)
        except IntegrityError:
            return JsonResponse({"message": EXISTS}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"message": INVALID_METHOD}, status=405)


@csrf_exempt
def assign_permission(request):
    """
    API endpoint to assign a permission to a role.

    This function handles POST requests to assign a permission to a role in the Role_Permission table.
    The role ID and permission ID should be provided in the JSON data of the request.

    Returns:
        JsonResponse: A JSON response indicating the result of the assignment.
    """

    if request.method == 'POST':
        data = json.loads(request.body)
        role_id = data.get('role_id', None)
        permission_id = data.get('permission_id', None)
       
        if role_id is not None and permission_id is not None:
            try:
                role = Role.objects.get(pk=role_id)
                permission = Permission.objects.get(pk=permission_id)
               
                role_permission = Role_Permission(role_id=role, permission_id=permission)
                role_permission.save()
               
                return JsonResponse({"message": ASSIGN}, status=201)
            except Role.DoesNotExist:
                return JsonResponse({"message": NOT_FOUND}, status=404)
            except Permission.DoesNotExist:
                return JsonResponse({"message": NOT_FOUND}, status=404)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=400)
       
        return JsonResponse({"message": REQUIRED}, status=400)
   
    return JsonResponse({"message": INVALID_METHOD}, status=405)


@csrf_exempt
def add_account(request):
    """
    API endpoint to add a new account to the database

    This function handles POST requests to add a new account to the database.

    Attributes:
        account_id (AutoField): The unique identifier for the account.
        user_name (CharField): The name of the user.
        password (CharField): The password for the account.
        role_id (ForeignKey): The role associated with the account.
        birth_day (DateField): The user's birth date.
        address (CharField): The user's address.
        email(CharField): The user's email
        phone_number (CharField): The user's phone number.
        gender (CharField): The gender of the user.
        status (CharField): The status of the account.

    Returns:
        JsonResponse: A JSON response indicating a result of the add operation
    """


    if request.method != "POST":
        return JsonResponse({"message": INVALID_METHOD}, status=405)
    
    else:
        data = json.loads(request.body)
           
        user_name = data.get("user_name", None)
        raw_password = data.get("password", None)
        role_id = data.get("role_id", None)
        birth_day = data.get("birth_day", None)
        address = data.get("address", None)
        email = data.get("email", None)
        phone_number = data.get("phone_number", None)
        gender = data.get("gender", None)

        if not re.match(r'^0\d{9}$', phone_number):
            return JsonResponse({"message": PHONE_FORMAT}, status=400)  

        if len(raw_password) < 8:
            return JsonResponse({"message": PASS_NOT_ENOUGH}, status=400)     

        if (
            user_name
            and raw_password
            and role_id
            and birth_day
            and address
            and email
            and phone_number
            and gender
        ):
               
            try:
                hashed_password = make_password(raw_password)
                role = Role.objects.get(role_id=role_id)

                account = Account(
                    user_name=user_name,
                    password=hashed_password,
                    role_id=role,
                    birth_day=birth_day,
                    address=address,
                    email=email,
                    phone_number=phone_number,
                    gender=gender,
                )
                account.save()
                return JsonResponse({"message": ADDED}, status=201)
            
            except Role.DoesNotExist:
                return JsonResponse({"message": NOT_FOUND_ROLE}, status=400)
            except IntegrityError:
                return JsonResponse({"message": EMAIL_EXISTS}, status=400)

        return JsonResponse({"message": REQUIRED}, status=400)
