from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name


class ProductDiscountTier(models.Model):
    """خصومات بالكميات (Tiered Discounts) لكل منتج."""
    product = models.ForeignKey(Product, related_name="discount_tiers", on_delete=models.CASCADE)
    min_qty = models.PositiveIntegerField(help_text="الحد الأدنى للكمية لتفعيل الخصم (مثال 2 أو 3)")
    percent_off = models.DecimalField(max_digits=5, decimal_places=2, help_text="نسبة الخصم % (مثال 10 يعني 10%)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["min_qty"]
        unique_together = ("product", "min_qty")

    def __str__(self) -> str:
        return f"{self.product.name} - {self.min_qty}+ => {self.percent_off}%"
