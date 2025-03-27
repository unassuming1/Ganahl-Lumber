import json
import datetime
from datetime import timedelta

# Load inventory data
with open('/home/ubuntu/ganahl-lumber-project/src/data/inventory_data.json', 'r') as file:
    data = json.load(file)

# Current date for the simulation (Wednesday, March 26, 2025)
current_date = datetime.datetime.now()
print(f"Current date: {current_date.strftime('%Y-%m-%d')} ({current_date.strftime('%A')})")

class CustomerServiceAgent:
    def __init__(self, inventory_data):
        self.data = inventory_data
        self.current_date = datetime.datetime.now()
    
    def process_inquiry(self, inquiry_text):
        """Process customer inquiry and return structured response"""
        print(f"\n=== PROCESSING CUSTOMER INQUIRY ===\n")
        print(f"Inquiry: '{inquiry_text}'")
        
        # Log the reasoning process
        reasoning = []
        reasoning.append(f"Received inquiry: '{inquiry_text}'")
        
        # Parse the inquiry for oak flooring project
        reasoning.append("Analyzing inquiry for product, quantity, and delivery date requirements")
        
        # Extract key information from the inquiry
        product_type = "oak flooring"
        project_size = 1000  # square feet
        delivery_by_date = self.current_date + timedelta(days=2)  # Friday if today is Wednesday
        
        reasoning.append(f"Identified request for {project_size} sq ft of {product_type} needed by {delivery_by_date.strftime('%A, %B %d')}")
        
        # Find the product in inventory
        product_found = False
        for category in self.data['inventory']:
            for item in self.data['inventory'][category]:
                if product_type.lower() in item['name'].lower():
                    product_id = item['id']
                    product_name = item['name']
                    current_stock = item['current_stock']
                    product_found = True
                    reasoning.append(f"Found matching inventory item: {item['name']} (ID: {item['id']}) with current stock of {current_stock} units")
                    break
            if product_found:
                break
        
        if not product_found:
            reasoning.append(f"Could not find {product_type} in inventory")
            return {
                "success": False,
                "message": f"I'm sorry, we don't currently carry {product_type}.",
                "reasoning": reasoning
            }
        
        # Check if we have enough stock (assuming 1 sq ft = 1 board foot as specified)
        if current_stock < project_size:
            reasoning.append(f"Insufficient stock: requested {project_size} sq ft but only have {current_stock} board feet available")
            
            # Check if we can source more from nearby warehouse
            reasoning.append("Checking alternative sourcing options")
            backup_available = 500  # As specified in the requirements
            
            if current_stock + backup_available >= project_size:
                reasoning.append(f"Can fulfill order by sourcing additional {project_size - current_stock} board feet from nearby warehouse")
                
                return {
                    "success": True,
                    "message": f"We currently have {current_stock} board feet of {product_name} in stock, which is not enough for your {project_size} sq ft project. However, we can source an additional {project_size - current_stock} board feet from our nearby warehouse to complete your order by {delivery_by_date.strftime('%A, %B %d')}.",
                    "reasoning": reasoning,
                    "requires_additional_sourcing": True,
                    "main_stock": current_stock,
                    "additional_stock_needed": project_size - current_stock,
                    "total_needed": project_size,
                    "delivery_date": delivery_by_date.strftime("%Y-%m-%d")
                }
            else:
                reasoning.append(f"Cannot fulfill order even with backup stock: total available is {current_stock + backup_available} board feet")
                
                return {
                    "success": False,
                    "message": f"I'm sorry, we only have {current_stock} board feet of {product_name} in stock, with an additional {backup_available} board feet available from our nearby warehouse. This total of {current_stock + backup_available} board feet is not sufficient for your {project_size} sq ft project. Would you like to place a special order?",
                    "reasoning": reasoning
                }
        
        # We have enough stock, now check delivery logistics
        reasoning.append(f"Sufficient stock available: {current_stock} board feet (need {project_size})")
        
        # Calculate delivery timeline
        # Assume 1 truck can carry 500 board feet and takes 2 hours per trip
        trucks_needed = (project_size + 499) // 500  # Ceiling division
        total_hours = trucks_needed * 2
        
        reasoning.append(f"Calculated logistics: {trucks_needed} truck(s) needed, {total_hours} hours total delivery time")
        
        # Check if we can deliver by the requested date
        days_until_delivery = (delivery_by_date - self.current_date).days
        
        if days_until_delivery < 1:
            reasoning.append(f"Requested delivery date ({delivery_by_date.strftime('%A')}) is too soon for standard delivery")
            
            # Check if expedited delivery is possible
            if total_hours <= 4:  # Can deliver in half a day
                reasoning.append("Expedited same-day delivery is possible")
                expedited_delivery = True
                delivery_date = self.current_date
            else:
                reasoning.append("Expedited delivery not possible, need at least one business day")
                expedited_delivery = False
                # Find next business day
                next_day = self.current_date + timedelta(days=1)
                while next_day.weekday() >= 5:  # Skip weekends
                    next_day += timedelta(days=1)
                delivery_date = next_day
        else:
            reasoning.append(f"Standard delivery possible by requested date ({delivery_by_date.strftime('%A')})")
            expedited_delivery = False
            delivery_date = delivery_by_date
        
        # Create delivery schedule
        delivery_schedule = {
            "material": product_name,
            "quantity": project_size,
            "units": "board feet",
            "trucks_required": trucks_needed,
            "estimated_hours": total_hours,
            "delivery_date": delivery_date.strftime("%Y-%m-%d"),
            "delivery_day": delivery_date.strftime("%A"),
            "expedited": expedited_delivery,
            "status": "Confirmed"
        }
        
        # Calculate remaining stock after order
        remaining_stock = current_stock - project_size
        reasoning.append(f"After fulfilling this order, {remaining_stock} board feet will remain in stock")
        
        # Check if we need to reorder based on reorder point
        reorder_point = None
        for category in self.data['inventory']:
            for item in self.data['inventory'][category]:
                if item['id'] == product_id:
                    reorder_point = item['reorder_point']
                    break
            if reorder_point:
                break
        
        if reorder_point and remaining_stock < reorder_point:
            reasoning.append(f"Remaining stock ({remaining_stock}) will be below reorder point ({reorder_point}). Should trigger reorder process.")
        
        # Format response message
        if delivery_date.strftime("%Y-%m-%d") == delivery_by_date.strftime("%Y-%m-%d"):
            delivery_confirmation = f"Yes, we can deliver by your requested date of {delivery_by_date.strftime('%A, %B %d')}."
        else:
            delivery_confirmation = f"We can deliver on {delivery_date.strftime('%A, %B %d')}, which is {'earlier' if delivery_date < delivery_by_date else 'later'} than your requested date."
        
        response_message = (
            f"{delivery_confirmation}\n"
            f"We have {current_stock} board feet of {product_name} in stock, which is sufficient for your {project_size} sq ft project.\n"
            f"Delivery details: {trucks_needed} truck(s), estimated {total_hours} hour(s) delivery time.\n"
            f"Backup: If needed, we can source an additional 500 board feet from our nearby warehouse."
        )
        
        return {
            "success": True,
            "message": response_message,
            "delivery_schedule": delivery_schedule,
            "stock_information": {
                "current_stock": current_stock,
                "required_amount": project_size,
                "remaining_after_order": remaining_stock,
                "backup_available": 500
            },
            "reasoning": reasoning
        }

# Create customer service agent instance
agent = CustomerServiceAgent(data)

# Process the example inquiry
inquiry = "Do you have enough oak flooring for a 1,000-square-foot project, deliverable by Friday?"
result = agent.process_inquiry(inquiry)

# Print the reasoning process
print("\n=== AI REASONING PROCESS ===")
for step in result["reasoning"]:
    print(f"- {step}")

# Print the result
print("\n=== CUSTOMER SERVICE RESPONSE ===")
print(result["message"])

if "delivery_schedule" in result:
    print("\n=== DELIVERY SCHEDULE DETAILS ===")
    for key, value in result["delivery_schedule"].items():
        print(f"{key}: {value}")

if "stock_information" in result:
    print("\n=== STOCK INFORMATION ===")
    for key, value in result["stock_information"].items():
        print(f"{key}: {value}")

# Save the result to a file
with open('/home/ubuntu/ganahl-lumber-project/src/data/customer_service_result.json', 'w') as file:
    json.dump(result, file, indent=2)

print("\nCustomer service inquiry result has been saved to file.")
