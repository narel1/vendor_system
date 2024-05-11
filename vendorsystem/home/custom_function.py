from .models import PurchaseOrder, Vendor
from django.utils import timezone

class MetricsUpdate:
    def __init__(self, purchase_order_id, quality_rating=None):
        self.purchase_order_id = purchase_order_id
        self.quality_rating = quality_rating
        self.purchase_order=PurchaseOrder.objects.get(pk=purchase_order_id)
        self.vendor=Vendor.objects.get(pk=purchase_order.vendor)
        self.nummberoforders = PurchaseOrder.objects.filter(vendor=purchase_order.vendor).count()
        self.nummberoforderscompleted = PurchaseOrder.objects.filter(vendor=purchase_order.vendor, status="Completed").count()
        self.nummberoforderswithqualityrating=PurchaseOrder.objects.filter(vendor=vendor_id).exclude(quality_rating=None).count()
    
    
    #AverageResponseTime
    def AverageResponseTime(self):
        average_response = (self.purchase_order.acknowledgment_date - self.purchase_order.issue_date).total_seconds/60
        total_response_time = self.vendor.average_response_time * self.nummberoforders
        total_response_time += average_response
        nummberoforders = self.nummberoforders
        average_response_time = total_response_time / nummberoforders
        self.vendor.average_response_time=average_response_time
    
    #Fulfilment Rate
    def FulfillmentRate():
        nummberoforderscompleted=self.nummberoforderscompleted+1
        fulfillment_rate = nummberoforderscompleted/self.nummberoforders
        self.vendor.fulfillment_rate=fulfillment_rate
        
    
    #QualityRatingAverage:
    def QualityRatingAverage():
        quality_rating_total=self.vendor.quality_rating_avg*self.nummberoforderswithqualityrating
        quality_rating_total+=self.quality_rating
        nummberoforderswithqualityrating = self.nummberoforderswithqualityrating + 1
        quality_rating_avg=quality_rating_total /nummberoforderswithqualityrating
        self.vendor.quality_rating_avg=quality_rating_avg
    
    #On-Time Delivery Rate:
    def OnTimeDeliveryRate():
        on_time_delivery_rate_total=self.vendor.on_time_delivery_rate*self.nummberoforderscompleted
        nummberoforderscompleted= self.nummberoforderscompleted + 1
        if purchase_order.delivery_date <= timezone.now():
            on_time_delivery_rate_total+=1
        on_time_delivery_rate=on_time_delivery_rate_total/nummberoforderscompleted
        self.vendor.on_time_delivery_rate=on_time_delivery_rate
   
    def SAVE_METRICS():
        self.vendor.save()
