# Generated by Django 4.2.4 on 2023-09-03 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("supermarket_manager", "0015_alter_account_account_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_id",
            field=models.CharField(
                max_length=5, primary_key=True, serialize=False, unique=True
            ),
        ),
    ]
