from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from .models import Role
from .constants import ADDED, EXISTS, REQUIRED, INVALID_METHOD
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
