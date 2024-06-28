import json

class PlayerInventory:
    def __init__(self):
        self.inventory = {
            "weapons": [],
            "armor": []
        }
        self._save_inventory_to_json("player_inventory.json")  # Initial save

    def _save_inventory_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.inventory, f, indent=4)
        print(f"Inventory saved to {filename}")

    def add_weapon(self, weapon_name):
        self.inventory["weapons"].append(weapon_name)
        self._save_inventory_to_json("player_inventory.json")  # Save after adding weapon

    def add_armor(self, armor_name):
        self.inventory["armor"].append(armor_name)
        self._save_inventory_to_json("player_inventory.json")  # Save after adding armor
