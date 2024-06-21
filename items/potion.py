from item import Item

class Potion(Item):
    def __init__(self, name, description, effect):
        super().__init__(name, description)
        self.effect = effect

    def use(self, character):
        # Implement potion usage logic
        character.apply_effect(self.effect)
