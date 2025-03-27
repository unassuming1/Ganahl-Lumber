```python
import json
import datetime
from datetime import timedelta

# Load inventory data
with open('/home/ubuntu/ganahl-lumber-project/src/data/inventory_data.json', 'r') as file:
    data = json.load(file)

# Current date for the simulation
current_date = datetime.datetime.now()
print(f"Current date: {current_date.strftime('%Y-%m-%d')}")

# Function to analyze inventory and generate purchase orders
def analyze_inventory_and_generate_po(demand_spike=None):
    print("\n=== INVENTORY ANALYSIS AND PURCHASE ORDER GENERATION ===\n")
    
    # Initialize purchase orders
    purchase_orders = {}
    
    # Track decision log
    decision_log = []
    
    # Add demand spike if provided
    if demand_spike:
        decision_log.append(f"ALERT: Detected sudden demand spike for {demand_spike['product_name']} - {demand_spike['quantity']} units needed by {demand_spike['required_date']}")
        
        # Find the product in our inventory
        product_found = False
        for category in data['inventory']:
            for item in data['inventory'][category]:
                if item['id'] == demand_spike['product_id']:
                    product_found = True
                    break
            if product_found:
                break
        
        if not product_found:
            decision_log.append(f"ERROR: Product {demand_spike['product_id']} not found in inventory")
            return purchase_orders, decision_log
    
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
            
            # Add demand spike if it matches this product
            if demand_spike and demand_spike['product_id'] == item_id:
                upcoming_demand += demand_spike['quantity']
                spike_required_date = datetime.datetime.strptime(demand_spike['required_date'], '%Y-%m-%d')
                if earliest_required_date is None or spike_required_date < earliest_required_date:
                    earliest_required_date = spike_required_date
                
                decision_log.append(f"ADJUSTMENT: Added demand spike of {demand_spike['quantity']} units to {item_name} upcoming demand")
            
            # Calculate days until stock falls below reorder point
            daily_usage = weekly_sales / 7
            if daily_usage > 0:
                days_until_reorder = (current_stock - reorder_point) / daily_usage
            else:
                days_until_reorder = float('inf')
            
            # Calculate projected stock after upcoming orders
            projected_stock = current_stock - upcoming_demand
            
            # Find primary supplier for this product
            primary_supplier_id = None
            primary_supplier_name = None
            primary_lead_time = None
            
            # Find alternative supplier with shortest lead time
            alt_supplier_id = None
            alt_supplier_name = None
            alt_lead_time = float('inf')
            
            for supplier in data['suppliers']:
                if item_id in supplier['products']:
                    if primary_supplier_id is None:
                        primary_supplier_id = supplier['id']
                        primary_supplier_name = supplier['name']
                        primary_lead_time = supplier['lead_time_days']
                    
                    # Check if this is a faster alternative
                    if supplier['lead_time_days'] < alt_lead_time:
                        alt_supplier_id = supplier['id']
                        alt_supplier_name = supplier['name']
                        alt_lead_time = supplier['lead_time_days']
            
            # Default to primary supplier
            supplier_id = primary_supplier_id
            supplier_name = primary_supplier_name
            lead_time = primary_lead_time
            
            # Decision making logic
            if projected_stock <= 0:
                # Critical situation - not enough stock to fulfill orders
                order_quantity = optimal_stock
                priority = "CRITICAL"
                reason = f"Projected stock ({projected_stock}) is negative - cannot fulfill all orders"
                decision_log.append(f"CRITICAL: {item_name} has insufficient stock to meet demand. {reason}")
                
                # Use alternative supplier if available and faster
                if demand_spike and demand_spike['product_id'] == item_id and alt_supplier_id != primary_supplier_id and alt_lead_time < primary_lead_time:
                    supplier_id = alt_supplier_id
                    supplier_name = alt_supplier_name
                    lead_time = alt_lead_time
                    decision_log.append(f"STRATEGY: Switched from {primary_supplier_name} (lead time: {primary_lead_time} days) to {alt_supplier_name} (lead time: {alt_lead_time} days) for faster delivery of {item_name}")
                
            elif projected_stock <= reorder_point:
                # High priority - stock will be below reorder point after fulfilling orders
                order_quantity = optimal_stock - projected_stock
                priority = "HIGH"
                reason = f"Projected stock ({projected_stock}) will be below reorder point ({reorder_point}) after fulfilling upcoming orders"
                decision_log.append(f"HIGH PRIORITY: {item_name} needs immediate reordering. {reason}")
                
                # Use alternative supplier if there's a demand spike for this product
                if demand_spike and demand_spike['product_id'] == item_id and alt_supplier_id != primary_supplier_id and alt_lead_time < primary_lead_time:
                    supplier_id = alt_supplier_id
                    supplier_name = alt_supplier_name
                    lead_time = alt_lead_time
                    decision_log.append(f"STRATEGY: Switched from {primary_supplier_name} (lead time: {primary_lead_time} days) to {alt_supplier_name} (lead time: {alt_lead_time} days) for faster delivery of {item_name}")
                
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

# Generate initial purchase orders
print("=== INITIAL INVENTORY ANALYSIS ===")
initial_purchase_orders, initial_decision_log = analyze_inventory_and_generate_po()

# Print initial decision log
print("\n=== INITIAL DECISION LOG ===\n")
for decision in initial_decision_log:
    print(decision)

# Print initial purchase orders
print("\n=== INITIAL PURCHASE ORDERS ===\n")
for supplier_id, po in initial_purchase_orders.items():
    print(f"Purchase Order for {po['supplier_name']} (ID: {supplier_id})")
    print(f"Order Date: {po['order_date']}")
    print(f"Expected Delivery: {po['expected_delivery']}")
    print("\nItems:")
    for item in po['items']:
        print(f"  - {item['product_name']}: {item['quantity']} units at ${item['unit_cost']:.2f} each = ${item['total_cost']:.2f} ({item['priority']} priority)")
        print(f"    Reason: {item['reason']}")
    print(f"\nTotal Order Value: ${po['total_value']:.2f}")
    print("\n" + "-"*50 + "\n")

# Save initial purchase orders to file
with open('/home/ubuntu/ganahl-lumber-project/src/data/initial_purchase_orders.json', 'w') as file:
    json.dump(initial_purchase_orders, file, indent=2)

# Save initial decision log to file
with open('/home/ubuntu/ganahl-lumber-project/src/data/initial_inventory_decision_log.txt', 'w') as file:
    file.write("\n".join(initial_decision_log))

# Simulate a demand spike for decking materials
print("\n=== SIMULATING DEMAND SPIKE ===\n")
print("Sudden demand spike detected: 1,000 units of decking materials needed in 7 days")
print("Primary supplier lead time: 7 days")
print("Analyzing alternative suppliers and adjusting priorities...\n")

demand_spike = {
    "product_id": "cedar-decking",
    "product_name": "Cedar Decking",
    "quantity": 1000,
    "required_date": (current_date + timedelta(days=7)).strftime('%Y-%m-%d')
}

# Generate updated purchase orders with demand spike
updated_purchase_orders, updated_decision_log = analyze_inventory_and_generate_po(demand_spike)

# Print updated decision log
print("\n=== UPDATED DECISION LOG ===\n")
for decision in updated_decision_log:
    print(decision)

# Print updated purchase orders
print("\n=== UPDATED PURCHASE ORDERS ===\n")
for supplier_id, po in updated_purchase_orders.items():
    print(f"Purchase Order for {po['supplier_name']} (ID: {supplier_id})")
    print(f"Order Date: {po['order_date']}")
    print(f"Expected Delivery: {po['expected_delivery']}")
    print("\nItems:")
    for item in po['items']:
        print(f"  - {item['product_name']}: {item['quantity']} units at ${item['unit_cost']:.2f} each = ${item['total_cost']:.2f} ({item['priority']} priority)")
        print(f"    Reason: {item['reason']}")
    print(f"\nTotal Order Value: ${po['total_value']:.2f}")
    print("\n" + "-"*50 + "\n")

# Save updated purchase orders to file
with open('/home/ubuntu/ganahl-lumber-project/src/data/updated_purchase_orders.json', 'w') as file:
    json.dump(updated_purchase_orders, file, indent=2)

# Save updated decision log to file
with open('/home/ubuntu/ganahl-lumber-project/src/data/updated_inventory_decision_log.txt', 'w') as file:
    file.write("\n".join(updated_decision_log))

# Generate comparison summary
print("\n=== BEFORE AND AFTER COMPARISON ===\n")

# Find cedar decking in initial and updated purchase orders
initial_cedar_order = None
initial_supplier = None
for supplier_id, po in initial_purchase_orders.items():
    for item in po['items']:
        if item['product_id'] == 'cedar-decking':
            initial_cedar_order = item
            initial_supplier = po['supplier_name']
            break
    if initial_cedar_order:
        break

updated_cedar_order = None
updated_supplier = None
for supplier_id, po in updated_purchase_orders.items():
    for item in po['items']:
        if item['product_id'] == 'cedar-decking':
            updated_cedar_order = item
            updated_supplier = po['supplier_name']
            break
    if updated_cedar_order:
        break

print("Cedar Decking Order Comparison:")
if initial_cedar_order:
    print(f"BEFORE: Order {initial_cedar_order['quantity']} units from {initial_supplier} ({initial_cedar_order['priority']} priority)")
else:
    print("BEFORE: No order needed for Cedar Decking")

if updated_cedar_order:
    print(f"AFTER: Order {updated_cedar_order['quantity']} units from {updated_supplier} ({updated_cedar_order['priority']} priority)")
else:
    print("AFTER: No order needed for Cedar Decking despite demand spike (check inventory levels)")

# Save comparison to file
with open('/home/ubuntu/ganahl-lumber-project/src/data/order_comparison.txt', 'w') as file:
    file.write("Cedar Decking Order Comparison:\n")
    if initial_cedar_order:
        file.write(f"BEFORE: Order {initial_cedar_order['quantity']} units from {initial_supplier} ({initial_cedar_order['priority']} priority)\n")
    else:
        file.write("BEFORE: No order needed for Cedar Decking\n")
    
    if updated_cedar_order:
        file.write(f"AFTER: Order {updated_cedar_order['quantity']} units from {updated_supplier} ({updated_cedar_order['priority']} priority)\n")
    else:
        file.write("AFTER: No order needed for Cedar Decking despite demand spike (check inventory levels)\n")

print("\nAdaptability demonstration complete. All files have been saved.")
```
