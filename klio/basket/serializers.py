from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from products.serializers import BasketProductListSerializer
from .models import Basket, Order, OrderDeliveryInfo, OrderPaymentInfo, OrderPrivateInfo


class BasketDetailSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    products = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'created', 'modified', 'products')

    def get_products(self, obj):
        self.context['basket_id'] = obj.id
        return BasketProductListSerializer(obj.products.filter(activity=True), many=True,
                                           read_only=True, context=self.context).data


class OrderDeliveryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDeliveryInfo
        fields = ('type', 'from_address', 'to_country', 'to_city', 'to_address', 'comment', 'delivery_terms')

    def validate_delivery_terms(self, value):
        if not value:
            raise serializers.ValidationError(_('You must agree to the delivery terms.'))
        return value


class OrderPaymentInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderPaymentInfo
        fields = ('type',)


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
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    delivery_info = OrderDeliveryInfoSerializer()
    modified = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    payment_info = OrderPaymentInfoSerializer()
    private_info = OrderPrivateInfoSerializer()

    class Meta:
        model = Order
        fields = ('id', 'created', 'modified', 'status', 'step', 'promo', 'promo_code', 'private_info', 'delivery_info',
                  'payment_info', 'basket')


class OrderDetailShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'created', 'modified', 'status')


class OrderListSerializer(serializers.ModelSerializer):
    basket = BasketDetailSerializer()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Order
        fields = ('id', 'created', 'modified', 'status', 'promo', 'basket')
