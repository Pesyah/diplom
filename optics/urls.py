from django.urls import path
from .views import OpticsDetailView, OpticsListView, mainPage

urlpatterns = [
    path('', mainPage),
    path('optics/<int:pk>/', OpticsDetailView.as_view(), name='optics_detail'),
    path('optics/', OpticsListView.as_view()),
]