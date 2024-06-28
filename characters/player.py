class Player:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.inventory = []

    def take_damage(self, damage):
        self.health -= damage

    def heal(self, amount):
        self.health += amount

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def __str__(self):
        return f"{self.name}: {self.health} HP - Inventory: {self.inventory}"

if __name__ == "__main__":
    player = Player("Greg", 100)
    print(player)
    player.take_damage(10)
    print(player)
    player.heal(5)
    print(player)
