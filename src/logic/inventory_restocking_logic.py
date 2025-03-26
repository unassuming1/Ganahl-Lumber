```python
import json
import datetime
from datetime import timedelta

# Load inventory data
with open('/home/ubuntu/ganahl-ai-project/inventory_data.json', 'r') as file:
    data = json.load(file)

# Current date for the simulation
current_date = datetime.datetime.now()
print(f"Current date: {current_date.strftime('%Y-%m-%d')}")

# Function to analyze inventory and generate purchase orders
def analyze_inventory_and_generate_po():
    print("\n=== INVENTORY ANALYSIS AND PURCHASE ORDER GENERATION ===\n")
    
    # Initialize purchase orders
    purchase_orders = {}
    
    # Track decision log
    decision_log = []
    
    # Analyze each product category
    for category in data['inventory']:
        for item in data['inventory'][category]:
            item_id = item['id']
            item_name = item['name']
            current_stock = item['current_stock']
            weekly_sales = data['sales_trends']['weekly'].get(item_id, 0)
            reorder_point = item['reorder_point']
            optimal_stock = item['optimal_stock']
            supplier_id = None
            
            # Check upcoming orders for this product
            upcoming_demand = 0
            earliest_required_date = None
            
            for order in data['upcoming_orders']:
                for order_item in order['items']:
                    if order_item['product_id'] == item_id:
                        upcoming_demand += order_item['quantity']
                        order_required_date = datetime.datetime.strptime(order['required_date'], '%Y-%m-%d')
                        if earliest_required_date is None or order_required_date < earliest_required_date:
                            earliest_required_date = order_required_date
            
            # Calculate days until stock falls below reorder point
            daily_usage = weekly_sales / 7
            if daily_usage > 0:
                days_until_reorder = (current_stock - reorder_point) / daily_usage
            else:
                days_until_reorder = float('inf')
            
            # Calculate projected stock after upcoming orders
            projected_stock = current_stock - upcoming_demand
            
            # Find supplier for this product
            for supplier in data['suppliers']:
                if item_id in supplier['products']:
                    supplier_id = supplier['id']
                    supplier_name = supplier['name']
                    lead_time = supplier['lead_time_days']
                    break
            
            # Decision making logic
            if projected_stock <= reorder_point:
                # Critical situation - stock will be below reorder point after fulfilling orders
                order_quantity = optimal_stock - projected_stock
                priority = "HIGH"
                reason = f"Projected stock ({projected_stock}) will be below reorder point ({reorder_point}) after fulfilling upcoming orders"
                decision_log.append(f"CRITICAL: {item_name} needs immediate reordering. {reason}")
            elif days_until_reorder <= 7:  # Will hit reorder point within a week
                order_quantity = optimal_stock - current_stock
                priority = "MEDIUM"
                reason = f"Stock will reach reorder point in {days_until_reorder:.1f} days"
                decision_log.append(f"WARNING: {item_name} will reach reorder point in {days_until_reorder:.1f} days")
            else:
                # No need to reorder yet
                order_quantity = 0
                priority = "LOW"
                reason = f"Sufficient stock available ({current_stock} units, reorder at {reorder_point})"
                decision_log.append(f"INFO: {item_name} has sufficient stock ({current_stock} units)")
            
            # If we need to order, add to purchase orders
            if order_quantity > 0:
                if supplier_id not in purchase_orders:
                    purchase_orders[supplier_id] = {
                        "supplier_name": supplier_name,
                        "order_date": current_date.strftime('%Y-%m-%d'),
                        "expected_delivery": (current_date + timedelta(days=lead_time)).strftime('%Y-%m-%d'),
                        "items": [],
                        "total_value": 0
                    }
                
                item_cost = item['cost_per_unit']
                total_item_cost = item_cost * order_quantity
                
                purchase_orders[supplier_id]["items"].append({
                    "product_id": item_id,
                    "product_name": item_name,
                    "quantity": order_quantity,
                    "unit_cost": item_cost,
                    "total_cost": total_item_cost,
                    "priority": priority,
                    "reason": reason
                })
                
                purchase_orders[supplier_id]["total_value"] += total_item_cost
    
    return purchase_orders, decision_log

# Generate purchase orders
purchase_orders, decision_log = analyze_inventory_and_generate_po()

# Print decision log
print("\n=== DECISION LOG ===\n")
for decision in decision_log:
    print(decision)

# Print purchase orders
print("\n=== PURCHASE ORDERS ===\n")
for supplier_id, po in purchase_orders.items():
    print(f"Purchase Order for {po['supplier_name']} (ID: {supplier_id})")
    print(f"Order Date: {po['order_date']}")
    print(f"Expected Delivery: {po['expected_delivery']}")
    print("\nItems:")
    for item in po['items']:
        print(f"  - {item['product_name']}: {item['quantity']} units at ${item['unit_cost']:.2f} each = ${item['total_cost']:.2f} ({item['priority']} priority)")
        print(f"    Reason: {item['reason']}")
    print(f"\nTotal Order Value: ${po['total_value']:.2f}")
    print("\n" + "-"*50 + "\n")

# Save purchase orders to file
with open('/home/ubuntu/ganahl-ai-project/purchase_orders.json', 'w') as file:
    json.dump(purchase_orders, file, indent=2)

# Save decision log to file
with open('/home/ubuntu/ganahl-ai-project/inventory_decision_log.txt', 'w') as file:
    file.write("\n".join(decision_log))

print("Purchase orders and decision log have been saved to files.")
```
