# Generated by Django 4.2.4 on 2023-09-18 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supermarket_manager", "0022_rename_birth_day_account_birthday_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="account",
            old_name="id",
            new_name="account_id",
        ),
        migrations.RenameField(
            model_name="account",
            old_name="birthday",
            new_name="birth_day",
        ),
        migrations.RenameField(
            model_name="account",
            old_name="role",
            new_name="role_id",
        ),
        migrations.RenameField(
            model_name="permission",
            old_name="id",
            new_name="permission_id",
        ),
        migrations.RenameField(
            model_name="permission",
            old_name="name",
            new_name="permission_name",
        ),
        migrations.RenameField(
            model_name="role",
            old_name="id",
            new_name="role_id",
        ),
        migrations.RenameField(
            model_name="role",
            old_name="name",
            new_name="role_name",
        ),
        migrations.RenameField(
            model_name="role_permission",
            old_name="permission",
            new_name="permission_id",
        ),
        migrations.RenameField(
            model_name="role_permission",
            old_name="role",
            new_name="role_id",
        ),
        migrations.RenameField(
            model_name="role_permission",
            old_name="id",
            new_name="role_permission_id",
        ),
        migrations.AddField(
            model_name="role",
            name="status",
            field=models.CharField(
                choices=[("Active", "Active"), ("Disabled", "Disabled")],
                default="Active",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="permission",
            name="status",
            field=models.CharField(
                choices=[("Active", "Active"), ("Disabled", "Disabled")],
                default="Active",
                max_length=10,
            ),
        ),
    ]
