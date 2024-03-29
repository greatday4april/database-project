"""car_dealer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from rest_framework import routers
from django.urls import path, include
from django.views.generic.base import RedirectView
from car_dealer import views

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet, 'customer')
router.register(r'bills', views.PurchaseBillViewSet, 'bill')
router.register(r'service_appointments', views.ServiceAppointmentViewSet, 'service_appointment')
router.register(r'service_items',
                views.ServiceItemViewSet, 'service_item')
router.register(r'sale_stats', views.SaleStatsViewSet, basename='sale_stat')

urlpatterns = [
    path('', RedirectView.as_view(url='api/')),
    path('api/', include(router.urls)),
    path('__debug__/', include(debug_toolbar.urls)),
]
