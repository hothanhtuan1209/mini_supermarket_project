from django.urls import path
from .views import add_role, list_roles, update_role

urlpatterns = [path("api/roles/add", add_role, name="add-role"),
               path('api/roles/list_roles', list_roles, name='list-roles'),
               path("api/roles/update/<str:role_id>", update_role, name="update-role")
]
