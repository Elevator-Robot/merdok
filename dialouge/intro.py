import time

from characters import enemy, player
from characters.inventory import PlayerInventory
from dice.roll import Dice

class GameIntroduction:
    def __init__(self):
        self.player_name = ""
        self.player_inventory = PlayerInventory()
        self.dice = Dice()
        self.player = player.Player(health=10, name="Prisoner")
        self.enemy = enemy.Enemy(health=10, name="Champion")

    def set_weapon(self):
        print("\n'You may choose 1 weapon to try and salvage your life... Choose wisely.'")
        time.sleep(2)

        while True:
            weapon_choice = input("""
                                \nChoose your weapon:
                                \n 1: sword
                                \n 2: axe
                                \n 3: bow
                                \n 4: staff
                                \n Enter number:""").strip()
            if weapon_choice == "1":
                self.player_inventory.add_weapon("sword", damage=4)
                print("\nYou feel the weight of the sword in your hand, the blade gleaming in the torchlight. +4 strength has been added to your stats.")
                break
            elif weapon_choice == "2":
                self.player_inventory.add_weapon("axe", damage=4)
                print("\nYou feel the weight of the axe in your hand, the blade gleaming in the torchlight. +4 strength has been added to your stats.")
                break
            elif weapon_choice == "3":
                self.player_inventory.add_weapon("bow", damage=4)
                print("\nYou feel the tension of the bowstring as you draw it back, the arrow poised to strike. +4 strength has been added to your stats.")
                break
            elif weapon_choice == "4":
                self.player_inventory.add_weapon("staff", damage=4)
                print("\nYou feel the power of the staff coursing through your veins, the magic within it waiting to be unleashed. +2 intelligence has been added to your stats.")
                break
            else:
                print("\nThat is not a valid weapon choice. Choose again.")
                continue

    def continue_arena(self):
        print("\nAhh, the prisoner has chosen their weapon. Very well, let us proceed to the arena where their fate shall be decided.")
        time.sleep(2)

        print("\nThey are dragged through a series of winding corridors, the torchlight flickering off the ancient stones. The air grows colder with each step, and the sense of foreboding in their chest deepens.")
        time.sleep(2)

        print("\nFinally, they emerge into a vast, circular chamber, the walls lined with towering statues and the floor covered in sand and bloodstains. The crowd roars as they are led to the center of the arena, the sound echoing in their ears like thunder.")
        time.sleep(2)

        print("\nThey steel themselves for the battle to come, their heart pounding in their chest. The figure who spoke before steps forward once more, their voice ringing out over the crowd.")
        time.sleep(2)

        print("\n'Let the battle begin!'")
        time.sleep(2)

    def start_introduction(self):
        print("\nThe first thing you notice as you regain consciousness is the cold, unyielding stone beneath you.")
        time.sleep(2)

        print("\nThe air is thick with the scent of dust and decay, and the only sound is the distant echo of your own heartbeat.")
        time.sleep(2)

        print("\nYou open your eyes to find yourself in a dimly lit chamber, the walls lined with ancient runes and symbols that seem to pulse with an otherworldly energy.")
        time.sleep(2)

        print("\nAs you struggle to your feet, you realize that you have no memory of how you came to be here, or even who you are.")
        time.sleep(2)

        print("\nAn angry voice yells in the darkness, 'Take that prisoner to the arena where he shall be masecured in front of our people.'")
        time.sleep(2)

        print("\nYou feel a surge of panic as you realize that you are not alone.")
        time.sleep(2)

        print("\nA group of shadowy figures surrounds you, their faces obscured by hoods and masks. You try to speak, but your voice catches in your throat.")
        time.sleep(2)

        print("\nOne of the figures steps forward, a glint of malice in their eyes. 'You have been chosen, mortal. Chosen to face the trials of the arena, to prove your worth in the eyes of the gods.'")
        time.sleep(2)

        self.set_weapon()

        self.continue_arena()

        self.battle()

    def battle(self):
        print("\nYou stand in the center of the arena, your weapon at the ready, your heart pounding in your chest.")
        time.sleep(2)

        print("\nYour opponent emerges from the shadows, a massive, hulking figure clad in armor and wielding a wicked-looking blade.")
        time.sleep(2)

        print("\nYou steel yourself for the battle to come, your muscles tensed, your mind focused.")
        time.sleep(2)

        print("\nThe figure charges at you, their blade raised high, a battle cry on their lips.")
        time.sleep(2)

        print("\nYou raise your weapon to meet their attack, the clash of steel ringing out through the arena.")
        time.sleep(2)

        user_roll = self.dice.d20_roll()
        print(f"\nYou roll a {user_roll}")
        time.sleep(2)

        enemy_roll = self.dice.d20_roll()
        print(f"\nThe enemy rolls a {enemy_roll}")
        time.sleep(2)

        if user_roll > enemy_roll:
            print("\nYou strike a mighty blow, the force of your attack sending your opponent reeling.")
            self.enemy.take_damage(5)
        elif user_roll < enemy_roll:
            print("\nYour opponent's blade finds its mark, cutting through your defenses and drawing blood.")
            self.player.take_damage(5)
        else:
            print("\nYour weapons clash, the two of you locked in a fierce struggle for dominance.")


