from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=30)),
                ("address", models.TextField()),
                ("notes", models.TextField(blank=True)),
                ("total", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(choices=[("new", "New"), ("confirmed", "Confirmed"), ("delivered", "Delivered"), ("cancelled", "Cancelled")], default="new", max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_name", models.CharField(max_length=160)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("qty", models.PositiveIntegerField(default=1)),
                ("line_total", models.DecimalField(decimal_places=2, max_digits=10)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="orders.order")),
            ],
        ),
    ]
