# Generated by Django 5.0.4 on 2024-05-08 12:30

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_vendor_id_alter_vendor_vendor_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('po_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('issue_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('acknowledgment_date', models.DateTimeField(null=True)),
                ('delivery_date', models.DateTimeField(null=True)),
                ('items', models.JSONField()),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('Canceled', 'Canceled'), ('Completed', 'Completed'), ('Pending', 'Pending')], default='Pending', max_length=9)),
                ('quality_rating', models.FloatField(null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.vendor')),
            ],
        ),
    ]
