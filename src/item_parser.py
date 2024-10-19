import re

def parse_inventory(content):
    items = []
    current_item = {}
    item_id = 0
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith("El objeto"):
            if current_item:
                items.append(current_item)
                current_item = {}
            item_id += 1
            match = re.match(r"El objeto '(.+)' es del tipo (.+), extra flags (.+)", line)
            if match:
                current_item['id'] = item_id
                current_item['name'] = match.group(1)
                current_item['type'] = match.group(2)
                current_item['flags'] = match.group(3).split()
                
                # Store the raw content for this item
                end_index = next((j for j in range(i+1, len(lines)) if lines[j].strip() == ""), len(lines))
                current_item['raw_content'] = '\n'.join(lines[i:end_index])
        elif line.startswith("Su peso"):
            match = re.match(r"Su peso es de (\d+), su valor (\d+), su nivel (\d+)", line)
            if match:
                current_item['weight'] = int(match.group(1))
                current_item['value'] = int(match.group(2))
                current_item['level'] = int(match.group(3))
        elif line.startswith("El arma es del tipo"):
            match = re.match(r"El arma es del tipo (.+)\.", line)
            if match:
                current_item['weapon_type'] = match.group(1)
        elif line.startswith("Lesiones de"):
            match = re.match(r"Lesiones de (\d+)d(\d+) \(media de (\d+)\)", line)
            if match:
                current_item['damage'] = f"{match.group(1)}d{match.group(2)}"
                current_item['avg_damage'] = int(match.group(3))
        elif line.startswith("Afecta al"):
            match = re.match(r"Afecta al (.+) en (-?\d+)", line)
            if match:
                attribute = match.group(1).lower().replace(' ', '_')
                value = int(match.group(2))
                current_item[attribute] = value
        elif line.startswith("Protege en"):
            match = re.match(r"Protege en (\d+) vs penetracion, (\d+) vs golpe, (\d+) vs corte y (\d+) vs magia", line)
            if match:
                current_item['penetracion'] = int(match.group(1))
                current_item['golpe'] = int(match.group(2))
                current_item['corte'] = int(match.group(3))
                current_item['magia'] = int(match.group(4))
        else:
            # Check for other attributes
            attributes = [
                ('hit roll', 'hit_roll'),
                ('damago roll', 'damago_roll'),
                ('proteccion class', 'proteccion_class'),
                ('wisdom', 'wisdom'),
                ('intelligence', 'intelligence'),
                ('strength', 'strength'),
                ('constitution', 'constitution'),
                ('dexterity', 'dexterity'),
                ('mana', 'mana'),
                ('hp', 'hp')
            ]
            for attr, key in attributes:
                match = re.search(rf"{attr} en (-?\d+)", line, re.IGNORECASE)
                if match:
                    current_item[key] = int(match.group(1))

    if current_item:
        items.append(current_item)

    return items