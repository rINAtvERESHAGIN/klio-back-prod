from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _

from cities_light.models import City, Country

from contacts.models import Contact
from products.models import Category, Product
from tags.models import Tag

User = get_user_model()


class Basket(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    products = models.ManyToManyField(Product, through='BasketProduct', verbose_name=_('products'),
                                      related_name='baskets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('user'))
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('session'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')

    def __str__(self):
        if self.user:
            return gettext('Basket') + ' #{0} ({1})'.format(self.id, self.user)
        if self.session:
            return gettext('Basket') + ' #{0} ('.format(self.id) + \
                gettext('Anonymous') + ' {0})'.format(self.session.session_key)
        else:
            return gettext('Basket') + ' #{0}'.format(self.id)

    def clean(self):
        if self.user:
            if Basket.objects.filter(user=self.user, user__isnull=False, is_active=True).exclude(pk=self.pk).exists():
                raise ValidationError(_('Active basket for current user already exists.'))
        if self.session:
            if Basket.objects.filter(session=self.session, session__isnull=False,
                                     is_active=True).exclude(pk=self.pk).exists():
                raise ValidationError(_('Active basket already exists.'))


class BasketProduct(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('basket'),
                               related_name='inside')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False, verbose_name=_('product'),
                                related_name='in_basket')
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name=_('price'))
    promo_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2,
                                      verbose_name=_('promo_price'))
    added = models.DateTimeField(auto_now_add=True, verbose_name=_('added'))

    class Meta:
        verbose_name = _('Basket product')
        verbose_name_plural = _('Basket products')
        unique_together = ('basket', 'product')


class Order(models.Model):
    ACTIVE, PENDING, DELIVERY, COMPLETED, DENIED = 'active', 'pending', 'delivery', 'completed', 'denied'
    STATUS_CHOICES = [
        (ACTIVE, _('Order is active')),
        (PENDING, _('Order pending')),
        (DELIVERY, _('Order on delivery')),
        (COMPLETED, _('Order completed')),
        (DENIED, _('Order denied')),
    ]

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    received = models.DateTimeField(blank=True, null=True, verbose_name=_('received'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('user'))
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('session'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE, verbose_name=_('status'))
    is_paid = models.BooleanField(default=False, verbose_name=_('is paid'))
    step = models.PositiveSmallIntegerField(default=1, verbose_name=_('step'))
    promo = models.BooleanField(default=False, verbose_name=_('promo'))
    promo_code = models.CharField(max_length=14, blank=True, verbose_name=_('promo code'))
    private_info = models.OneToOneField('OrderPrivateInfo', on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='order', verbose_name=_('private info'))
    delivery_info = models.OneToOneField('OrderDeliveryInfo', on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='order', verbose_name=_('delivery info'))
    payment_info = models.OneToOneField('OrderPaymentInfo', on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='order', verbose_name=_('payment info'))
    basket = models.OneToOneField('Basket', on_delete=models.CASCADE, null=False, verbose_name=_('basket'),
                                  related_name='order')
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name=_('price'))

    class Meta:
        ordering = ['-created']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return _('Order') + '#{0}'.format(self.id)


class OrderDeliveryInfo(models.Model):
    PICKUP, COURIER, COMPANY = 'pickup', 'courier', 'company'
    DELIVERY_TYPES = [
        (PICKUP, _('Pickup')),
        (COURIER, _('Courier')),
        (COMPANY, _('Transport company')),
    ]

    type = models.CharField(max_length=20, choices=DELIVERY_TYPES, verbose_name=_('type'))
    from_address = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name=_('from address'))
    to_country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,
                                   verbose_name=_('to country'))
    to_city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_('to city'))
    to_address = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('to address'))
    comment = models.TextField(blank=True, null=True, verbose_name=_('comment'))
    delivery_terms = models.BooleanField(default=False, blank=False, verbose_name=_('delivery terms'))
    moscow_terms = models.BooleanField(default=False, blank=False, verbose_name=_('moscow terms'))

    class Meta:
        verbose_name = _('Order Delivery Info')
        verbose_name_plural = _('Order Delivery Data')

    def __str__(self):
        try:
            return gettext('Order') + '#{0}'.format(self.order.id) + ' - ' + gettext('Delivery Info')
        except Order.DoesNotExist:
            return gettext('Delivery Info') + '#{0}'.format(self.id)

    def clean(self):
        current_order_other_delivery = OrderDeliveryInfo.objects.filter(order=self.order).exists()
        if current_order_other_delivery:
            raise ValidationError(_('There is a delivery info for this order already.'))


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
            return gettext('Order') + '#{0}'.format(self.order.id) + ' - ' + gettext('Payment Info')
        except Order.DoesNotExist:
            return gettext('Payment Info') + '#{0}'.format(self.id)

    def clean(self):
        current_order_other_payment = OrderPaymentInfo.objects.filter(order=self.order).exists()
        if current_order_other_payment:
            raise ValidationError(_('There is a payment info for this order already.'))


class OrderPrivateInfo(models.Model):
    INDIVIDUAL, COMPANY = 'individual', 'company'
    CLIENT_TYPES = [
        (INDIVIDUAL, _('Individual')),
        (COMPANY, _('Company')),
    ]

    client_type = models.CharField(max_length=10, choices=CLIENT_TYPES, verbose_name=_('client type'))
    last_name = models.CharField(max_length=64, null=False, blank=False, default=None, verbose_name=_('last name'))
    first_name = models.CharField(max_length=64, null=False, blank=False, default=None, verbose_name=_('first name'))
    middle_name = models.CharField(max_length=128, null=True, blank=True, default=None, verbose_name=_('middle name'))
    phone = models.CharField(max_length=64, null=False, blank=False, default=None, verbose_name=_('phone'))
    email = models.EmailField(blank=False, null=False)
    personal_data = models.BooleanField(default=False, blank=False, verbose_name=_('personal data'))

    class Meta:
        verbose_name = _('Order Private Info')
        verbose_name_plural = _('Order Private Data')

    def __str__(self):
        try:
            return gettext('Order') + '#{0}'.format(self.order.id) + ' – ' + gettext('Private Info')
        except Order.DoesNotExist:
            return gettext('Private Info') + '#{0}'.format(self.id)

    def clean(self):
        current_order_other_private = OrderPrivateInfo.objects.filter(order=self.order).exists()
        if current_order_other_private:
            raise ValidationError(_('There is a private info for this order already.'))


class PromoCode(models.Model):
    PERCENT, FIXED = 'percent', 'fixed'
    DISCOUNT_TYPES = [
        (PERCENT, _('Percentage discount')),
        (FIXED, _('Fixed discount')),
    ]

    code = models.CharField(max_length=20, blank=False, null=False, unique=True, verbose_name=_('code'))
    start_date = models.DateField(verbose_name=_('start date'))
    deadline = models.DateField(verbose_name=_('deadline'))
    categories = models.ManyToManyField(Category, blank=True, related_name='promos', verbose_name=_('categories'))
    products = models.ManyToManyField(Product, blank=True, related_name='promos', verbose_name=_('products'))
    tags = models.ManyToManyField(Tag, blank=True, related_name='promos', verbose_name=_('tags'))
    activity = models.BooleanField(default=False, verbose_name=_('activity'))
    discount_type = models.CharField(choices=DISCOUNT_TYPES, default=PERCENT, max_length=10, blank=True,
                                     verbose_name=_('discount type'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                          verbose_name=_('discount amount'))

    class Meta:
        ordering = ['-activity']
        verbose_name = _('Promo Code')
        verbose_name_plural = _('Promo Codes')

    def __str__(self):
        return self.code
