# Generated by Django 4.1.2 on 2022-11-17 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_merge_20221115_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='iva',
            field=models.DecimalField(decimal_places=3, max_digits=15),
        ),
    ]
