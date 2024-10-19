import tkinter as tk
from tkinter import ttk

def create_filter_frame(parent, apply_filters_callback):
    filter_frame = tk.Frame(parent)
    filter_frame.pack(pady=5)

    filter_title = tk.Label(filter_frame, text="Inventory Filters", font=("Arial", 12, "bold"))
    filter_title.pack(pady=(0, 5))

    object_type_label = tk.Label(filter_frame, text="Object Type:")
    object_type_label.pack(side=tk.LEFT, padx=(0, 5))
    object_type_var = tk.StringVar()
    object_type_combo = ttk.Combobox(filter_frame, textvariable=object_type_var, state="readonly")
    object_type_combo.pack(side=tk.LEFT, padx=(0, 10))
    object_type_combo.bind("<<ComboboxSelected>>", apply_filters_callback)

    weapon_type_label = tk.Label(filter_frame, text="Weapon Type:")
    weapon_type_label.pack(side=tk.LEFT, padx=(0, 5))
    weapon_type_var = tk.StringVar()
    weapon_type_combo = ttk.Combobox(filter_frame, textvariable=weapon_type_var, state="readonly")
    weapon_type_combo.pack(side=tk.LEFT)
    weapon_type_combo.bind("<<ComboboxSelected>>", apply_filters_callback)

    level_frame = tk.Frame(filter_frame)
    level_frame.pack(side=tk.LEFT, padx=(10, 5))
    tk.Label(level_frame, text="Level:").pack(side=tk.LEFT)
    min_level_var = tk.StringVar()
    tk.Entry(level_frame, textvariable=min_level_var, width=5).pack(side=tk.LEFT)
    tk.Label(level_frame, text="-").pack(side=tk.LEFT)
    max_level_var = tk.StringVar()
    tk.Entry(level_frame, textvariable=max_level_var, width=5).pack(side=tk.LEFT)

    filter_vars = {
        'object_type_var': object_type_var,
        'object_type_combo': object_type_combo,
        'weapon_type_var': weapon_type_var,
        'weapon_type_combo': weapon_type_combo,
        'min_level_var': min_level_var,
        'max_level_var': max_level_var
    }

    return filter_frame, filter_vars

def create_checkbox_frame(parent, apply_filters_callback):
    checkbox_frame = tk.Frame(parent)
    checkbox_frame.pack(pady=5)

    attributes = ['Hit Roll', 'Damago Roll', 'Wisdom', 'Intelligence', 'Strength', 'Constitution', 'Dexterity', 'HP', 'Mana']
    attribute_vars = {}
    tk.Label(checkbox_frame, text="Attributes:").pack(side=tk.LEFT)
    for attr in attributes:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(checkbox_frame, text=attr, variable=var, command=apply_filters_callback)
        cb.pack(side=tk.LEFT)
        attribute_vars[attr.lower().replace(' ', '_')] = var

    return checkbox_frame, attribute_vars

def create_search_frame(parent, apply_filters_callback):
    search_frame = tk.Frame(parent)
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=30)
    search_entry.pack(side=tk.LEFT)
    search_entry.bind("<KeyRelease>", apply_filters_callback)

    return search_frame, search_var

def create_treeview(parent, sort_callback):
    tree = ttk.Treeview(parent, columns=("id", "name", "level", "hit_roll", "damago_roll", "full_roll", "wisdom", "intelligence", "strength", "constitution", "dexterity", "mana", "hp", "proteccion_class", "penetracion", "golpe", "corte", "magia"), show="headings")
    
    columns = [
        ("id", "ID", 50),
        ("name", "Name", 150),
        ("level", "Level", 50),
        ("hit_roll", "Hit Roll", 70),
        ("damago_roll", "Damago Roll", 70),
        ("full_roll", "Full Roll", 70),
        ("wisdom", "Wisdom", 70),
        ("intelligence", "Intelligence", 70),
        ("strength", "Strength", 70),
        ("constitution", "Constitution", 70),
        ("dexterity", "Dexterity", 70),
        ("mana", "Mana", 70),
        ("hp", "HP", 70),
        ("proteccion_class", "Proteccion Class", 70),
        ("penetracion", "Penetracion", 70),
        ("golpe", "Golpe", 70),
        ("corte", "Corte", 70),
        ("magia", "Magia", 70)
    ]

    for col, heading, width in columns:
        tree.heading(col, text=heading, command=lambda c=col: sort_callback(c, False))
        tree.column(col, width=width)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)

    return tree