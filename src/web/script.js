// Ganahl Lumber AI Capabilities Demo - Main JavaScript

// Mock data for the application
const mockData = {
    inventory: {
        lumber: [
            {
                id: "2x4-df",
                name: "2x4 Douglas Fir",
                category: "Dimensional Lumber",
                unit: "pieces",
                current_stock: 500,
                min_stock_level: 200,
                reorder_point: 300,
                weekly_sales: 100,
                upcoming_orders: 300,
                days_until_shortage: 5,
                priority: "high"
            },
            {
                id: "cedar-decking",
                name: "Cedar Decking",
                category: "Decking",
                unit: "board feet",
                current_stock: 600,
                min_stock_level: 400,
                reorder_point: 500,
                weekly_sales: 75,
                upcoming_orders: 200,
                days_until_shortage: 12,
                priority: "medium"
            },
            {
                id: "oak-flooring",
                name: "Oak Flooring",
                category: "Flooring",
                unit: "board feet",
                current_stock: 1200,
                min_stock_level: 800,
                reorder_point: 1000,
                weekly_sales: 90,
                upcoming_orders: 0,
                days_until_shortage: 30,
                priority: "low"
            }
        ],
        sheet_goods: [
            {
                id: "plywood-1/2",
                name: "1/2\" Plywood Sheathing",
                category: "Sheet Goods",
                unit: "sheets",
                current_stock: 200,
                min_stock_level: 100,
                reorder_point: 150,
                weekly_sales: 50,
                upcoming_orders: 100,
                days_until_shortage: 10,
                priority: "medium"
            }
        ],
        hardware: [
            {
                id: "nails-common-3in",
                name: "3\" Common Nails",
                category: "Fasteners",
                unit: "pieces",
                current_stock: 10000,
                min_stock_level: 5000,
                reorder_point: 7000,
                weekly_sales: 2000,
                upcoming_orders: 1500,
                days_until_shortage: 25,
                priority: "low"
            }
        ]
    },
    purchase_orders: {
        initial: [
            {
                product_id: "2x4-df",
                product_name: "2x4 Douglas Fir",
                quantity: 500,
                supplier: "Pacific Northwest Timber",
                lead_time: 5,
                total_cost: 2875.00,
                priority: "high",
                reasoning: "Predicted shortage in 5 days, prioritized due to upcoming order"
            },
            {
                product_id: "plywood-1/2",
                product_name: "1/2\" Plywood Sheathing",
                quantity: 300,
                supplier: "Georgia Pacific",
                lead_time: 6,
                total_cost: 9750.00,
                priority: "medium",
                reasoning: "Stock will be below reorder point after fulfilling upcoming orders"
            },
            {
                product_id: "cedar-decking",
                product_name: "Cedar Decking",
                quantity: 400,
                supplier: "Western Cedar Products",
                lead_time: 7,
                total_cost: 1700.00,
                priority: "medium",
                reasoning: "Regular restocking based on current inventory levels and standard sales trends"
            },
            {
                product_id: "nails-common-3in",
                product_name: "3\" Common Nails",
                quantity: 5000,
                supplier: "Stanley Black & Decker",
                lead_time: 3,
                total_cost: 250.00,
                priority: "low",
                reasoning: "Maintaining optimal stock levels"
            }
        ],
        updated: [
            {
                product_id: "2x4-df",
                product_name: "2x4 Douglas Fir",
                quantity: 500,
                supplier: "Pacific Northwest Timber",
                lead_time: 5,
                total_cost: 2875.00,
                priority: "high",
                reasoning: "Predicted shortage in 5 days, prioritized due to upcoming order"
            },
            {
                product_id: "plywood-1/2",
                product_name: "1/2\" Plywood Sheathing",
                quantity: 300,
                supplier: "Georgia Pacific",
                lead_time: 6,
                total_cost: 9750.00,
                priority: "medium",
                reasoning: "Stock will be below reorder point after fulfilling upcoming orders"
            },
            {
                product_id: "cedar-decking",
                product_name: "Cedar Decking",
                quantity: 1400,
                supplier: "Premium Decking Supply",
                lead_time: 3,
                total_cost: 5950.00,
                priority: "critical",
                reasoning: "Shifted to faster supplier to meet sudden demand spike while maintaining safety stock"
            },
            {
                product_id: "nails-common-3in",
                product_name: "3\" Common Nails",
                quantity: 5000,
                supplier: "Stanley Black & Decker",
                lead_time: 3,
                total_cost: 250.00,
                priority: "low",
                reasoning: "Maintaining optimal stock levels"
            }
        ]
    },
    adaptability: {
        scenario: {
            product_id: "cedar-decking",
            product_name: "Cedar Decking",
            quantity: 1000,
            required_by: "7 days",
            primary_supplier: "Western Cedar Products",
            primary_lead_time: 7,
            alternative_supplier: "Premium Decking Supply",
            alternative_lead_time: 3
        },
        log_messages: [
            "ALERT: Detected sudden demand spike for Cedar Decking - 1,000 units needed by April 2, 2025",
            "ADJUSTMENT: Added demand spike of 1,000 units to Cedar Decking upcoming demand",
            "CRITICAL: Cedar Decking has insufficient stock to meet demand. Projected stock (-400) is negative - cannot fulfill all orders",
            "STRATEGY: Switched from Western Cedar Products (lead time: 7 days) to Premium Decking Supply (lead time: 3 days) for faster delivery of Cedar Decking",
            "ACTION: Increased order quantity from 400 to 1,400 board feet to account for demand spike and maintain safety stock",
            "RESULT: New purchase order created with Premium Decking Supply for 1,400 board feet of Cedar Decking with expected delivery by March 29, 2025"
        ]
    },
    command_processing: {
        example: {
            command: "Plan a delivery schedule for 500 board feet of cedar next week",
            response: "Delivery of 500 board feet of Cedar Decking scheduled for Monday, March 31, 2025.\nLogistics: 1 truck(s), 2 hour(s) total delivery time.\nStock check: 600 units available, 100 units will remain after delivery.",
            reasoning: [
                "Received command: 'Plan a delivery schedule for 500 board feet of cedar next week'",
                "Identified delivery scheduling request for 500 board feet of cedar",
                "Found matching inventory item: Cedar Decking (ID: cedar-decking) with current stock of 600 units",
                "Checked if we have enough stock: 600 units available > 500 units requested",
                "Calculated logistics: 1 truck(s) needed, 2 hours total delivery time",
                "Scheduled for next week on Monday, March 31"
            ]
        }
    },
    customer_service: {
        example: {
            inquiry: "Do you have enough oak flooring for a 1,000-square-foot project, deliverable by Friday?",
            response: "Yes, we can deliver by your requested date of Friday, March 28.\n\nWe have 1,200 board feet of Oak Flooring in stock, which is sufficient for your 1,000 sq ft project.\n\nDelivery details: 2 truck(s), estimated 4 hour(s) delivery time.\n\nBackup: If needed, we can source an additional 500 board feet from our nearby warehouse.",
            reasoning: [
                "Received inquiry: 'Do you have enough oak flooring for a 1,000-square-foot project, deliverable by Friday?'",
                "Analyzing inquiry for product, quantity, and delivery date requirements",
                "Identified request for 1000 sq ft of oak flooring needed by Friday, March 28",
                "Found matching inventory item: Oak Flooring (ID: oak-flooring) with current stock of 1200 units",
                "Sufficient stock available: 1200 board feet (need 1000)",
                "Calculated logistics: 2 truck(s) needed, 4 hours total delivery time",
                "Standard delivery possible by requested date (Friday)",
                "After fulfilling this order, 200 board feet will remain in stock",
                "Remaining stock (200) will be below reorder point (1000). Should trigger reorder process."
            ],
            delivery_schedule: {
                material: "Oak Flooring",
                quantity: 1000,
                units: "board feet",
                delivery_date: "2025-03-28",
                delivery_day: "Friday",
                trucks_required: 2,
                estimated_hours: 4,
                status: "Confirmed"
            }
        }
    },
    business_impact: {
        categories: [
            {
                name: "Inventory Management",
                value: 69140,
                metrics: "5 hours/week saved, 1.5% stockout reduction, 5% overstock reduction"
            },
            {
                name: "Order Processing",
                value: 43870,
                metrics: "10 min/order saved, 3.5% accuracy improvement"
            },
            {
                name: "Logistics Optimization",
                value: 90360,
                metrics: "15% route efficiency, 15% truck utilization improvement"
            },
            {
                name: "Customer Service",
                value: 104820,
                metrics: "3.8 hour response time improvement, 7% satisfaction increase"
            }
        ],
        total: 308190,
        roi: "500-700% over 5 years"
    }
};

// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    // Inventory Management Section
    const refreshInventoryBtn = document.getElementById('refresh-inventory');
    
    // Adaptability Section
    const triggerScenarioBtn = document.getElementById('trigger-scenario');
    const adaptationLog = document.getElementById('adaptation-log');
    
    // Command Processing Section
    const commandInput = document.getElementById('command-text');
    const submitCommandBtn = document.getElementById('submit-command');
    const commandResponse = document.getElementById('command-response');
    const commandReasoning = document.getElementById('command-reasoning');
    
    // Customer Service Section
    const customerExample = document.getElementById('customer-example');
    const customerResponseArea = document.getElementById('customer-response-area');
    const customerResponse = document.getElementById('customer-response');
    const customerReasoning = document.getElementById('customer-reasoning');
    
    // Initialize event listeners
    initEventListeners();
    
    // Initialize the page
    function initEventListeners() {
        // Inventory Management
        if (refreshInventoryBtn) {
            refreshInventoryBtn.addEventListener('click', handleRefreshInventory);
        }
        
        // Adaptability
        if (triggerScenarioBtn) {
            triggerScenarioBtn.addEventListener('click', handleTriggerScenario);
        }
        
        // Command Processing
        if (submitCommandBtn) {
            submitCommandBtn.addEventListener('click', handleSubmitCommand);
        }
        
        if (commandInput) {
            commandInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    handleSubmitCommand();
                }
            });
        }
        
        // Customer Service
        if (customerExample) {
            customerExample.addEventListener('click', handleCustomerExample);
        }
    }
    
    // Inventory Management Handlers
    function handleRefreshInventory() {
        refreshInventoryBtn.textContent = "Refreshing...";
        refreshInventoryBtn.disabled = true;
        
        // Simulate refresh delay
        setTimeout(function() {
            // Update inventory stats with slight variations
            const statCards = document.querySelectorAll('.stat-card .stat-value');
            if (statCards.length >= 4) {
                // Randomly adjust values slightly
                const newValues = [
                    Math.floor(mockData.inventory.lumber[0].current_stock * (0.95 + Math.random() * 0.1)),
                    Math.floor(mockData.inventory.sheet_goods[0].current_stock * (0.95 + Math.random() * 0.1)),
                    Math.floor(mockData.inventory.hardware[0].current_stock * (0.95 + Math.random() * 0.1)),
                    Math.max(1, Math.floor(mockData.inventory.lumber[0].days_until_shortage * (0.9 + Math.random() * 0.2)))
                ];
                
                // Animate the changes
                statCards.forEach((card, index) => {
                    const originalValue = parseInt(card.textContent);
                    const newValue = newValues[index];
                    animateValue(card, originalValue, newValue, 1000);
                });
            }
            
            refreshInventoryBtn.textContent = "Refresh Data";
            refreshInventoryBtn.disabled = false;
        }, 1000);
    }
    
    // Adaptability Handlers
    function handleTriggerScenario() {
        triggerScenarioBtn.textContent = "Processing...";
        triggerScenarioBtn.disabled = true;
        
        // Reset the log
        adaptationLog.innerHTML = "Simulating demand spike...\n\n";
        
        // Simulate typing effect for the log
        let i = 0;
        function typeNextMessage() {
            if (i < mockData.adaptability.log_messages.length) {
                adaptationLog.innerHTML += mockData.adaptability.log_messages[i] + "\n";
                i++;
                setTimeout(typeNextMessage, 800);
            } else {
                triggerScenarioBtn.textContent = "Scenario Complete";
                setTimeout(function() {
                    triggerScenarioBtn.textContent = "Reset Scenario";
                    triggerScenarioBtn.disabled = false;
                }, 2000);
            }
        }
        
        setTimeout(typeNextMessage, 1000);
    }
    
    // Command Processing Handlers
    function handleSubmitCommand() {
        const commandText = commandInput.value.trim();
        if (!commandText) return;
        
        // Display loading state
        commandResponse.textContent = "Processing command...";
        commandReasoning.textContent = "Analyzing...";
        
        // Simulate processing delay
        setTimeout(function() {
            if (commandText.toLowerCase().includes('cedar') && 
                (commandText.toLowerCase().includes('delivery') || 
                 commandText.toLowerCase().includes('schedule'))) {
                
                commandResponse.textContent = mockData.command_processing.example.response;
                commandReasoning.textContent = mockData.command_processing.example.reasoning.join("\n");
            } else {
                commandResponse.textContent = 
                    "I couldn't understand that command. Try asking me to plan a delivery schedule for a specific quantity of material.";
                
                commandReasoning.textContent = 
                    "- Received command: '" + commandText + "'\n" +
                    "- Command not recognized as a delivery scheduling request\n" +
                    "- Suggested format: 'Plan a delivery schedule for [quantity] board feet of [material] next week'";
            }
        }, 1000);
    }
    
    // Customer Service Handlers
    function handleCustomerExample() {
        customerResponseArea.style.display = 'block';
        customerExample.style.display = 'none';
        
        // Animate the response appearing
        customerResponse.style.opacity = 0;
        customerReasoning.style.opacity = 0;
        
        setTimeout(function() {
            customerResponse.style.opacity = 1;
            customerResponse.style.transition = 'opacity 1s';
            
            setTimeout(function() {
                customerReasoning.style.opacity = 1;
                customerReasoning.style.transition = 'opacity 1s';
            }, 500);
        }, 300);
    }
    
    // Utility Functions
    function animateValue(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = Math.floor(progress * (end - start) + start);
            element.textContent = value;
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
    
    // Mobile responsiveness enhancements
    function enhanceMobileExperience() {
        // Check if we're on a mobile device
        const isMobile = window.innerWidth <= 768;
        
        if (isMobile) {
            // Adjust table displays for better mobile viewing
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                table.classList.add('mobile-friendly');
            });
            
            // Ensure command input is easily accessible
            const commandSection = document.getElementById('command');
            if (commandSection) {
                commandSection.scrollIntoView({ behavior: 'smooth' });
            }
        }
    }
    
    // Call mobile enhancements on load and resize
    enhanceMobileExperience();
    window.addEventListener('resize', enhanceMobileExperience);
});
