import tkinter as tk
from tkinter import filedialog, ttk
from item_parser import parse_inventory
from gui_components import create_filter_frame, create_checkbox_frame, create_search_frame, create_treeview
from utils import sort_column, filter_item
import os

class InventoryViewer:
    def __init__(self, master, application_path):
        self.master = master
        self.master.title("Petria Inventory Viewer")
        self.master.geometry("1400x700")

        icon_path = os.path.join(application_path, 'img', 'icon.ico')
        if os.path.exists(icon_path):
            self.master.iconbitmap(icon_path)

        self.items = []
        self.original_content = ""

        self.setup_gui()
        
        # Check if inventario.txt exists in the current directory
        if os.path.exists("inventario.txt"):
            self.load_file("inventario.txt")

    def setup_gui(self):
        self.load_button = tk.Button(self.master, text="Load Inventory File", command=self.load_file)
        self.load_button.pack(pady=10)
        
        top_container = tk.Frame(self.master)
        top_container.pack(pady=10, fill=tk.X)

        self.filter_frame, self.filter_vars = create_filter_frame(top_container, self.apply_filters)
        self.checkbox_frame, self.attribute_vars = create_checkbox_frame(top_container, self.apply_filters)
        self.search_frame, self.search_var = create_search_frame(self.master, self.apply_filters)

        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=5, fill=tk.X)
        self.update_filters_button = tk.Button(button_frame, text="Update Filters", command=self.apply_filters)
        self.update_filters_button.pack()

        tree_frame = tk.Frame(self.master)
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tree = create_treeview(tree_frame, self.sort_column)
        self.tree.bind("<<TreeviewSelect>>", self.show_item_details)

        self.details_text = tk.Text(self.master, height=15, width=70)
        self.details_text.pack(pady=10)
                
    def load_file(self, filename=None):
        if filename:
            file_path = filename
        else:
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        
        print(f"Attempting to load file: {file_path}")
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.original_content = file.read()
                
                print(f"File loaded successfully. Content length: {len(self.original_content)}")
                
                self.items = parse_inventory(self.original_content)
                self.items.sort(key=lambda x: x.get('level', 0))
                self.update_filter_options()
                self.update_item_list()
            except Exception as e:
                print(f"Error loading file: {e}")
        else:
            print("No file selected")

    def update_filter_options(self):
        object_types = set(item['type'] for item in self.items if 'type' in item)
        weapon_types = set(item.get('weapon_type', '') for item in self.items if 'weapon_type' in item)
        weapon_types.discard('')

        self.filter_vars['object_type_combo']['values'] = ['All'] + list(sorted(object_types))
        self.filter_vars['object_type_combo'].set('All')

        self.filter_vars['weapon_type_combo']['values'] = ['All'] + list(sorted(weapon_types))
        self.filter_vars['weapon_type_combo'].set('All')

        min_level = min(item.get('level', 0) for item in self.items)
        max_level = max(item.get('level', 0) for item in self.items)
        self.filter_vars['min_level_var'].set(str(min_level))
        self.filter_vars['max_level_var'].set(str(max_level))

    def apply_filters(self, event=None):
        self.update_item_list()

    def update_item_list(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.items:
            if filter_item(item, self.filter_vars, self.attribute_vars, self.search_var.get()):
                hit_roll = item.get('hit_roll', 0)
                damago_roll = item.get('damago_roll', 0)
                full_roll = hit_roll + damago_roll
                values = [
                    item.get('id', ''),
                    item.get('name', ''),
                    item.get('level', 0),
                    hit_roll,
                    damago_roll,
                    full_roll,
                    item.get('wisdom', 0),
                    item.get('intelligence', 0),
                    item.get('strength', 0),
                    item.get('constitution', 0),
                    item.get('dexterity', 0),
                    item.get('mana', 0),
                    item.get('hp', 0),
                    item.get('proteccion_class', 0),
                    item.get('penetracion', 0),
                    item.get('golpe', 0),
                    item.get('corte', 0),
                    item.get('magia', 0)
                ]
                self.tree.insert("", "end", values=values)
                
    def sort_column(self, col, reverse):
        if col != "level":
            # If sorting by a column other than level, sort by that column first, then by level
            l = [(self.tree.set(k, col), self.tree.set(k, "level"), k) for k in self.tree.get_children('')]
            l.sort(key=lambda t: (self.convert_value(t[0]), int(t[1])), reverse=reverse)
        else:
            # If sorting by level, just sort by level
            l = [(self.tree.set(k, "level"), k) for k in self.tree.get_children('')]
            l.sort(key=lambda t: int(t[0]), reverse=reverse)

        for index, (val, *rest) in enumerate(l):
            self.tree.move(rest[-1], '', index)

        # Update column headers
        for header in self.tree["columns"]:
            if header == col:
                self.tree.heading(header, text=f"{header.capitalize()} {'↓' if reverse else '↑'}", command=lambda c=header: self.sort_column(c, not reverse))
            else:
                self.tree.heading(header, text=header.capitalize(), command=lambda c=header: self.sort_column(c, False))

        # Always keep "Level" column header with an up arrow
        if col != "level":
            self.tree.heading("level", text="Level ↑")

    def convert_value(self, value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    def show_item_details(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = int(self.tree.item(selected_item)['values'][0])
            print(f"Selected item ID: {item_id}")
            item = next((item for item in self.items if item['id'] == item_id), None)
            if item:
                print(f"Found item: {item['name']}")
                if 'raw_content' in item:
                    self.details_text.delete(1.0, tk.END)
                    self.details_text.insert(tk.END, item['raw_content'])
                else:
                    self.details_text.delete(1.0, tk.END)
                    self.details_text.insert(tk.END, f"Raw content not found for item '{item['name']}' (ID: {item_id})")
            else:
                print(f"Item with ID {item_id} not found")
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, f"Item with ID {item_id} not found")