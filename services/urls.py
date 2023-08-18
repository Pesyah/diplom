from django.urls import path
from .views import ServicesDetailView, ServicesListView

urlpatterns = [
    path('services/<int:pk>/', ServicesDetailView.as_view(), name='services_detail'),
    path('services/', ServicesListView.as_view()),
]