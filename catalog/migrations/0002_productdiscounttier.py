from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductDiscountTier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("min_qty", models.PositiveIntegerField(help_text="الحد الأدنى للكمية لتفعيل الخصم (مثال 2 أو 3)")),
                ("percent_off", models.DecimalField(decimal_places=2, help_text="نسبة الخصم % (مثال 10 يعني 10%)", max_digits=5)),
                ("is_active", models.BooleanField(default=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="discount_tiers", to="catalog.product")),
            ],
            options={
                "ordering": ["min_qty"],
                "unique_together": {("product", "min_qty")},
            },
        ),
    ]
