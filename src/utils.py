def sort_column(self, col, reverse):
    l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
    
    def convert(value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    l.sort(key=lambda t: convert(t[0]), reverse=reverse)

    for index, (val, k) in enumerate(l):
        self.tree.move(k, '', index)

    self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    if col != "level":
        self.tree.heading("level", command=lambda: self.sort_column("level", False))

def filter_item(item, filter_vars, attribute_vars, search_term):
    object_type_filter = filter_vars['object_type_var'].get()
    weapon_type_filter = filter_vars['weapon_type_var'].get()
    min_level = filter_vars['min_level_var'].get()
    max_level = filter_vars['max_level_var'].get()

    if object_type_filter != 'All' and item.get('type', '') != object_type_filter:
        return False

    if weapon_type_filter != 'All':
        if 'weapon_type' not in item or item['weapon_type'] != weapon_type_filter:
            return False

    item_level = item.get('level', 0)
    if min_level and max_level:
        try:
            if not (int(min_level) <= item_level <= int(max_level)):
                return False
        except ValueError:
            pass

    for attr, var in attribute_vars.items():
        if var.get() and attr not in item:
            return False

    if search_term:
        item_name = item.get('name', '').lower()
        if search_term.lower() not in item_name:
            return False

    return True