# Create your views here.

from rest_framework import viewsets
# from rest_framework.views import APIView

from car_dealer.serializers import CustomerSerializer, PurchaseBillSerializer
from car_dealer.models import Customer, PurchaseBill


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class PurchaseBillViewSet(viewsets.ModelViewSet):
    queryset = PurchaseBill.objects.all()
    serializer_class = PurchaseBillSerializer
