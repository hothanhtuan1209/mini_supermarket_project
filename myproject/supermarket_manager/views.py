from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import (Role, Permission, Role_Permission, Account)
import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .constants import (
    ADDED,
    EXISTS,
    REQUIRED,
    INVALID_METHOD,
    UPDATED,
    NOT_FOUND,
    ASSIGN,
    NOT_FOUND_ROLE,
    PHONE_FORMAT,
    PASS_NOT_ENOUGH,
    LOGIN,
    INCORRECT,
    REQUIRED_LOGIN,
    CHANGED_PASSWORD,
    INCORRECT_OLD_PASSWORD
)
import json


@csrf_exempt
@login_required(login_url='api/logins')
def add_role(request):
    """
    Function:
        - View function to add a new role to the database.

        - This function handles POST requests to add a new role to the database.
        - The role name must be provided in the JSON data of the request.

    Returns:
        - JsonResponse with a success message if the role is added successfully.
        - JsonResponse with an error message if the role name already exists or if the request data is invalid.
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


@login_required(login_url='api/logins')
def get_roles(request):
    """
    Function:
        - API endpoint to retrieve a list of roles from the database.

        - This function handles GET requests to retrieve a list of roles from the database.

    Returns:
        - JsonResponse: A JSON response containing the list of roles.
    """

    if request.method == "GET":
        roles = Role.objects.all()
        role_data = [
            {"role_id": role.role_id, "role_name": role.role_name} for role in roles
        ]
        return JsonResponse({"roles": role_data}, status=200)

    return JsonResponse({"message": INVALID_METHOD}, status=405)


@csrf_exempt
@login_required(login_url='api/logins')
def update_role(request, role_id):
    """
    Function:
        - API endpoint to update the name of a role.

    Parameters:
        - request: The HTTP request object.
        - role_id: The id of the role to be updated.

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
@login_required(login_url='api/logins')
def delete_role(request, role_id):
    """
    Function:
        - API endpoint to delete a role from the database.

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
@login_required(login_url='api/logins')
def add_permission(request):
    """
    Function:
        - API endpoint to add a new permission to the database.

        - This function handles POST requests to add a new permission to the database.
        - The permission name and description must be provided in the JSON data of the request.

    Returns:
        - JsonResponse: A JSON response indicating the result of the add operation.
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


@login_required(login_url='api/logins')
def get_permissions(request):
    """
    Function:
        - API endpoint to retrieve a list of permissions from the database.

        - This function handles GET requests to retrieve a list of permissions from the database.

    Returns:
        - JsonResponse: A JSON response containing the list of permissions.
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
@login_required(login_url='api/logins')
def update_permission(request, permission_id):
    """
    Function:
        - API endpoint to update a permission in the database.

        - This function handles PUT requests to update the information of a permission in the database.
        - The permission ID should be provided in the URL.
        - The updated permission data should be provided in the JSON data of the request.

    Parameter:
        - permission_id (int): The ID of the permission to be updated.

    Returns:
        - JsonResponse: A JSON response indicating the result of the operation.
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
@login_required(login_url='api/logins')
def assign_permission(request):
    """
    Function:
        - API endpoint to assign a permission to a role.

        - This function handles POST requests to assign a permission to a role in the Role_Permission table.
        - The role ID and permission ID should be provided in the JSON data of the request.

    Returns:
        - JsonResponse: A JSON response indicating the result of the assignment.
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


@csrf_protect
@login_required(login_url='api/logins')
def add_account(request):
    """
    Function:
        - API endpoint to add a new account to the database

        - This function handles POST requests to add a new account to the database.
    
    Attributes:
        - account_id (CharField): The unique identifier for the account.
        - user_name (CharField): The name of the user.
        - password (TextField): The password for the account.
        - role_id (ForeignKey): The role associated with the account.
        - birth_day (DateField): The user's birth date.
        - address (CharField): The user's address.
        - email(CharField): The user's email
        - phone_number (CharField): The user's phone number.
        - gender (CharField): The gender of the user.
        - status (CharField): The status of the account.
    
    Returns:
        - JsonResponse: A JSON response indicating a result of the add operation
    """


    if request.method != "POST":
        return JsonResponse({"message": INVALID_METHOD}, status=405)

    data = json.loads(request.body)

    user_name = data.get("user_name", None)
    raw_password = data.get("password", None)
    role_id = data.get("role_id", None)
    birth_day = data.get("birth_day", None)
    address = data.get("address", None)
    email = data.get("email", None)
    phone_number = data.get("phone_number", None)

    if not re.match(r'^0\d{9}$', phone_number):
        return JsonResponse({"message": PHONE_FORMAT}, status=400)  

    if raw_password is not None and len(raw_password) < 8:
        return JsonResponse({"message": PASS_NOT_ENOUGH}, status=400)     

    if (
        user_name
        and raw_password
        and role_id
        and birth_day
        and address
        and email
        and phone_number
    ):

        try:
            hashed_password = make_password(raw_password)
            role            = Role.objects.get(role_id=role_id)
            account = Account()
            account.account_id   = account.random_account_id()
            account.user_name    = user_name
            account.user_name    = user_name
            account.password     = hashed_password
            account.role_id      = role
            account.birth_day    = birth_day
            account.address      = address
            account.email        = email
            account.phone_number = phone_number
            account.save()
            return JsonResponse({"message": ADDED}, status=201)

        except Role.DoesNotExist:
            return JsonResponse({"message": NOT_FOUND_ROLE}, status=400)

    return JsonResponse({"message": REQUIRED}, status=400)


@login_required(login_url='api/logins')
def get_account_detail(request, account_id):
    """
    Function:
        - API endpoint to retrieve detailed information about a specific user account.

        - This function handles GET requests to retrieve detailed information about a user account
        based on the provided `account_id`. It returns a JSON response with the following details:

            + 'user_name': The name of the user.
            + 'role': The role associated with the user account.
            + 'birth_day': The user's birth date in the format 'YYYY-MM-DD'.
            + 'address': The user's address.
            + 'email': The user's email address.
            + 'phone_number': The user's phone number.
            + 'gender': The user's gender (displayed as 'Male', 'Female', or 'Other').
            + 'status': The status of the user account (displayed as 'Active' or 'Disable').

    Parameters:
        - request (HttpRequest): The HTTP request object.
        - account_id (str): The unique identifier of the user account to retrieve.

    Returns:
        - JsonResponse: A JSON response containing the user account details if found,
        or a JSON response with a 'message' field indicating 'NOT_FOUND' and a status code of 404
        if the account is not found in the database.
    """
        
    try:
        account = Account.objects.get(account_id=account_id)
        account_data = {
            'user_name': account.user_name,
            'role': account.role_id.role_name,
            'birth_day': account.birth_day.strftime('%Y-%m-%d'),
            'address': account.address,
            'email': account.email,
            'phone_number': account.phone_number,
            'gender': account.get_gender_display(),
            'status': account.get_status_display(),
        }
        return JsonResponse(account_data, status=200)
    except Account.DoesNotExist:
        
        return JsonResponse({"message": NOT_FOUND}, status=404)


@csrf_exempt
def login_account(request):
    """
    Function:
        - API endpoint for user login.

        - This function handles POST requests for user login.
        - Users can login using their email and password.
        - If either the email or password is missing, it returns a 400 Bad Request response.
        - If the login credentials are incorrect, it returns a 401 Unauthorized response.

    Parameters:
        - request (HttpRequest): The HTTP request object containing user login credentials.

    Returns:
        - JsonResponse: A JSON response indicating the result of the login attempt.
    """

    if request.method != "POST":
        return JsonResponse({"message": INVALID_METHOD }, status=405)
    
    data = json.loads(request.body)
    email = data.get("email", None)
    password = data.get("password", None)

    if not email or not password:
        return JsonResponse({"message": REQUIRED_LOGIN}, status=400)

    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({"message": LOGIN}, status=200)
    
    return JsonResponse({"message": INCORRECT}, status=401)


@csrf_exempt
@login_required(login_url='api/logins')
def update_account(request, account_id):
    """
    Function:
        - Update account information.

        - This view allows updating account information such as user name, birth date, address,
          email, phone number, gender, and status.
        - The view expects a PUT request with a JSON
          body containing the fields to be updated.

    Parameters:
        - request: The HTTP request object.
        - account_id: The unique identifier of the account to be updated.

    Returns:
        - JsonResponse: A JSON response indicating the result of the update operation.
    """

    if request.method != "PUT":
        return JsonResponse({"message": INVALID_METHOD}, status=405)
    
    try:
        account = Account.objects.get(account_id=account_id)
        data = json.loads(request.body)

        if "status" in data:
            if account.status == "A":
                account.status = "D"
            else:
                account.status = "A"

        account.user_name = data.get('user_name', account.user_name)
        account.birth_day = data.get('birth_day', account.birth_day)
        account.address = data.get('address', account.address)
        account.email = data.get('email', account.email)
        account.phone_number = data.get('phone_number', account.phone_number)
        account.gender = data.get('gender', account.gender)

        account.save()

        return JsonResponse({"message": UPDATED})
    
    except Account.DoesNotExist:
        return JsonResponse({"message": NOT_FOUND}, status=404)
    
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)


@csrf_exempt
@login_required(login_url='api/logins')
def change_password(request, account_id):
    """
    Function:
        - Change account password.

        - This view allows changing the password of the account associated with the provided
        account_id. It expects a POST request with a JSON body containing the old_password
        and new_password fields.

    Parameters:
        - request: The HTTP request object.
        - account_id: The unique identifier of the account whose password will be changed.

    Returns:
        - JsonResponse: A JSON response indicating the result of the password change operation.
    """

    if request.method != "PATCH":
        return JsonResponse({"message": INVALID_METHOD}, status=405)

    try:
        account = Account.objects.get(account_id=account_id)
        data = json.loads(request.body)

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if account.check_password(old_password):
            account.set_password(new_password)
            
            account.save()
            update_session_auth_hash(request, account)

            return JsonResponse({"message": CHANGED_PASSWORD})
        
        else:
            return JsonResponse({"message": INCORRECT_OLD_PASSWORD}, status=400)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
