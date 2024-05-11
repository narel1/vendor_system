from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Vendor, PurchaseOrder
from home.serializers import VendorSerializerForGet, VendorSerializerForPost, VendorSerializerForPut
from home.serializers import PurchaseOrderSerializerForGet, PurchaseOrderSerializerForPost, PurchaseOrderSerializerForPut
from home.serializers import AcknowledgeOrderSerializer, FeedBackOrderSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .custom_function import MetricsUpdate
import uuid

# /api/vendors
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def vendor(request):
    vendor_id = request.GET.get('vendor_id')
    if request.method=='GET':
        try:
            if vendor_id == None:
                vendors=Vendor.objects.all()
                serializers=VendorSerializerForGet(vendors,many=True)
                return Response(serializers.data , status=status.HTTP_200_OK)
            vendor=Vendor.objects.get(pk=vendor_id)
            serializer = VendorSerializerForGet(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method=='POST':
        data=request.data
        try:
            serializer=VendorSerializerForPost(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='PUT':
        data=request.data
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = VendorSerializerForPut(instance=vendor, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response({"message": "Successfully Deleted"}, status=status.HTTP_200_OK)
    


# /api/purchase_orders
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def purchase_orders(request):
    po_id = request.GET.get('po_id')
    if request.method == 'GET':
        if po_id == None:
            purchase_orders=PurchaseOrder.objects.all()
            serializers=PurchaseOrderSerializerForGet(purchase_orders, many=True)
            return Response(serializers.data , status=status.HTTP_404_NOT_FOUND)
        try:
            purchase_order=PurchaseOrder.objects.get(pk=po_id)
            serializer=PurchaseOrderSerializerForGet(purchase_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase Order with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        data = request.data 
        try:
            serializer = PurchaseOrderSerializerForPost(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PUT':
        data = request.data
        if po_id is not None:
            try:
                purchase_order = PurchaseOrder.objects.get(pk=po_id)
            except PurchaseOrder.DoesNotExist:
                return Response({"error": "Purchase Order with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)           
            serializer = PurchaseOrderSerializerForPut(instance=purchase_order, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"errors":"Purchase Order ID not given"}, status=status.HTTP_404_NOT_FOUND)
    else:
        if po_id is not None:
            try:
                vendor = Vendor.objects.get(pk=vendor_id)
            except Vendor.DoesNotExist:
                return Response({"error": "Vendor with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
            vendor.delete()
            return Response({"message": "Successfully Deleted"}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def acknowledgeorder(request,po_id):
    data=request.data
    if request.method=='POST' and po_id:
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purcahse Order with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AcknowledgeOrderSerializer(instance=purchase_order, data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                metrics=MetricsUpdate(po_id)
                metrics.AverageResponseTime()
                metrics.SAVE_METRICS()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def feedbackorder(request, po_id,):
    data=request.data
    if po_id:
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purcahse Order with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FeedBackOrderSerializer(instance=purchase_order, data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                metrics=MetricsUpdate(po_id, serializer.data.quality_rating)
                metrics.FulfillmentRate()
                metrics.OnTimeDeliveryRate()
                metrics.QualityRatingAverage()
                metrics.SAVE_METRICS()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def vendorperformance(request, vendor_id):
    if request.method =='GET' and vendor_id:
        try:
            vendor=Vendor.objects.get(pk=vendor_id)
            serializer = VendorSerializerForGet(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor with the specified ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
