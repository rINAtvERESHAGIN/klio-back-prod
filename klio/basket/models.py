import requests
from xml.etree import ElementTree
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from cities_light.models import City, Country

from config.b2p_utils import get_sector, generate_signature, get_authorize_url, get_register_url, get_fail_url, get_success_url
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
    to_city = models.ForeignKey(City, on_delete=models.PROTECT, null=False, blank=False, verbose_name=_('to city'))
    to_address = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('to address'))
    comment = models.TextField(blank=True, null=True, verbose_name=_('comment'))
    price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2, verbose_name=_('price'))
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

#
class OrderPaymentB2PInfo(models.Model):
    B2P_PROGRESS, B2P_FAIL, B2P_SUCCESS = 'progress', 'fail', 'success'
    B2P_ORDER_STATUS_CHOICES = [
        (B2P_PROGRESS, _('In progress')),
        (B2P_FAIL, _('Fail')),
        (B2P_SUCCESS, _('Success')),
    ]

    payment_info = models.OneToOneField(to=OrderPaymentInfo, on_delete=models.CASCADE, related_name='b2p')
    b2p_order_number = models.CharField(max_length=100, verbose_name=_('best2pay order number'))# default='0'
    b2p_order_register_status = models.CharField(max_length=10, choices=B2P_ORDER_STATUS_CHOICES, default=B2P_PROGRESS,
                                        verbose_name=_('best2pay order register status'))
    b2p_order_status = models.CharField(max_length=10, choices=B2P_ORDER_STATUS_CHOICES, default=B2P_PROGRESS,
                                        verbose_name=_('best2pay order status'))
    b2p_last_operation_number = models.IntegerField(verbose_name=_('best2pay last ended operation number'), default=-1)
    b2p_last_operation_code = models.IntegerField(verbose_name=_('best2pay last ended operation result code'), default=-1)

    class Meta:
        verbose_name = _('Order B2P Registered Payment Info')
        verbose_name_plural = _('Order B2P Registered Payment Data')

    def __str__(self):
        try:
            return gettext('Order') + '#{0}'.format(self.payment_info.order.id) + ' - ' + gettext('Payment Info')
        except Order.DoesNotExist:
            return gettext('Payment Info') + '#{0}'.format(self.id)

    @staticmethod
    def get_order_b2p_register_data(payment_info: OrderPaymentInfo):
        return {
            'amount': int(payment_info.order.price * 100),
            'currency': 643,
            'reference': payment_info.order.id,
            'description': f'Оплата заказа №{payment_info.order.id} на сайте kliogem.ru',
            'sector': get_sector(),
            'url': get_success_url(payment_info.order.id),
            'failurl': get_fail_url(payment_info.order.id),
            'email': payment_info.order.private_info.email,
            'phone': payment_info.order.private_info.phone,
            'signature': generate_signature([int(payment_info.order.price * 100), 643]),
            'first_name': payment_info.order.private_info.first_name,
            'last_name': payment_info.order.private_info.last_name
        }

    @staticmethod
    def get_order_b2p_register_url():
        return f'{get_register_url()}'

    def get_order_b2p_redirected_authorize_url(self):
        return f'{get_authorize_url()}?' \
               f'sector={get_sector()}&' \
               f'id={self.payment_info.b2p.b2p_order_number}&' \
               f'signature={generate_signature([self.payment_info.b2p.b2p_order_number]).decode("utf-8")}'

    @classmethod
    def make_register_request(cls, payment_info: OrderPaymentInfo):
        # if created.type == OrderPaymentInfo.CARD:
        if not hasattr(payment_info, 'order'):
            raise AttributeError('Can make processing registration request to non ordered payment info')
        resp = requests.post(
            url=cls.get_order_b2p_register_url(),
            data=cls.get_order_b2p_register_data(payment_info)
        )
        if hasattr(payment_info, 'b2p'):
            self = payment_info.b2p
        else:
            self = None
        if resp.status_code == 200:
            data = ElementTree.fromstring(resp.content)
            if self is None:
                self = cls.objects.create(
                    payment_info=payment_info,
                    b2p_order_register_status=cls.B2P_SUCCESS,
                    b2p_order_number=data.findall('id')[0].text
                )
            else:
                self.b2p_order_register_status = cls.B2P_SUCCESS
                self.b2p_order_number = data.findall('id')[0].text
                self.save()
        else:
            if self is None:
                self = cls.objects.create(
                    payment_info=payment_info,
                    b2p_order_register_status=cls.B2P_FAIL,
                    b2p_order_number='None'
                )
            else:
                self.b2p_order_register_status = cls.B2P_FAIL
                self.b2p_order_number = 'None'
                self.save()
        return self


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
    for_all_products = models.BooleanField(default=False, blank=True, verbose_name=_('For all products'))
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
