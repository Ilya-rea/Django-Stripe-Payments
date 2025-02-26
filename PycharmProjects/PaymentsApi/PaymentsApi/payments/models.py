from django.db import models

class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'US Dollar'),
        ('eur', 'Euro'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.name} ({self.currency.upper()})"


class Discount(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_coupon_id = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.name} - {self.amount}"


class Tax(models.Model):
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_tax_id = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return f"{self.name} - {self.percentage}%"


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    paid = models.BooleanField(default=False)
    currency = models.CharField(max_length=3, choices=Item.CURRENCY_CHOICES, default='usd')

    @property
    def total_price(self):
        total = sum(item.price for item in self.items.all())

        if self.discount:
            total -= self.discount.amount

        if self.tax:
            total += total * (self.tax.percentage / 100)

            return round(total, 2)


    def __str__(self):
        return f"Order {self.id} - {self.currency.upper()} - Total: {self.total_price}"