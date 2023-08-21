from django.urls import path
from .views import add_role

urlpatterns = [path("api/roles/add", add_role, name="add-role")]
