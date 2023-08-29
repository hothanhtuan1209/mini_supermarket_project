from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from .models import Role, Permission
from .constants import (
    ADDED,
    EXISTS,
    REQUIRED,
    INVALID_METHOD,
    UPDATED,
    NOT_FOUND,
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
        JsonResponse: A JSON response indicating the result of the update operation.
    """

    if request.method == "PUT":
        try:
            permission = Permission.objects.get(permission_id=permission_id)
            data = json.loads(request.body)

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
def toggle_status(request, permission_id):
    """
    Toggle the status of a permission.

    This function handles PUT requests to toggle the status of a permission identified by its permission_id.
    If the permission is currently active (status "A"), it will be toggled to "D" (disabled), and vice versa.

    Parameters:
        request (HttpRequest): The HTTP request object.
        permission_id (int): The ID of the permission to toggle the status.

    Returns:
        JsonResponse: A JSON response indicating the result of the toggle status operation
    """

    if request.method == "PUT":
        try:
            permission = Permission.objects.get(permission_id=permission_id)

            if permission.status == "A":
                permission.status = "D"
            else:
                permission.status = "A"
            permission.save()

            return JsonResponse(status=204)

        except Permission.DoesNotExist:
            return JsonResponse({"message": NOT_FOUND}, status=404)

    return JsonResponse({"message": INVALID_METHOD}, status=400)
