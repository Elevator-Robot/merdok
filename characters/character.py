import json

class CharacterStats:
    def __init__(self):
        self.stats = {
            "strength": 0,
            "dexterity": 0,
            "intelligence": 0,
            "charisma": 0
        }
        self._save_stats_to_json("character_stats.json")  # Initial save

    def _save_stats_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.stats, f, indent=4)
        print(f"Stats saved to {filename}")

    def update_stat(self, stat_name, value):
        if stat_name in self.stats:
            self.stats[stat_name] = value
            self._save_stats_to_json("character_stats.json")  # Save after updating stat
        else:
            print(f"Stat {stat_name} does not exist")
