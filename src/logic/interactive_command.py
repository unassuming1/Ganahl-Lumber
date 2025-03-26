```python
import json
import datetime
from datetime import timedelta
import re

# Load inventory data
with open('/home/ubuntu/ganahl-ai-project/inventory_data.json', 'r') as file:
    data = json.load(file)

# Current date for the simulation
current_date = datetime.datetime.now()

class CommandProcessor:
    def __init__(self, inventory_data):
        self.data = inventory_data
        self.current_date = datetime.datetime.now()
    
    def process_command(self, command_text):
        """Process natural language command and return structured response"""
        print(f"\n=== PROCESSING COMMAND: '{command_text}' ===\n")
        
        # Log the reasoning process
        reasoning = []
        reasoning.append(f"Received command: '{command_text}'")
        
        # Check for delivery scheduling command
        delivery_match = re.search(r'plan\s+a\s+delivery\s+(?:schedule\s+)?for\s+(\d+)\s+(?:board\s+feet|bf)\s+of\s+(\w+)(?:\s+next\s+week)?', command_text.lower())
        
        if delivery_match:
            quantity = int(delivery_match.group(1))
            material = delivery_match.group(2)
            
            reasoning.append(f"Identified delivery scheduling request for {quantity} board feet of {material}")
            
            # Find the material in inventory
            material_id = None
            current_stock = 0
            
            for category in self.data['inventory']:
                for item in self.data['inventory'][category]:
                    if material.lower() in item['name'].lower():
                        material_id = item['id']
                        material_name = item['name']
                        current_stock = item['current_stock']
                        reasoning.append(f"Found matching inventory item: {item['name']} (ID: {item['id']}) with current stock of {current_stock} units")
                        break
                if material_id:
                    break
            
            if not material_id:
                reasoning.append(f"Could not find {material} in inventory")
                return {
                    "success": False,
                    "message": f"Could not find {material} in inventory",
                    "reasoning": reasoning
                }
            
            # Check if we have enough stock
            if current_stock < quantity:
                reasoning.append(f"Insufficient stock: requested {quantity} units but only have {current_stock} units available")
                return {
                    "success": False,
                    "message": f"Insufficient stock of {material_name}. Requested: {quantity} units, Available: {current_stock} units",
                    "reasoning": reasoning
                }
            
            # Calculate delivery timeline
            # Assume 1 truck can carry 500 board feet and takes 2 hours per trip
            trucks_needed = (quantity + 499) // 500  # Ceiling division
            total_hours = trucks_needed * 2
            
            reasoning.append(f"Calculated logistics: {trucks_needed} truck(s) needed, {total_hours} hours total delivery time")
            
            # Determine delivery date (next Monday by default, or sooner if possible)
            today = self.current_date
            days_to_monday = (7 - today.weekday()) % 7
            if days_to_monday == 0:
                days_to_monday = 7  # If today is Monday, go to next Monday
            
            delivery_date = today + timedelta(days=days_to_monday)
            
            # If we can deliver sooner (within 2 business days), do so
            if total_hours <= 8:  # Can deliver in one business day
                business_days = 1
            else:
                business_days = 2
            
            # Skip weekends for business days calculation
            quick_delivery_date = today
            while business_days > 0:
                quick_delivery_date += timedelta(days=1)
                if quick_delivery_date.weekday() < 5:  # Monday to Friday
                    business_days -= 1
            
            # Use the earlier date if it's before next Monday
            if quick_delivery_date < delivery_date:
                delivery_date = quick_delivery_date
                reasoning.append(f"Can deliver quickly within {(quick_delivery_date - today).days} days (by {quick_delivery_date.strftime('%A, %B %d')})")
            else:
                reasoning.append(f"Scheduled for next week on {delivery_date.strftime('%A, %B %d')}")
            
            # Create delivery schedule
            delivery_schedule = {
                "material": material_name,
                "quantity": quantity,
                "units": "board feet",
                "trucks_required": trucks_needed,
                "estimated_hours": total_hours,
                "delivery_date": delivery_date.strftime("%Y-%m-%d"),
                "delivery_day": delivery_date.strftime("%A"),
                "status": "Scheduled"
            }
            
            # Format response message
            response_message = (
                f"Delivery of {quantity} board feet of {material_name} scheduled for "
                f"{delivery_date.strftime('%A, %B %d')}.\n"
                f"Logistics: {trucks_needed} truck(s), {total_hours} hour(s) total delivery time.\n"
                f"Stock check: {current_stock} units available, {current_stock - quantity} units will remain after delivery."
            )
            
            return {
                "success": True,
                "message": response_message,
                "delivery_schedule": delivery_schedule,
                "reasoning": reasoning
            }
        
        # If no recognized command pattern was matched
        reasoning.append("Command not recognized as a delivery scheduling request")
        return {
            "success": False,
            "message": "I couldn't understand that command. Try asking me to plan a delivery schedule for a specific quantity of material.",
            "reasoning": reasoning
        }

# Create command processor instance
processor = CommandProcessor(data)

# Test with the example command
test_command = "Plan a delivery schedule for 500 board feet of cedar next week."
result = processor.process_command(test_command)

# Print the reasoning process
print("=== AI REASONING PROCESS ===")
for step in result["reasoning"]:
    print(f"- {step}")

# Print the result
print("\n=== COMMAND RESPONSE ===")
print(result["message"])

if "delivery_schedule" in result:
    print("\n=== DELIVERY SCHEDULE DETAILS ===")
    for key, value in result["delivery_schedule"].items():
        print(f"{key}: {value}")

# Save the result to a file
with open('/home/ubuntu/ganahl-ai-project/command_processing_result.json', 'w') as file:
    json.dump(result, file, indent=2)

print("\nCommand processing result has been saved to file.")
```
