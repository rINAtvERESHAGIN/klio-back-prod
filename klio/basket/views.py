import json
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.exceptions import ValidationError
from django.http import HttpResponse
from products.models import Product
from .models import Basket, BasketProduct, Order, OrderDeliveryInfo, OrderPaymentInfo, OrderPaymentB2PInfo, \
    OrderPrivateInfo, PromoCode
from .serializers import (BasketDetailSerializer, OrderDeliveryInfoSerializer, OrderDetailSerializer,
                          OrderDetailShortSerializer, OrderListSerializer, OrderPaymentInfoSerializer,
                          OrderPrivateInfoSerializer, OrderPaymentInfoB2PSerializer)


class BasketAddProductView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = BasketDetailSerializer

    def create(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        amount = request.data.get('amount')
        price = request.data.get('price')

        if not self.request.user.is_anonymous:
            basket, _ = Basket.objects.get_or_create(user=self.request.user, is_active=True)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            basket, _ = Basket.objects.get_or_create(session=current_session, is_active=True)

        product_in_basket, created = BasketProduct.objects.get_or_create(basket=basket, product_id=product_id)

        if amount == 1:
            if not created:
                product_in_basket.quantity += 1
        else:
            product_in_basket.quantity = amount
        product_in_basket.price = price
        product_in_basket.save()
        serializer = self.serializer_class(basket, context={'request': self.request})
        return Response(serializer.data)


class BasketDeleteProductView(DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = BasketDetailSerializer

    def destroy(self, request, *args, **kwargs):
        product_id = self.kwargs.get('id')

        if not self.request.user.is_anonymous:
            basket = get_object_or_404(Basket, user=self.request.user, is_active=True)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            basket = get_object_or_404(Basket, session=current_session, is_active=True)

        instance = get_object_or_404(BasketProduct, basket=basket, product_id=product_id)
        self.perform_destroy(instance)
        serializer = self.serializer_class(basket, context={'request': self.request})
        return Response(serializer.data)


class BasketUpdateProductView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = BasketDetailSerializer

    def update(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        amount = request.data.get('amount')
        price = request.data.get('price')

        if not self.request.user.is_anonymous:
            basket = get_object_or_404(Basket, user=self.request.user, is_active=True)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            basket = get_object_or_404(Basket, session=current_session, is_active=True)

        product_in_basket = get_object_or_404(BasketProduct, basket=basket, product_id=product_id)
        product_in_basket.quantity = amount
        product_in_basket.price = price
        product_in_basket.save()
        serializer = self.serializer_class(basket, context={'request': self.request})
        return Response(serializer.data)


class CurrentBasketView(RetrieveAPIView):
    serializer_class = BasketDetailSerializer

    def get_object(self):
        if not self.request.user.is_anonymous:
            return get_object_or_404(Basket, user=self.request.user, is_active=True)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            return get_object_or_404(Basket, session=current_session, is_active=True)


class CurrentBasketInactivateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = BasketDetailSerializer

    def update(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            basket = get_object_or_404(Basket, user=self.request.user, is_active=True)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            basket = get_object_or_404(Basket, session=current_session, is_active=True)

        basket.is_active = False
        basket.save()

        serializer = self.serializer_class(basket, context={'request': self.request})
        return Response(serializer.data)


class OrderCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def create(self, request, *args, **kwargs):

        # Check active basket first
        if not self.request.user.is_anonymous:
            basket = get_object_or_404(Basket, user=self.request.user, is_active=True)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            basket = get_object_or_404(Basket, session=current_session, is_active=True)

        # Check and create order
        if not self.request.user.is_anonymous:
            order, _ = Order.objects.get_or_create(user=self.request.user, basket=basket, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            order, _ = Order.objects.get_or_create(session=current_session, basket=basket, status=Order.ACTIVE)

        serializer = self.serializer_class(order, context={'request': self.request})
        return Response(serializer.data)


class OrderActiveRetrieveView(RetrieveAPIView):
    serializer_class = OrderDetailSerializer

    def get_object(self):
        if not self.request.user.is_anonymous:
            return get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            return get_object_or_404(Order, session=current_session, status=Order.ACTIVE)
            # return get_object_or_404(Order, session=current_session, status=Order.PENDING)


class OrderPendingRetrieveView(RetrieveAPIView):
    serializer_class = OrderDetailSerializer

    def get_object(self):
        if not self.request.user.is_anonymous:
            return get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            return get_object_or_404(Order, session=current_session, status=Order.PENDING)


class OrderActiveToPendingView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailShortSerializer

    def update(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            order = get_object_or_404(Order, session=current_session, status=Order.ACTIVE)

        if not order.price:
            sum_price = 0
            for basket_product in order.basket.inside.all():
                sum_price += (basket_product.quantity * basket_product.price)
            order.price = sum_price

        if order.payment_info.type == order.payment_info.CARD:
            try:
                OrderPaymentB2PInfo.make_register_request(payment_info=order.payment_info)
            except Exception as exception:
                print(exception)
                return HttpResponse(status=400)

        order.status = Order.PENDING
        order.received = timezone.localtime()
        order.save()

        order.send_notification_to_admins()
        order.send_notification_to_customer()
        serializer = self.serializer_class(order, context={'request': self.request})
        return Response(serializer.data)


# order/active/update
class OrderActiveUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def update(self, request, *args, **kwargs):
        # Get data
        data = json.loads(request.body.decode('utf-8'))
        new_step = data.get('step')
        promocode = data.get('promocode', None)

        # Check if step param is provided
        if not new_step:
            return Response(_('Order step is not provided'), status=HTTP_400_BAD_REQUEST)

        def check_promo_code(code):
            promo = PromoCode.objects.filter(activity=True, code=code) \
                .exclude(start_date__isnull=False, start_date__gt=timezone.localtime()) \
                .exclude(deadline__isnull=False, deadline__lt=timezone.localtime()) \
                .first()
            return promo

        def get_promo_basket_products(order_obj, promo_obj):
            promo_products = order_obj.basket.inside.filter(
                product__activity=True, product__kind__in=[Product.UNIQUE, Product.CHILD]
            ).filter(Q(
                product__in=promo_obj.products.values_list('id', flat=True)
            ) | Q(
                product__category__in=promo_obj.categories.values_list('id', flat=True)
            ) | Q(
                product__tags__in=promo_obj.tags.values_list('id', flat=True)
            )
            ).distinct()
            return promo_products

        def recalculate_basket_products_promo_prices(promo_bps, promo_obj):
            for bp in promo_bps:

                if promo_obj.discount_type == 'percent':
                    bp.promo_price = round(
                        bp.price * (1 - promo_obj.discount_amount / 100), 2)

                elif promo_obj.special.discount_type == 'fixed':
                    bp.promo_price = round(
                        bp.price - promo_obj.discount_amount, 2)

                bp.save()

        # Get order
        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            order = get_object_or_404(Order, session=current_session, status=Order.ACTIVE)

        if promocode:
            # Check promo code first
            promo_active = check_promo_code(promocode)

            if promo_active:
                # If promo code is valid find promo products in basket
                if promo_active.for_all_products:
                    promo_basket_products = order.basket.inside.all()
                else:
                    promo_basket_products = get_promo_basket_products(order, promo_active)

                if promo_basket_products:
                    # Recalculate promo prices for promo products
                    recalculate_basket_products_promo_prices(promo_basket_products, promo_active)

                    order.promo = True
                    order.promo_code = promo_active.code

                else:
                    return Response({'promocode': _('No promo products in the basket.')}, status=HTTP_400_BAD_REQUEST)

            else:
                return Response({'promocode': _('Promocode is not valid.')}, status=HTTP_400_BAD_REQUEST)

        else:
            # Check if order already has a promo and recalculate the promo prices for products
            if order.promo and order.promo_code:

                # Check if promo code is valid
                promo_active = check_promo_code(order.promo_code)

                if promo_active:
                    # For valid promocode find promo products in basket
                    if promo_active.for_all_products:
                        promo_basket_products = order.basket.inside.all()
                    else:
                        promo_basket_products = get_promo_basket_products(order, promo_active)

                    if promo_basket_products:
                        # Recalculate promo prices for promo products
                        recalculate_basket_products_promo_prices(promo_basket_products, promo_active)

                else:
                    # For invalid promocode erase all promo prices for all basket products
                    for basket_product in order.basket.inside.all():
                        basket_product.promo_price = None
                        basket_product.save()

        if new_step == 3:
            # Recalculate the price on the 3rd stage of order process:
            order_price = 0
            for basket_product in order.basket.inside.all():
                product_price = basket_product.promo_price if basket_product.promo_price else basket_product.price
                order_price += product_price * basket_product.quantity
            order.price = order_price

            # Refresh delivery price
            delivery = order.delivery_info
            order_price, delivery_price = 0, 0

            if delivery.type == 'courier':
                # if delivery.to_city.name in ['Moscow', 'Kostroma']:
                if delivery.to_city.name == 'Moscow':
                    for basket_product in order.basket.inside.all():
                        order_price += basket_product.price * basket_product.quantity
                    delivery_price = 500 if order_price < 3000 else 0

                if delivery.to_city.name == 'Saint Petersburg':
                    for basket_product in order.basket.inside.all():
                        order_price += basket_product.price * basket_product.quantity
                    delivery_price = 500 if order_price < 5000 else 0

            delivery.price = delivery_price
            delivery.save()

        order.step = new_step
        order.save()
        serializer = self.serializer_class(order, context={'request': self.request})
        return Response(serializer.data, status=HTTP_200_OK)


class OrderDeliveryInfoCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            order = get_object_or_404(Order, session=current_session, status=Order.ACTIVE)

        if order.delivery_info:
            return Response(_('Order already has a linked delivery info model'), status=HTTP_400_BAD_REQUEST)

        data['order'] = order

        serializer = OrderDeliveryInfoSerializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            new_delivery_info = serializer.create(validated_data=serializer.validated_data)
            order.delivery_info = new_delivery_info
            order.save()

            order_serializer = self.serializer_class(order, context={'request': self.request})
            return Response(order_serializer.data, status=HTTP_200_OK)


class OrderDeliveryInfoUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def update(self, request, *args, **kwargs):
        data = request.data

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            order = get_object_or_404(Order, session=current_session, status=Order.ACTIVE)

        delivery_info = get_object_or_404(OrderDeliveryInfo, order=order)
        serializer = OrderDeliveryInfoSerializer(delivery_info, data=data, partial=True,
                                                 context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            order_serializer = self.serializer_class(order, context={'request': self.request})
            return Response(order_serializer.data, status=HTTP_200_OK)


class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset


class OrderPaymentInfoCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            order = get_object_or_404(Order, session=current_session, status=Order.ACTIVE)

        if order.payment_info:
            return Response(_('Order already has a linked payment info model'), status=HTTP_400_BAD_REQUEST)

        data['order'] = order

        serializer = OrderPaymentInfoSerializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            new_payment_info: OrderPaymentInfo = serializer.create(validated_data=serializer.validated_data)
            order.payment_info = new_payment_info
            order.save()
            order_serializer = self.serializer_class(order, context={'request': self.request})
            return Response(order_serializer.data, status=HTTP_200_OK)


class OrderPaymentInfoUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def update(self, request, *args, **kwargs):
        data = request.data

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            order = get_object_or_404(Order, session=current_session, status=Order.ACTIVE)

        payment_info = get_object_or_404(OrderPaymentInfo, order=order)
        serializer = OrderPaymentInfoSerializer(payment_info, data=data, partial=True,
                                                context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            order_serializer = self.serializer_class(order, context={'request': self.request})
            return Response(order_serializer.data, status=HTTP_200_OK)


class OrderPaymentB2PInfoGetRedirectToPayView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderPaymentInfoB2PSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['id'])
        payment_info = get_object_or_404(OrderPaymentInfo, order=order)
        serializer: OrderPaymentInfoB2PSerializer = self.get_serializer(instance=payment_info.b2p)
        return Response({
            **serializer.data,
            "redirect": payment_info.b2p.get_order_b2p_redirected_authorize_url()
        }, status=HTTP_200_OK)


class OrderPaymentB2PInfoChangeStatusUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderPaymentInfoB2PSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs['id'])
        payment_info = get_object_or_404(OrderPaymentInfo, order=order)
        serializer: OrderPaymentInfoB2PSerializer = self.get_serializer(instance=payment_info.b2p, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance=payment_info.b2p, validated_data=serializer.validated_data)
        return Response(serializer.data, status=HTTP_200_OK)


class OrderPrivateInfoCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            order = get_object_or_404(Order, session=current_session, status=Order.ACTIVE)

        if order.private_info:
            return Response(_('Order already has a linked private info model'), status=HTTP_400_BAD_REQUEST)

        data['order'] = order

        serializer = OrderPrivateInfoSerializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            new_private_info = serializer.create(validated_data=serializer.validated_data)
            order.private_info = new_private_info
            order.save()

            order_serializer = self.serializer_class(order, context={'request': self.request})
            return Response(order_serializer.data, status=HTTP_200_OK)


class OrderPrivateInfoUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def update(self, request, *args, **kwargs):
        data = request.data

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            order = get_object_or_404(Order, session=current_session, status=Order.ACTIVE)

        private_info = get_object_or_404(OrderPrivateInfo, order=order)
        serializer = OrderPrivateInfoSerializer(private_info, data=data, partial=True,
                                                context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            order_serializer = self.serializer_class(order, context={'request': self.request})
            return Response(order_serializer.data, status=HTTP_200_OK)
