from home.views import vendor, purchase_orders, acknowledgeorder, feedbackorder
from django.urls import path


urlpatterns = [
    path('vendors/', vendor),
    path('purchase_orders/', purchase_orders),
    path('purchase_orders/<uuid:po_id>/acknowledge/', acknowledgeorder, name='acknowledge_purchase_order'),
    path('purchase_orders/<uuid:po_id>/feedback/', feedbackorder, name='feedback_purchase_order')
]