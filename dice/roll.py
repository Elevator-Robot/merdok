import random


class Dice:
    def d5_roll(self):
        return random.randint(1,5)
    def d10_roll(self):
        return random.randint(1,10)
    def d20_roll(self):
        return random.randint(1,20)