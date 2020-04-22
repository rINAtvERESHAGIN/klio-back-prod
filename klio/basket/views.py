import json
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import Basket, BasketProduct, Order, OrderDeliveryInfo, OrderPaymentInfo, OrderPrivateInfo
from .serializers import (BasketDetailSerializer, OrderDeliveryInfoSerializer, OrderDetailSerializer,
                          OrderDetailShortSerializer, OrderListSerializer, OrderPaymentInfoSerializer,
                          OrderPrivateInfoSerializer)


class BasketAddProductView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = BasketDetailSerializer

    def create(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        amount = request.data.get('amount')

        if not self.request.user.is_anonymous:
            basket, _ = Basket.objects.get_or_create(user=self.request.user, is_active=True)
        else:
            basket, _ = Basket.objects.get_or_create(session=self.request.session.session_key, is_active=True)

        product_in_basket, created = BasketProduct.objects.get_or_create(basket=basket, product_id=product_id)

        if amount == 1:
            if not created:
                product_in_basket.quantity += 1
        else:
            product_in_basket.quantity = amount
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
            basket = get_object_or_404(Basket, session=self.request.session.session_key, is_active=True)

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

        if not self.request.user.is_anonymous:
            basket = get_object_or_404(Basket, user=self.request.user, is_active=True)
        else:
            basket = get_object_or_404(Basket, session=self.request.session.session_key, is_active=True)

        product_in_basket = get_object_or_404(BasketProduct, basket=basket, product_id=product_id)
        product_in_basket.quantity = amount
        product_in_basket.save()
        serializer = self.serializer_class(basket, context={'request': self.request})
        return Response(serializer.data)


class CurrentBasketView(RetrieveAPIView):
    serializer_class = BasketDetailSerializer

    def get_object(self):
        if not self.request.user.is_anonymous:
            return get_object_or_404(Basket, user=self.request.user, is_active=True)
        if self.request.session.session_key:
            return get_object_or_404(Basket, session=self.request.session.session_key, is_active=True)
        raise Http404


class CurrentBasketInactivateView(UpdateAPIView):
    serializer_class = BasketDetailSerializer

    def update(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            basket = get_object_or_404(Basket, user=self.request.user, is_active=True)
        else:
            basket = get_object_or_404(Basket, session=self.request.session.session_key, is_active=True)

        basket.is_active = False
        basket.save()

        serializer = self.serializer_class(basket, context={'request': self.request})
        return Response(serializer.data)


class OrderCreateView(CreateAPIView):
    serializer_class = OrderDetailSerializer

    def create(self, request, *args, **kwargs):

        # Check active basket first
        if not self.request.user.is_anonymous:
            basket = get_object_or_404(Basket, user=self.request.user, is_active=True)
        else:
            basket = get_object_or_404(Basket, session=self.request.session.session_key, is_active=True)

        # Check and create order
        if not self.request.user.is_anonymous:
            order, _ = Order.objects.get_or_create(user=self.request.user, basket=basket, status=Order.ACTIVE)
        else:
            order, _ = Order.objects.get_or_create(session=self.request.session.session_key, status=Order.ACTIVE)

        serializer = self.serializer_class(order, context={'request': self.request})
        return Response(serializer.data)


class OrderActiveRetrieveView(RetrieveAPIView):
    serializer_class = OrderDetailSerializer

    def get_object(self):
        if not self.request.user.is_anonymous:
            return get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        if self.request.session.session_key:
            return get_object_or_404(Order, session=self.request.session.session_key, status=Order.ACTIVE)
        raise Http404


class OrderActiveToPendingView(UpdateAPIView):
    serializer_class = OrderDetailShortSerializer

    def update(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            order = get_object_or_404(Order, session=self.request.session.session_key, status=Order.ACTIVE)

        order.status = Order.PENDING
        order.save()
        serializer = self.serializer_class(order, context={'request': self.request})
        return Response(serializer.data)


class OrderActiveUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        new_step = data['step']

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            order = get_object_or_404(Order, session=self.request.session.session_key, status=Order.ACTIVE)

        order.step = new_step
        order.save()
        serializer = self.serializer_class(order, context={'request': self.request})
        return Response(serializer.data)


class OrderDeliveryInfoCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            order = get_object_or_404(Order, session=self.request.session.session_key, status=Order.ACTIVE)

        if order.delivery_info:
            return Response(_('Order already has a linked delivery info model'), status=HTTP_400_BAD_REQUEST)

        data['order'] = order

        serializer = OrderDeliveryInfoSerializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            new_delivery_info = serializer.create(validated_data=data)
            order.delivery_info = new_delivery_info
            order.save()

            order_serializer = self.serializer_class(order, context={'request': self.request})
            return Response(order_serializer.data, status=HTTP_200_OK)


class OrderDeliveryInfoUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            order = get_object_or_404(Order, session=self.request.session.session_key, status=Order.ACTIVE)

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
        data = json.loads(request.body.decode('utf-8'))

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            order = get_object_or_404(Order, session=self.request.session.session_key, status=Order.ACTIVE)

        if order.payment_info:
            return Response(_('Order already has a linked payment info model'), status=HTTP_400_BAD_REQUEST)

        data['order'] = order

        serializer = OrderPaymentInfoSerializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            new_payment_info = serializer.create(validated_data=data)
            order.payment_info = new_payment_info
            order.save()

            order_serializer = self.serializer_class(order, context={'request': self.request})
            return Response(order_serializer.data, status=HTTP_200_OK)


class OrderPaymentInfoUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            order = get_object_or_404(Order, session=self.request.session.session_key, status=Order.ACTIVE)

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
        data = json.loads(request.body.decode('utf-8'))

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            order = get_object_or_404(Order, session=self.request.session.session_key, status=Order.ACTIVE)

        if order.private_info:
            return Response(_('Order already has a linked private info model'), status=HTTP_400_BAD_REQUEST)

        data['order'] = order

        serializer = OrderPrivateInfoSerializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            new_private_info = serializer.create(validated_data=data)
            order.private_info = new_private_info
            order.save()

            order_serializer = self.serializer_class(order, context={'request': self.request})
            return Response(order_serializer.data, status=HTTP_200_OK)


class OrderPrivateInfoUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderDetailSerializer

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        if not self.request.user.is_anonymous:
            order = get_object_or_404(Order, user=self.request.user, status=Order.ACTIVE)
        else:
            order = get_object_or_404(Order, session=self.request.session.session_key, status=Order.ACTIVE)

        private_info = get_object_or_404(OrderPrivateInfo, order=order)
        serializer = OrderPrivateInfoSerializer(private_info, data=data, partial=True,
                                                context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            order_serializer = self.serializer_class(order, context={'request': self.request})
            return Response(order_serializer.data, status=HTTP_200_OK)
