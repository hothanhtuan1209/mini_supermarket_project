from django.urls import path
from .views import (
    add_role,
    get_roles,
    update_role,
    delete_role,
)

urlpatterns = [
    path("api/roles/adds", add_role, name="add-role"),
    path("api/roles/get_roles", get_roles, name="get-roles"),
    path("api/roles/updates/<str:role_id>", update_role, name="update-role"),
    path("api/roles/<str:role_id>", delete_role, name="delete-role"),
]
