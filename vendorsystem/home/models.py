from django.db import models
from django.utils import timezone
import uuid

# ● name: CharField - Vendor's name.
# ● contact_details: TextField - Contact information of the vendor.
# ● address: TextField - Physical address of the vendor.
# ● vendor_code: CharField - A unique identifier for the vendor.
# ● on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
# ● quality_rating_avg: FloatField - Average rating of quality based on purchase
# orders.
# ● average_response_time: FloatField - Average time taken to acknowledge
# purchase orders.
# ● fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully.

class Vendor(models.Model):
    name=models.CharField(max_length=100)
    contact_details=models.TextField(max_length=1000)
    address=models.CharField(max_length=5000)
    vendor_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    on_time_delivery_rate=models.FloatField(default=0)
    quality_rating_avg=models.FloatField(default=0)
    average_response_time=models.FloatField(default=0)
    fulfillment_rate=models.FloatField(default=0)
    def __str__(self):
        return f"Vendor: {self.name}, Contact: {self.contact_details}, Address: {self.address}, ID: {self.vendor_id}, On-time Delivery Rate: {self.on_time_delivery_rate}, Quality Rating Avg: {self.quality_rating_avg}, Average Response Time: {self.average_response_time}, Fulfillment Rate: {self.fulfillment_rate}"


# ● vendor: ForeignKey - Link to the Vendor model.
# ● date: DateTimeField - Date of the performance record.
# ● on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
# ● quality_rating_avg: FloatField - Historical record of the quality rating average.
# ● average_response_time: FloatField - Historical record of the average response
# time.
# ● fulfillment_rate: FloatField - Historical record of the fulfilment rate.

# class VendorPerformance(models.Model):
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
#     date = models.DateTimeField()
#     on_time_delivery_rate = models.FloatField()
#     quality_rating_avg = models.FloatField()
#     average_response_time = models.FloatField()
#     fulfillment_rate = models.FloatField()


# ● po_number: CharField - Unique number identifying the PO.
# ● vendor: ForeignKey - Link to the Vendor model.
# ● order_date: DateTimeField - Date when the order was placed.
# ● delivery_date: DateTimeField - Expected or actual delivery date of the order.
# ● items: JSONField - Details of items ordered.
# ● quantity: IntegerField - Total quantity of items in the PO.
# ● status: CharField - Current status of the PO (e.g., pending, completed, canceled).
# ● quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
# ● issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
# ● acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor
# acknowledged the PO.

class PurchaseOrder(models.Model):
    def save(self, *args, **kwargs):
        if self.pk: 
            # If acknowledgment_date is provided and is not None, mark it as non-editable
            if self.acknowledgment_date is not None:
                self._meta.get_field('acknowledgment_date').editable = False
                self._meta.get_field('quality_rating').editable =True
        super().save(*args, **kwargs)

    PENDING="Pending"
    COMPLETED="Completed"
    CANCELED="Canceled"
    order_status = [(CANCELED,"Canceled"), (COMPLETED,"Completed"), (PENDING,"Pending")]
    po_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE) 
    order_date = models.DateTimeField(default=timezone.now, editable=False)
    issue_date = models.DateTimeField(default=timezone.now, editable=False)
    acknowledgment_date = models.DateTimeField(null=True)
    delivery_date = models.DateTimeField(null=True)
    items = models.JSONField()
    quantity = models.IntegerField()    
    status = models.CharField(max_length=9, choices=order_status, default=PENDING)
    quality_rating = models.FloatField(null=True, editable=False)
    def __str__(self):
        return f'PurchaseOrder {self.po_id} - Vendor: {self.vendor}, Items:{self.items} Quantity: {self.quantity}, Order_date:{self.order_date}, Acknowledgement Date:{self.acknowledgment_date},  Delivery Date:{self.delivery_date} '
    













    