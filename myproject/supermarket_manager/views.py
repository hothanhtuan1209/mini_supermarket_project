from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from .models import Role
from .constants import ADDED, EXISTS, REQUIRED, INVALID_METHOD, UPDATED, NOT_FOUND
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
                return JsonResponse({"message": ADDED}, status=200)
            except IntegrityError:
                return JsonResponse({"message": EXISTS}, status=400)
        return JsonResponse({"message": REQUIRED}, status=400)

    return JsonResponse({"message": INVALID_METHOD}, status=405)


def list_roles(request):
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
            except Role.DoesNotExist:
                return JsonResponse({"message": NOT_FOUND}, status=404)
        return JsonResponse({"message": REQUIRED}, status=400)

    return JsonResponse({"message": INVALID_METHOD}, status=405)
