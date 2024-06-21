class Enemy:
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
    enemy = Enemy("Goblin", 50)
    print(enemy)
    enemy.take_damage(10)
    print(enemy)
    enemy.heal(5)
    print(enemy)
    enemy.add_to_inventory("Gold")
    print(enemy)
    enemy.remove_from_inventory("Gold")
    print(enemy)
