from django.contrib import admin
from .models import Role, Account, Permission, Role_Permission

admin.site.register(Role)
admin.site.register(Account)
admin.site.register(Permission)
admin.site.register(Role_Permission)
