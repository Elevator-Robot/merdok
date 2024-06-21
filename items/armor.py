from item import Item

class Armor(Item):
    def __init__(self, name, description, defense):
        super().__init__(name, description)
        self.defense = defense

    def use(self, character):
        # Implement armor usage logic
        character.defend(self.defense)
