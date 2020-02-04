from django.db import models

from cities_light.models import City, Country

from contacts.models import Contact
from products.models import Product
from users.models import User


class Basket(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # session = models.ForeignKey()
    product = models.ManyToManyField(Product, through='BasketProduct')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Basket #{0} ({1})'.format(self.id, self.user.__str__())


class BasketProduct(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=1)
    added = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    ACTIVE, PENDING, COMPLETED, DENIED = 'active', 'pending', 'completed', 'denied'
    STATUS_CHOICES = [
        (ACTIVE, 'Order is active'),
        (PENDING, 'Order pending'),
        (COMPLETED, 'Order completed'),
        (DENIED, 'Order denied'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    step = models.PositiveSmallIntegerField(default=1)
    promo = models.BooleanField(default=False)
    promo_code = models.CharField(max_length=14, blank=True)
    private_info = models.OneToOneField('OrderPrivateInfo', on_delete=models.CASCADE, null=False)
    delivery_info = models.OneToOneField('OrderDeliveryInfo', on_delete=models.CASCADE, null=False)
    payment_info = models.OneToOneField('OrderPaymentInfo', on_delete=models.CASCADE, null=False)
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return 'Order #{0}'.format(self.id)


class OrderPrivateInfo(models.Model):
    INDIVIDUAL, COMPANY = 'individual', 'company'
    CLIENT_TYPES = [
        (INDIVIDUAL, 'Individual'),
        (COMPANY, 'Company'),
    ]

    client_type = models.CharField(max_length=10, choices=CLIENT_TYPES)
    last_name = models.CharField(max_length=64, null=True, blank=False, default=None)
    first_name = models.CharField(max_length=64, null=True, blank=False, default=None)
    middle_name = models.CharField(max_length=128, null=True, blank=True, default=None)
    phone = models.CharField(max_length=64, null=True, blank=False, default=None)
    email = models.EmailField()
    personal_data = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return 'Order #{0} - Private Info'.format(self.id)


class OrderDeliveryInfo(models.Model):
    PICKUP, COURIER = 'pickup', 'courier'
    DELIVERY_TYPES = [
        (PICKUP, 'Pickup'),
        (COURIER, 'Courier'),
    ]

    type = models.CharField(max_length=10, choices=DELIVERY_TYPES)
    from_address = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False, blank=False)
    to_country = models.ForeignKey(Country, on_delete=models.PROTECT)
    to_city = models.ForeignKey(City, on_delete=models.PROTECT)
    comment = models.TextField(blank=True)
    delivery_terms = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return 'Order #{0} - Delivery Info'.format(self.order.id)


class OrderPaymentInfo(models.Model):
    CASH, CARD, TRANSFER = 'cash', 'card', 'transfer'
    PAYMENT_CHOICES = [
        (CASH, 'Cash'),
        (CARD, 'Plastic Card'),
        (TRANSFER, 'Wire transfer'),
    ]

    type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)

    def __str__(self):
        return 'Order #{0} - Payment Info'.format(self.order.id)


class PromoCode(models.Model):
    code = models.CharField(max_length=20, blank=False, null=False)
    start_date = models.DateField()
    deadline = models.DateField()
    activity = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['-activity']
