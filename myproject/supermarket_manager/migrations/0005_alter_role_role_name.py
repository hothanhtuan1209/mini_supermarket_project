# Generated by Django 4.2.4 on 2023-08-18 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supermarket_manager", "0004_alter_role_permission_role_permission_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="role_name",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]