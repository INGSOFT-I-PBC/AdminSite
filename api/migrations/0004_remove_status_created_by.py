# Generated by Django 4.1 on 2022-10-09 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_rename_inventorymodel_inventory_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="status",
            name="created_by",
        ),
    ]
