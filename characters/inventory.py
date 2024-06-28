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

    def add_weapon(self, weapon_name, damage):
        weapon = {
            "name": weapon_name,
            "damage": damage
        }
        self.inventory["weapons"].append(weapon)
        self._save_inventory_to_json("player_inventory.json")

    def add_armor(self, armor_name, defense):
        armor = {
            "name": armor_name,
            "defense": defense
        }
        self.inventory["armor"].append(armor)
        self._save_inventory_to_json("player_inventory.json")
