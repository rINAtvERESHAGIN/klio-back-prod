import json
from decimal import Decimal
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import Basket, BasketProduct, Order, OrderDeliveryInfo, OrderPaymentInfo, OrderPrivateInfo, PromoCode
from .serializers import (BasketDetailSerializer, OrderDeliveryInfoSerializer, OrderDetailSerializer,
                          OrderDetailShortSerializer, OrderListSerializer, OrderPaymentInfoSerializer,
                          OrderPrivateInfoSerializer)


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

        order.status = Order.PENDING
        order.received = timezone.localtime()
        order.save()
        serializer = self.serializer_class(order, context={'request': self.request})
        return Response(serializer.data)


class OrderActiveUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        new_step = data.get('step')
        promocode = data.get('promocode', None)

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            current_session = Session.objects.get(session_key=self.request.session.session_key)
            order = get_object_or_404(Order, session=current_session, status=Order.ACTIVE)

        if promocode:
            # Check promocode first
            promo_active = PromoCode.objects.filter(activity=True, code=promocode)\
                .exclude(start_date__isnull=False, start_date__gt=timezone.localtime())\
                .exclude(deadline__isnull=False, deadline__lt=timezone.localtime())\
                .first()

            # Find suitable products in basket
            if promo_active:
                order.promo = True
                order.promo_code = promo_active.code
                suitable_categories_ids = promo_active.categories.values_list('id', flat=True)
                suitable_tags_ids = promo_active.tags.values_list('id', flat=True)
                suitable_products_ids = promo_active.products.values_list('id', flat=True)
                promo_basket_products = order.basket.inside.filter(Q(
                    product__activity=True, product__in=suitable_products_ids
                ) | Q(
                    product__activity=True, product__category__in=suitable_categories_ids
                ) | Q(
                    product__activity=True, product__tags__in=suitable_tags_ids
                )
                ).distinct()

                # Calculate and save sum to order
                discounted_sum = 0
                if promo_basket_products:
                    for basket_product in promo_basket_products:
                        if promo_active.discount_type == 'percent':
                            basket_product.price = str(
                                round(basket_product.price * (1 - promo_active.discount_amount / 100), 2)
                            )
                        elif promo_active.special.discount_type == 'fixed':
                            basket_product.price = round(basket_product.price - promo_active.discount_amount, 2)

                        discounted_sum += (Decimal(basket_product.price) * basket_product.quantity)

                    basket_products = order.basket.inside.exclude(
                        id__in=promo_basket_products.values_list('id', flat=True))

                    sum_price = 0
                    for basket_product in basket_products:
                        sum_price += (basket_product.quantity * basket_product.price)

                    if discounted_sum:
                        sum_price += discounted_sum

                    order.price = sum_price

            else:
                return Response({'promocode': _('Promocode is not valid.')}, status=HTTP_400_BAD_REQUEST)

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
            new_payment_info = serializer.create(validated_data=serializer.validated_data)
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
