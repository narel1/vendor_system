
# Vendor Purchase System

The Vendor Purchase System is a Django-based application that manages vendors and purchase orders. It provides CRUD (Create, Read, Update, Delete) operations for vendors and purchase orders, along with additional functionalities such as acknowledging orders, providing feedback, and tracking vendor performance metrics.

## Features

- **Vendor Management**: Allows users to create, retrieve, update, and delete vendor information.
- **Purchase Order Management**: Enables users to create, retrieve, update, and delete purchase orders.
- **Acknowledgment**: Provides an API endpoint to acknowledge purchase orders, updating their status accordingly.
- **Feedback**: Allows users to provide feedback on purchase orders, updating their status to "Completed" upon submission.
- **Performance Metrics**: Automatically calculates and updates vendor performance metrics, including average response time, fulfillment rate, quality rating average, and on-time delivery rate.

## API Endpoints

- `/api/vendors/`: CRUD operations for managing vendors.
- `/api/purchase_orders/`: CRUD operations for managing purchase orders.
- `/api/purchase_orders/<po_id>/acknowledge/`: API endpoint to acknowledge a purchase order.
- `/api/purchase_orders/<po_id>/feedback/`: API endpoint to provide feedback on a purchase order.
- `/api/vendors/<vendor_id>/performance/`: Retrieves performance metrics for a specific vendor.

## Installation

1. Clone the repository to your local machine:
2. Navigate to the project directory:
3. Install the required dependencies:


4. Run the Django development server:


5. Access the API endpoints using the provided URLs.

## Usage

1. Use the CRUD APIs to manage vendor information as needed.
2. Utilize the purchase order APIs for specific operations with appropriate serializers.
3. Ensure purchase orders are approved by vendors before further processing.
4. Note that delivery dates are automatically set one day ahead upon approval.
5. Handle status changes carefully, especially after feedback submission, to update metrics and finalize order status.

## Explanation

Custom functions are implemented within serializers to handle specific requirements during data processing:

- **Average Response Time**: Calculates and updates average response time based on acknowledgment dates.
- **On-Time Delivery Rate**: Calculates and updates the on-time delivery rate based on delivery dates.
- **Quality Rating Average**: Calculates and updates the quality rating average based on user feedback.
- **Fulfillment Rate**: Calculates and updates the fulfillment rate based on order completion status.

## Custom Functions

- **MetricsUpdate**: Calculates and updates vendor performance metrics based on purchase order data.
- **convert_to_int**: Utility function to convert a string to an integer if possible.

## Serializer Classes

- **VendorSerializerForGet**: Serializes vendor data for GET requests.
- **VendorSerializerForPost**: Serializes vendor data for POST requests.
- **VendorSerializerForPut**: Serializes vendor data for PUT requests.
- **PurchaseOrderSerializerForGet**: Serializes purchase order data for GET requests.
- **PurchaseOrderSerializerForPost**: Serializes purchase order data for POST requests.
- **PurchaseOrderSerializerForPut**: Serializes purchase order data for PUT requests.
- **AcknowledgeOrderSerializer**: Serializes data for acknowledging purchase orders.
- **FeedBackOrderSerializer**: Serializes data for providing feedback on purchase orders.

## Contributing

Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests to help improve the application.

## License

This project is licensed under the [MIT License](LICENSE).




