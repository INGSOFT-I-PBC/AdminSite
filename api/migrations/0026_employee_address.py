# Generated by Django 4.1.1 on 2022-12-02 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_purchase_aproved_at_role_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='address',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
