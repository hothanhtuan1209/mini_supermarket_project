from django.core.management.base import BaseCommand
from supermarket_manager.models import Permission

class Command(BaseCommand):
    help = "Create custom permission"

    def handle(self, *args, **kwargs):
        permission_need_create = [
            ('Read', 'permission to read data'),
            ('Update', 'permission to update data'),
            ('Create', 'permission to create data'),
            ('Delete', 'permission to delete data')
        ]

        for permission_name, description in permission_need_create:
            permission, created = Permission.objects.get_or_create(
                permission_name=permission_name,
                defaults={'description': description}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Permission {permission_name} created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Permission {permission_name} already exists'))

            self.stdout.write(self.style.SUCCESS(f'ID: {permission.id}, Name: {permission.permission_name}'))
