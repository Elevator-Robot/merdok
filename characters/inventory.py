import json

class PlayerInventory:
    def __init__(self):
        self.inventory = {
            "weapons": [],
            "armor": []
        }

    def add_weapon(self, weapon_name):
        self.inventory["weapons"].append(weapon_name)

    def add_armor(self, armor_name):
        self.inventory["armor"].append(armor_name)

    def save_inventory_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.inventory, f, indent=4)
        print(f"Inventory saved to {filename}")
