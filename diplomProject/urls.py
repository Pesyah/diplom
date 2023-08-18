"""
URL configuration for diplomProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from optics.urls import urlpatterns as opticsUrlPatterns
from orders_on_optic.urls import urlpatterns as orders_on_opticUrlPatterns
from orders_on_services.urls import urlpatterns as orders_on_serviceUrlPatterns
from services.urls import urlpatterns as servicesUrlPatterns

from django.shortcuts import redirect 
 

urlpatterns = [
    path('admin/', admin.site.urls),
    *opticsUrlPatterns,
    *servicesUrlPatterns,
    *orders_on_opticUrlPatterns,
    *orders_on_serviceUrlPatterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)