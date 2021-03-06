from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from products.models import Product
from products.serializers import BasketProductListSerializer
from .models import Basket, Order, OrderDeliveryInfo, OrderPaymentInfo, OrderPrivateInfo, OrderPaymentB2PInfo


class BasketDetailSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    products = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'created', 'modified', 'products')

    def get_products(self, obj):
        self.context['basket_id'] = obj.id
        return BasketProductListSerializer(
            obj.products.filter(activity=True, kind__in=[Product.UNIQUE, Product.CHILD]),
            many=True, read_only=True, context=self.context
        ).data


class OrderDeliveryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDeliveryInfo
        fields = ('type', 'from_address', 'to_city', 'to_address', 'comment', 'price', 'delivery_terms',
                  'moscow_terms')

    def validate_delivery_terms(self, value):
        if not value:
            raise serializers.ValidationError(_('You must agree to the delivery terms.'))
        return value

    def validate_moscow_terms(self, value):
        if not value:
            raise serializers.ValidationError(
                _('You must agree that you are informed that the order is packaged in Moscow.')
            )
        return value


class OrderPaymentInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderPaymentInfo
        fields = ('type',)


class OrderPaymentInfoB2PSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(source='payment_info.order.id', read_only=True, required=False)
    status = serializers.ChoiceField(choices=OrderPaymentB2PInfo.B2P_ORDER_STATUS_CHOICES, source='b2p_order_status')
    operation = serializers.IntegerField(source='b2p_last_operation_number')
    result_code = serializers.IntegerField(source='b2p_last_operation_code')

    class Meta:
        model = OrderPaymentB2PInfo
        fields = ('order', 'status', 'operation', 'result_code')
        read_only_fields = ('order',)

    def validate_status(self, value):
        if self.instance is not None and self.instance.b2p_order_status == OrderPaymentB2PInfo.B2P_SUCCESS:
            raise serializers.ValidationError(
                _('You cant change status when order is paid.')
            )
        return value

    def update(self, instance, validated_data):
        instance: OrderPaymentB2PInfo = super().update(instance, validated_data)
        if instance.b2p_order_status == OrderPaymentB2PInfo.B2P_SUCCESS:
            instance.payment_info.order.is_paid = True
            instance.payment_info.order.save()
        return instance


class OrderPrivateInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderPrivateInfo
        fields = ('client_type', 'last_name', 'first_name', 'middle_name', 'phone', 'email', 'personal_data')

    def validate_personal_data(self, value):
        if not value:
            raise serializers.ValidationError(_('You must agree to the processing of personal data.'))
        return value


class OrderDetailSerializer(serializers.ModelSerializer):
    basket = BasketDetailSerializer()
    created = serializers.DateTimeField(format="%Y-%m-%d")
    delivery_info = OrderDeliveryInfoSerializer()
    modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    payment_info = OrderPaymentInfoSerializer()
    private_info = OrderPrivateInfoSerializer()

    class Meta:
        model = Order
        fields = ('id', 'created', 'modified', 'status', 'step', 'price', 'promo', 'promo_code', 'private_info',
                  'delivery_info', 'payment_info', 'basket')


class OrderDetailShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'created', 'modified', 'status')


class OrderListSerializer(serializers.ModelSerializer):
    basket = BasketDetailSerializer()
    created = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Order
        fields = ('id', 'created', 'status', 'promo', 'price', 'basket')
