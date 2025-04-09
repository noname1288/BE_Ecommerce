from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path("", include(router.urls)),
    path("pay/<uuid:order_id>/", OrderViewSet.as_view({'post': 'checkout'}), name="paypal-payment"),
    path("payment-success/", OrderViewSet.as_view({'get': 'payment_success'}), name="payment-success"),
    path("payment-cancel/", OrderViewSet.as_view({'get': 'payment_cancel'}), name="payment-cancel"),
]
