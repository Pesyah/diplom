from django.urls import path
from .views import create_order, ServiceOrderDetailView

urlpatterns = [
    path('service/createOrder', create_order),
    path('service/order/<int:pk>/', ServiceOrderDetailView.as_view(), name='service_order_detail'),
]