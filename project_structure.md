# Project Structure Design for Ganahal Lumber AI Capabilities

## Directory Structure

```
ganahal-lumber/
├── docs/                     # Documentation files
│   ├── research/             # Research and analysis documents
│   │   ├── operational_context.md
│   │   ├── internal_needs_summary.md
│   │   └── business_impact_analysis.md
│   └── README.md             # Main project documentation
│
├── src/                      # Source code
│   ├── data/                 # Data files and structures
│   │   └── inventory_data.json
│   │
│   ├── logic/                # Business logic implementation
│   │   ├── inventory_restocking_logic.py
│   │   ├── inventory_adaptability.py
│   │   ├── interactive_command.py
│   │   └── customer_service_scenario.py
│   │
│   └── web/                  # Web interface files
│       ├── index.html        # Main webpage
│       ├── script.js         # JavaScript functionality
│       └── styles.css        # CSS styles (to be extracted from HTML)
│
└── .gitignore                # Git ignore file
```

## File Organization Logic

1. **Documentation (docs/)**
   - Contains all documentation files
   - Research documents in a dedicated subdirectory
   - README.md at the top level for easy access

2. **Source Code (src/)**
   - Separated into logical components:
     - **data/**: Contains JSON data structures
     - **logic/**: Contains Python implementation files
     - **web/**: Contains HTML, JavaScript, and CSS files

3. **Web Interface (src/web/)**
   - Main HTML file at the top level
   - JavaScript and CSS in separate files for better maintainability
   - CSS will be extracted from the current inline styles in HTML

## Implementation Plan

1. Create the directory structure
2. Extract CSS from HTML into a separate file
3. Move files to their appropriate locations
4. Update file references if needed
5. Commit the reorganized structure
6. Push to GitHub
7. Verify the repository structure
