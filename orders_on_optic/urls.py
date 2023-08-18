from django.urls import path
from .views import create_order, OpticsOrderDetailView

urlpatterns = [
    path('optics/createOrder', create_order),
    path('optics/order/<int:pk>/', OpticsOrderDetailView.as_view(), name='optics_order_detail'),
]