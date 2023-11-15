from django.urls import path
from .views import (
    create_role,
    get_roles,
    update_role,
    delete_role,
    create_permission,
    get_permissions,
    update_permission,
    assign_permission,
    create_account,
    get_account_detail,
    login_account,
    update_account,
    logout,
    get_list_account
)

urlpatterns = [
    path("api/roles/creates", create_role, name="create-role"),
    path("api/roles/get_roles", get_roles, name="get-roles"),
    path("api/roles/updates/<str:role_id>", update_role, name="update-role"),
    path("api/permissions/creates", create_permission, name="create-permission"),
    path('api/permissions/get_permission', get_permissions, name='get-permission'),
    path("api/permissions/updates/<str:permission_id>", update_permission, name="update-permission"),
    path("api/assign-permissions", assign_permission, name="assign-permission"),
    path("api/accounts", create_account, name="create-account"),
    path("api/accounts/<uuid:account_id>", get_account_detail, name="get-account-detail"),
    path("api/logins", login_account, name="login"),
    path("api/accounts/updates/<str:account_id>", update_account, name="update-account"),
    path("api/logouts", logout, name="logout"),
    path("api/accounts/pages/<int:page>", get_list_account, name="lits-accounts")
]
