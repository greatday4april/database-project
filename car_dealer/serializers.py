from typing import DefaultDict
from rest_framework import serializers
from car_dealer.models import Customer, PurchaseBill, Service, ServiceAppointment, ServicePackage, ServicePerformed
import datetime


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class PurchaseBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseBill
        fields = '__all__'


class ServiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePerformed
        fields = '__all__'


class ServiceAppointmentSerializer(serializers.ModelSerializer):
    estimated_time = serializers.SerializerMethodField()
    line_items = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()

    def get_total_cost(self, appt: ServiceAppointment):
        return '${}'.format(sum(line_item['cost'] for line_item in self.get_line_items_impl(appt)))

    def get_line_items(self, appt: ServiceAppointment):
        line_items = self.get_line_items_impl(appt)
        new_line_items = []
        for value in line_items:
            new_line_items.append(value)
            new_line_items[-1]['labor_time'] = str(value['labor_time'])
        return new_line_items

    def get_line_items_impl(self, appt: ServiceAppointment):
        names = appt.service_package.service_names

        services = Service.objects.filter(name__in=names).all()
        services_performed = ServicePerformed.objects.filter(appt=appt)
        line_items = []

        for service in services:
            line_items.append({
                "item": service.name,
                "type": str(service.type),
                "labor_time": service.labor_time,
                "cost": service.cost
            })

        for service_performed in services_performed:
            service = service_performed.service
            line_items.append({
                "item": service.name,
                "type": str(service.type),
                "labor_time": service.labor_time,
                "cost": service.cost
            })

        return line_items

    def get_estimated_time(self, appt: ServiceAppointment):
        labor_times = [
            line_item['labor_time'] for line_item in self.get_line_items_impl(appt)
        ]
        delta = datetime.timedelta()
        for labor_time in labor_times:
            delta += labor_time
        return str(delta)

    class Meta:
        model = ServiceAppointment
        fields = '__all__'


class SaleStatsSerializer(serializers.Serializer):
    stats = serializers.SerializerMethodField(read_only=True)
    begin_date = serializers.DateField(write_only=True)
    end_date = serializers.DateField(write_only=True)

    def get_stats(self, bills):
        numbers = DefaultDict(int)
        profit = DefaultDict(float)
        for bill in bills:
            vehicle = '{} {} {}'.format(bill.vin.year, bill.vin.make, bill.vin.model)
            bill: PurchaseBill = bill
            profit[vehicle] += bill.price
            numbers[vehicle] += 1

        stats = []
        for vin, value in profit.items():
            stats.append({
                'vehicle': vin,
                'profit': value,
                'sale_number': numbers[vin]
            })
        return stats
