from django.urls import path

from .views import (BasketAddProductView, BasketDeleteProductView, BasketUpdateProductView, CurrentBasketView,
                    CurrentBasketInactivateView, OrderCreateView, OrderActiveRetrieveView, OrderActiveToPendingView,
                    OrderActiveUpdateView, OrderDeliveryInfoCreateView, OrderDeliveryInfoUpdateView, OrderListView,
                    OrderPaymentInfoCreateView, OrderPaymentInfoUpdateView, OrderPrivateInfoCreateView,
                    OrderPrivateInfoUpdateView, OrderPaymentB2PInfoGetRedirectToPayView,
                    OrderPaymentB2PInfoChangeStatusUpdateView, OrderPendingRetrieveView)

urlpatterns = [
    #
    path('order/active', OrderActiveRetrieveView.as_view(), name='active_order'),
    # в ожидании
    path('order/pending', OrderPendingRetrieveView.as_view(), name='active_order'),
    #
    path('order/active/to-pending', OrderActiveToPendingView.as_view(), name='active_to_pending'),
    #
    path('order/active/update', OrderActiveUpdateView.as_view(), name='active_order_update'),
    #
    path('order/create', OrderCreateView.as_view(), name='create_new_order'),
    #
    path('order/delivery/create', OrderDeliveryInfoCreateView.as_view(), name='order_delivery_create'),
    #
    path('order/delivery/update', OrderDeliveryInfoUpdateView.as_view(), name='order_delivery_update'),
    #
    path('order/list', OrderListView.as_view(), name='orders'),
    #
    path('order/payment/create', OrderPaymentInfoCreateView.as_view(), name='order_payment_create'),
    #
    path('order/payment/update', OrderPaymentInfoUpdateView.as_view(), name='order_payment_update'),
    #
    path('order/payment/<int:id>/processing/redirect', OrderPaymentB2PInfoGetRedirectToPayView.as_view(),
         name='order_payment_b2p_get_redirect'),
    #
    path('order/payment/<int:id>/processing/status', OrderPaymentB2PInfoChangeStatusUpdateView.as_view(),
         name='order_payment_b2p_status_update'),
    #
    path('order/private/create', OrderPrivateInfoCreateView.as_view(), name='order_private_create'),
    #
    path('order/private/update', OrderPrivateInfoUpdateView.as_view(), name='order_private_update'),
    #
    path('current', CurrentBasketView.as_view(), name='current_basket'),
    #
    path('current/inactivate', CurrentBasketInactivateView.as_view(), name='current_basket_inactivate'),
    #
    path('products/<int:id>/add', BasketAddProductView.as_view(), name='basket_product_add'),
    #
    path('products/<int:id>/delete', BasketDeleteProductView.as_view(), name='basket_product_delete'),
    #
    path('products/<int:id>/update', BasketUpdateProductView.as_view(), name='basket_product_update'),
]
