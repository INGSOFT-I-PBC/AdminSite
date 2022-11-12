# Generated by Django 4.1.2 on 2022-11-11 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0016_provider_provider_bussine_c6ea86_idx_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("PA", "Pendiente aprobacion"),
                    ("CR", "Creado"),
                    ("CA", "Cancelado"),
                    ("CN", "Cambios necesarios"),
                    ("AP", "Aprobado"),
                    ("NG", "Negada"),
                ],
                default="PA",
                max_length=6,
            ),
        ),
    ]