from django.urls import path
from .views import (
    add_role,
    get_roles,
    update_role,
    delete_role,
    add_permission,
    get_permissions,
    update_permission,
    assign_permission,
    add_account,
    get_account_detail,
    login_account,
    update_account,
    change_password
)

urlpatterns = [
    path("api/roles/adds", add_role, name="add-role"),
    path("api/roles/get_roles", get_roles, name="get-roles"),
    path("api/roles/updates/<str:role_id>", update_role, name="update-role"),
    path("api/roles/<str:role_id>", delete_role, name="delete-role"),
    path("api/permissions/adds", add_permission, name="add-permission"),
    path('api/permissions/get_permission', get_permissions, name='get-permission'),
    path("api/permissions/updates/<str:permission_id>", update_permission, name="update-permission"),
    path("api/assign-permissions", assign_permission, name="assign-permission"),
    path("api/accounts", add_account, name="add-account"),
    path("api/accounts/<str:account_id>", get_account_detail, name="get-account-detail"),
    path("api/logins", login_account, name="login-account"),
    path("api/accounts/updates/<str:account_id>", update_account, name="update-account"),
    path("api/accounts/<str:account_id>/change-password", change_password, name="change password")
]
