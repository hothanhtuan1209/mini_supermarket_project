from django.core.management.base import BaseCommand
from supermarket_manager.models import Role, Permission

class Command(BaseCommand):
    help = "Create custom roles and permissions"

    def handle(self, *args, **kwargs):
        role_names = ["Admin", "Employee"]

        for role_name in role_names:
            role, created = Role.objects.get_or_create(role_name=role_name)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Role {role_name} created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Role {role_name} already exists'))

            self.stdout.write(self.style.SUCCESS(f'ID: {role.role_id}, Name: {role.role_name}'))

        permission_to_create = [
            ('Read', 'permission to read data'),
            ('Update', 'permission to update data'),
            ('Create', 'permission to create data'),
            ('Delete', 'permission to delete data')
        ]

        for permission_name, description in permission_to_create:
            permission, created = Permission.objects.get_or_create(
                permission_name=permission_name,
                description=description
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Permission {permission_name} created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Permission {permission_name} already exists'))

            self.stdout.write(self.style.SUCCESS(f'ID: {permission.id}, Name: {permission.permission_name}'))
