from django.db import models

# Create your models here.


class ServiceType(models.TextChoices):
    PART = 'PART'
    TEST = 'TEST'


class Vehicle(models.Model):
    vin = models.CharField(max_length=60, null=False, primary_key=True)
    cost = models.IntegerField(null=False)
    model = models.CharField(max_length=60, null=False, db_index=True)
    make = models.CharField(max_length=60, null=False, db_index=True)
    msrp = models.IntegerField(null=False)
    year = models.IntegerField(null=False)

    def __str__(self) -> str:
        return '{} {}: {}'.format(self.make, self.model, self.vin)

    class Meta:
        db_table = "vehicle"


class Service(models.Model):
    labor_time = models.DurationField(null=False)
    cost = models.FloatField(null=False, default=0.0)
    name = models.CharField(max_length=60, null=False,
                            db_index=True, primary_key=True)
    type = models.CharField(
        max_length=20, choices=ServiceType.choices, db_index=True)

    class Meta:
        db_table = "service"


class ServicePackage(models.Model):
    name = models.CharField(null=False, max_length=30, primary_key=True)
    car_age = models.IntegerField(null=True)
    service_names = models.JSONField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "service_package"


class Customer(models.Model):
    customer_no = models.AutoField(primary_key=True)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=60, null=False, db_index=True)
    phone_number = models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "customer"


class PurchaseBill(models.Model):
    date = models.DateField(auto_now=True, db_index=True)
    price = models.IntegerField(null=False)
    bill_id = models.AutoField(primary_key=True)
    vin = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING,
                            null=False, related_name='purchased_vehicle', db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,
                                 null=False, related_name='purchase_customer', db_index=True)

    class Meta:
        db_table = "purchase_bill"


class ServiceAppointment(models.Model):
    appt_id = models.AutoField(primary_key=True)
    scheduled_time = models.TimeField(null=False, db_index=True)
    dropoff_time = models.TimeField(null=True)
    pickup_time = models.TimeField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,
                                 null=False, related_name='served_customer', db_index=True)
    vin = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING,
                            null=False, related_name='served_vehicle', db_index=True)
    service_package = models.ForeignKey(ServicePackage, on_delete=models.DO_NOTHING,
                                        null=True, related_name='service_package', default=None, db_index=True)

    class Meta:
        db_table = "service_appointment"


class ServicePerformed(models.Model):
    appt = models.ForeignKey(ServiceAppointment, on_delete=models.DO_NOTHING,
                             null=False, related_name='appt_for_service', db_index=True)
    service = models.ForeignKey(
        Service, on_delete=models.DO_NOTHING, null=False, related_name='service_for_appt', db_index=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "service_performed"
