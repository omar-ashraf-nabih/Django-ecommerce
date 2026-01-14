from django.db import models

class Order(models.Model):
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    notes = models.TextField(blank=True)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=30,
        choices=[
            ("new", "New"),
            ("confirmed", "Confirmed"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )

    def __str__(self) -> str:
        return f"Order #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=160)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.product_name} x{self.qty}"
