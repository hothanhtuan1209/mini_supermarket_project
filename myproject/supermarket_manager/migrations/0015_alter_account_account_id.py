# Generated by Django 4.2.4 on 2023-09-03 14:18

from django.db import migrations, models
import supermarket_manager.models

import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("supermarket_manager", "0014_remove_account_login_name_alter_account_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_id",
            field=models.CharField(
                default=uuid.uuid4,
                max_length=5,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
