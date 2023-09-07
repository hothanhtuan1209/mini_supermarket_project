from django.core.management.base import BaseCommand
from supermarket_manager.models import Role

class Command(BaseCommand):
    help = "Create custom role"

    def handle(self, *args, **kwargs):
        role_names = ["Admin", "Employee"]

        for role_name in role_names:
            role, created = Role.objects.get_or_create(role_name=role_name)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Role {role_name} created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Role {role_name} already exists'))

            self.stdout.write(self.style.SUCCESS(f'ID: {role.role_id}, Name: {role.role_name}'))
