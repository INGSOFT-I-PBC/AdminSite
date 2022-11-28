# Generated by Django 4.1.2 on 2022-11-28 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0025_purchase_aproved_at_role_created_at_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("deleted_at", models.DateTimeField(default=None, null=True)),
                ("product_name", models.CharField(max_length=128)),
                ("summary", models.TextField(blank=True, default="")),
                ("short_description", models.CharField(max_length=256)),
                ("brand_name", models.CharField(max_length=50)),
                (
                    "base_price",
                    models.DecimalField(
                        decimal_places=3,
                        default=0,
                        help_text="The base price or the common price for a product",
                        max_digits=20,
                    ),
                ),
            ],
            options={
                "db_table": "products",
            },
        ),
        migrations.CreateModel(
            name="ProductVariant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("deleted_at", models.DateTimeField(default=None, null=True)),
                ("variant_name", models.CharField(max_length=50)),
                (
                    "sku",
                    models.CharField(
                        help_text="The Stock Keeping Unit code", max_length=128
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=3, default=0, max_digits=20),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="variants",
                        to="api.product",
                    ),
                ),
            ],
            options={
                "db_table": "products_variant",
            },
        ),
        migrations.CreateModel(
            name="VariantMeta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=60)),
                ("value", models.CharField(max_length=60)),
                (
                    "variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="meta",
                        to="api.productvariant",
                    ),
                ),
            ],
            options={
                "db_table": "product_variant_meta",
            },
        ),
        migrations.CreateModel(
            name="ProductProviders",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="providers",
                        to="api.productvariant",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="provided_products",
                        to="api.provider",
                    ),
                ),
            ],
            options={
                "db_table": "product_providers",
            },
        ),
        migrations.CreateModel(
            name="ProductMeta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("value", models.CharField(max_length=50)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="common_props",
                        to="api.product",
                    ),
                ),
            ],
            options={
                "db_table": "product_meta",
            },
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["product_name"], name="products_product_97a29d_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["short_description"], name="products_short_d_3dff02_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="variantmeta",
            index=models.Index(fields=["name"], name="product_var_name_eec70c_idx"),
        ),
        migrations.AddIndex(
            model_name="variantmeta",
            index=models.Index(fields=["value"], name="product_var_value_8157b7_idx"),
        ),
        migrations.AddIndex(
            model_name="productvariant",
            index=models.Index(
                fields=["variant_name"], name="products_va_variant_cc68ed_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="productvariant",
            index=models.Index(fields=["sku"], name="products_va_sku_5451be_idx"),
        ),
        migrations.AddIndex(
            model_name="productvariant",
            index=models.Index(fields=["price"], name="products_va_price_b46f78_idx"),
        ),
        migrations.AddIndex(
            model_name="productmeta",
            index=models.Index(fields=["name"], name="product_met_name_7ff056_idx"),
        ),
        migrations.AddIndex(
            model_name="productmeta",
            index=models.Index(fields=["value"], name="product_met_value_b1d5ef_idx"),
        ),
    ]