# Create your views here.

from rest_framework.filters import BaseFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.views import APIView

from car_dealer.serializers import CustomerSerializer, PurchaseBillSerializer, ServiceAppointmentSerializer, ServiceItemSerializer, SaleStatsSerializer
from car_dealer.models import Customer, PurchaseBill, ServiceAppointment, ServicePerformed


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class PurchaseBillViewSet(viewsets.ModelViewSet):
    queryset = PurchaseBill.objects.all()
    serializer_class = PurchaseBillSerializer


class ServiceAppointmentViewSet(viewsets.ModelViewSet):
    queryset = ServiceAppointment.objects.all()
    serializer_class = ServiceAppointmentSerializer


class ServiceItemViewSet(viewsets.ModelViewSet):
    queryset = ServicePerformed.objects.all()
    serializer_class = ServiceItemSerializer


class SaleStatsViewSet(viewsets.ViewSet):
    serializer_class = SaleStatsSerializer

    def list(self, request):
        return Response(PurchaseBillSerializer(instance=PurchaseBill.objects.all(), many=True).data, status.HTTP_200_OK)

    def create(self, request):
        begin_date = request.data.get('begin_date')
        end_date = request.data.get('end_date')

        bills = PurchaseBill.objects.filter(date__gte=begin_date).filter(date__lte=end_date)
        return Response(SaleStatsSerializer(instance=bills).data, status.HTTP_200_OK)
