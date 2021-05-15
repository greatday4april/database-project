import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from car_dealer.models import Customer, Service, ServiceAppointment, ServicePackage, ServicePerformed, ServiceType, Vehicle, PurchaseBill

import string
import random
import names
import datetime

from faker import Faker
from faker_vehicle import VehicleProvider


fake = Faker()
fake.add_provider(VehicleProvider)

random.seed(1)


def random_str(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def seed_database():
    ServicePerformed.objects.all().delete()
    ServiceAppointment.objects.all().delete()
    PurchaseBill.objects.all().delete()
    ServicePackage.objects.all().delete()
    Service.objects.all().delete()
    Vehicle.objects.all().delete()
    Customer.objects.all().delete()

    for _i in range(20):
        digits = [digit for digit in string.digits]
        phone_number_str = ''.join([random.choice(digits) for _i in range(10)])
        Customer.objects.create(
            email='{}@gmail.com'.format(random_str(5)),
            name=names.get_full_name(),
            phone_number=phone_number_str,
        )


    for _i in range(100):
        vehicle = fake.vehicle_object()
        cost = random.randint(100, 1000) * 100
        vin = random_str(15)
        Vehicle.objects.create(
            vin=vin,
            cost=cost,
            model=vehicle['Model'],
            make=vehicle['Make'],
            year=vehicle['Year'],
            msrp=cost * (1 + random.random())
        )

    service_names = []
    for _i in range(200):
        service_name = random_str(10)
        service_names.append(service_name)

        Service.objects.create(
            name=service_name,
            cost=random.randint(10, 5000),
            labor_time=datetime.timedelta(minutes=random.randint(20, 120)),
            type=random.choice(ServiceType.choices)
        )

    number_words = ["Zero", "One", "Two", "Three",
                    "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
    packages = []

    for i in range(1, 11):
        packages.append(ServicePackage.objects.create(
            name='{}-year package'.format(number_words[i]),
            car_age=i,
            service_names=random.choices(service_names, k=(i + 2))
        ))

    customers = Customer.objects.all()
    vehicles = list(Vehicle.objects.all())
    indices = set(range(0, len(vehicles)))

    for customer in customers:
        vehicle: Vehicle = vehicles[indices.pop()]
        PurchaseBill.objects.create(
            date=datetime.date(year=random.randint(2020, 2021), month=random.randint(1, 12), day=random.randint(1, 30)),
            price=vehicle.cost * (1 + random.random() * 0.3),
            vin=vehicle,
            customer=customer
        )

    bills = list(PurchaseBill.objects.all())
    for bill in bills:
        if random.randint(0, 3) != 0:
            continue

        service_time = bill.date
        years = random.randint(1, 10)
        service_time += datetime.timedelta(days=365 * years)
        appt = ServiceAppointment.objects.create(
            scheduled_time=datetime.datetime(year=service_time.year, month=service_time.month, day=service_time.day),
            customer=bill.customer,
            service_package=packages[years - 1],
            vin=bill.vin
        )

        assigned_services = random.choices(service_names, k=random.randint(0, 5))
        for assigned_service in assigned_services:
            service = Service.objects.get(pk=assigned_service)
            print(service)
            ServicePerformed.objects.create(
                appt=appt,
                service=service
            )


seed_database()
