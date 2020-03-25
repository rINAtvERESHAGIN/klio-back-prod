from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from cities_light.models import City, Country

from contacts.models import Contact
from products.models import Product

User = get_user_model()


class Basket(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    # session = models.ForeignKey()
    products = models.ManyToManyField(Product, through='BasketProduct', verbose_name=_('products'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('user'))
    active = models.BooleanField(default=True, verbose_name=_('active'))

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')

    def __str__(self):
        return _('Basket') + '#{0} ({1})'.format(self.id, self.user.__str__())


class BasketProduct(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('basket'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('product'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))
    added = models.DateTimeField(auto_now_add=True, verbose_name=_('added'))

    class Meta:
        verbose_name = _('Basket product')
        verbose_name_plural = _('Basket products')


class Order(models.Model):
    ACTIVE, PENDING, COMPLETED, DENIED = 'active', 'pending', 'completed', 'denied'
    STATUS_CHOICES = [
        (ACTIVE, _('Order is active')),
        (PENDING, _('Order pending')),
        (COMPLETED, _('Order completed')),
        (DENIED, _('Order denied')),
    ]

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('user'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name=_('status'))
    step = models.PositiveSmallIntegerField(default=1, verbose_name=_('step'))
    promo = models.BooleanField(default=False, verbose_name=_('promo'))
    promo_code = models.CharField(max_length=14, blank=True, verbose_name=_('promo code'))
    private_info = models.OneToOneField('OrderPrivateInfo', on_delete=models.CASCADE, null=False,
                                        related_name='order', verbose_name=_('private info'))
    delivery_info = models.OneToOneField('OrderDeliveryInfo', on_delete=models.CASCADE, null=False,
                                         related_name='order', verbose_name=_('delivery info'))
    payment_info = models.OneToOneField('OrderPaymentInfo', on_delete=models.CASCADE, null=False,
                                        related_name='order', verbose_name=_('payment info'))
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, null=False, verbose_name=_('basket'))

    class Meta:
        ordering = ['-created']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return _('Order') + '#{0}'.format(self.id)


class OrderPrivateInfo(models.Model):
    INDIVIDUAL, COMPANY = 'individual', 'company'
    CLIENT_TYPES = [
        (INDIVIDUAL, _('Individual')),
        (COMPANY, _('Company')),
    ]

    client_type = models.CharField(max_length=10, choices=CLIENT_TYPES, verbose_name=_('client type'))
    last_name = models.CharField(max_length=64, null=True, blank=False, default=None, verbose_name=_('last name'))
    first_name = models.CharField(max_length=64, null=True, blank=False, default=None, verbose_name=_('first name'))
    middle_name = models.CharField(max_length=128, null=True, blank=True, default=None, verbose_name=_('middle name'))
    phone = models.CharField(max_length=64, null=True, blank=False, default=None, verbose_name=_('phone'))
    email = models.EmailField()
    personal_data = models.BooleanField(default=False, blank=False, verbose_name=_('personal data'))

    class Meta:
        verbose_name = _('Order Private Info')
        verbose_name_plural = _('Order Private Data')

    def __str__(self):
        try:
            return _('Order') + '#{0}'.format(self.order.id) + ' – ' + _('Private Info')
        except Order.DoesNotExist:
            return _('Private Info') + '#{0}'.format(self.id)


class OrderDeliveryInfo(models.Model):
    PICKUP, COURIER = 'pickup', 'courier'
    DELIVERY_TYPES = [
        (PICKUP, _('Pickup')),
        (COURIER, _('Courier')),
    ]

    type = models.CharField(max_length=10, choices=DELIVERY_TYPES, verbose_name=_('type'))
    from_address = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name=_('from address'))
    to_country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name=_('to country'))
    to_city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name=_('to city'))
    to_address = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('to address'))
    comment = models.TextField(blank=True, verbose_name=_('comment'))
    delivery_terms = models.BooleanField(default=False, blank=False, verbose_name=_('delivery terms'))

    class Meta:
        verbose_name = _('Order Delivery Info')
        verbose_name_plural = _('Order Delivery Data')

    def __str__(self):
        try:
            return _('Order') + '#{0}'.format(self.order.id) + ' - ' + _('Delivery Info')
        except Order.DoesNotExist:
            return _('Delivery Info') + '#{0}'.format(self.id)


class OrderPaymentInfo(models.Model):
    CASH, CARD, TRANSFER = 'cash', 'card', 'transfer'
    PAYMENT_CHOICES = [
        (CASH, _('Cash')),
        (CARD, _('Plastic Card')),
        (TRANSFER, _('Wire transfer')),
    ]

    type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, verbose_name=_('type'))

    class Meta:
        verbose_name = _('Order Payment Info')
        verbose_name_plural = _('Order Payment Data')

    def __str__(self):
        try:
            return _('Order') + '#{0}'.format(self.order.id) + ' - ' + _('Payment Info')
        except Order.DoesNotExist:
            return _('Payment Info') + '#{0}'.format(self.id)


class PromoCode(models.Model):
    code = models.CharField(max_length=20, blank=False, null=False, verbose_name=_('code'))
    start_date = models.DateField(verbose_name=_('start date'))
    deadline = models.DateField(verbose_name=_('deadline'))
    activity = models.BooleanField(default=False, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity']
        verbose_name = _('Promo Code')
        verbose_name_plural = _('Promo Codes')

    def __str__(self):
        return self.code
