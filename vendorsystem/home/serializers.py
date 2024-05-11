from rest_framework import serializers
from .models import Vendor, PurchaseOrder
from django.utils import timezone
import json


class VendorSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=['name','contact_details','address']
        # fields which we are serializing

class VendorSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields='__all__'
        # fields which we are serializing

class VendorSerializerForPut(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        exclude = ['vendor_id', 'on_time_delivery_rate', 'quality_rating_avg',
        'average_response_time', 'fulfillment_rate']  # Exclude the vendor_id field
        extra_kwargs = {
            'name': {'required': False},
            'contact_details': {'required': False},
            'address': {'required': False},
        }

class PurchaseOrderSerializerForGet(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields='__all__'

class PurchaseOrderSerializerForPost(serializers.ModelSerializer):
    
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())
    class Meta:
        model=PurchaseOrder
        fields=['vendor', 'items', 'quantity']

    def to_internal_value(self, data):
        try:
            uuid_str = data.get('vendor', None)
            if uuid_str:
                vendor = Vendor.objects.get(pk=uuid_str)
                data['quantity'] = len(data['items'].keys())
        except Vendor.DoesNotExist:
            raise serializers.ValidationError("Vendor does not exist")
        return super().to_internal_value(data)
   
class PurchaseOrderSerializerForPut(serializers.ModelSerializer):
    
    items = serializers.JSONField() 
    class Meta:
        model=PurchaseOrder
        fields=['vendor', 'items', 'quantity']
        
    def to_internal_value(self, data):
        try:
            uuid_str = data.get('vendor', None)
            if uuid_str:
                vendor = Vendor.objects.get(pk=uuid_str)
                data['quantity'] = len(data['items'].keys())
        except Vendor.DoesNotExist:
            raise serializers.ValidationError("Vendor does not exist")
        return super().to_internal_value(data)

    def validate_items(self, items):
        if not items:  # Check if items dictionary is empty
            raise serializers.ValidationError("Items must not be empty")
        return items

    


class AcknowledgeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['status', 'acknowledgment_date','delivery_date']
    def to_internal_value(self, data):   
        data['acknowledgment_date']=timezone.now()
        data['delivery_date']=timezone.now()
        one_day_delta = timedelta(days=1)
        data['delivery_date'] = current_datetime + one_day_delta
        return super().to_internal_value(data)

    def validate_status(self, data):
        if data is not  "Pending" or data is not "Canceled":
            serializers.ValidationError("Status should be string and it can be either Pending or Canceled ")



def convert_to_int(value):
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    elif isinstance(value, int):
        return value
    else:
        return None

class FeedBackOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['quality_rating', 'status']
    def to_internal_value(self, data):   
        data['status']="Completed"
        return super().to_internal_value(data)

    def validate_quality_rating(self,data):
        feedback=convert_to_int(data)
        if feedback is not None:
            if feedback < 0 or feedback > 5:
                return serializers.ValidationError("Enter quality rating between from 1 to 5")
        else:
            return serializers.ValidationError("Enter quality rating between from 1 to 5")





        
        


