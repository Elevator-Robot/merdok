from item import Item

class Weapon(Item):
    def __init__(self, name, description, damage):
        super().__init__(name, description)
        self.damage = damage

    def use(self, character):
        # Implement weapon usage logic
        character.attack(self.damage)
