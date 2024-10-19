# Petria Inventory Viewer

## Description
PyPetriaInventory is a Python application that allows users to load, view, and filter inventory items from a text file. It provides a graphical user interface for easy interaction with the inventory data.

## Features
- Load the Petria inventory files in text format
- Display Petria items in a sortable treeview
- Filter Petria items by various attributes:
  - Object type
  - Weapon type
  - Level range
  - Item attributes (Hit Roll, Damago Roll, Wisdom, Intelligence, etc.)
- Search items by name
- View detailed item information
- Automatically load 'inventario.txt' if present in the same directory

## Requirements
- Python 3.x
- tkinter

## Installation
1. Clone this repository:

`git clone https://github.com/SirLouen/petria-inventory-viewer.git`

2. Navigate to the project directory:

`cd inventory-viewer`

3. Run the main script:

`python inventory_viewer.py`

## Usage
1. Launch the application.
2. If 'inventario.txt' is in the same directory, it will be loaded automatically.
3. Otherwise, click "Load Inventory File" to select an inventory file.
4. Use the filters and search bar to find specific items.
5. Click on an item in the treeview to see its details.

## File Structure
- `main.py`: Entry point for the application	
- `inventory_viewer.py`: Main application file
- `gui_components.py`: GUI component creation functions
- `item_parser.py`: Functions for parsing inventory items
- `utils.py`: Utility functions for sorting and filtering

## Contributing
Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/SirLouen/petria-inventory-viewer/issues) if you want to contribute.

## License
[MIT](https://choosealicense.com/licenses/mit/)