# Generated by Django 3.1.2 on 2021-05-15 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_dealer', '0003_auto_20210515_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasebill',
            name='date',
            field=models.DateField(db_index=True),
        ),
    ]
