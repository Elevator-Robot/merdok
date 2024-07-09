import textwrap
import time

from characters import enemy, player
from characters.character import CharacterStats
from characters.inventory import PlayerInventory
from dice.roll import Dice

class GameIntroduction:
    def __init__(self):
        self.player_name = ""
        self.player_inventory = PlayerInventory()
        self.dice = Dice()
        self.player = player.Player(health=10, name="Prisoner")
        self.enemy = enemy.Enemy(health=10, name="Champion")
        self.character_stats = CharacterStats()

    def format_text(self, text, wait=2):
        for line in textwrap.wrap(text, width=100):
            print(line)
            time.sleep(wait)


    def set_weapon(self):
        print("\n'You may choose 1 weapon to try and salvage your life... Choose wisely.'")
        time.sleep(2)

        while True:
            weapon_choice = input("""
Choose your weapon:
    1: sword
    2: axe
    3: bow
    4: staff
Enter number: """).strip()
            if weapon_choice == "1":
                self.player_inventory.add_weapon("sword", damage=4)
                self.character_stats.update_stat("strength", 4)
                self.format_text("You feel the weight of the sword in your hand, the blade gleaming in the torchlight. +4 strength has been added to your stats.")
                break
            elif weapon_choice == "2":
                self.player_inventory.add_weapon("axe", damage=4)
                self.character_stats.update_stat("strength", 4)
                self.format_text("You feel the weight of the axe in your hand, the blade gleaming in the torchlight. +4 strength has been added to your stats.")
                break
            elif weapon_choice == "3":
                self.player_inventory.add_weapon("bow", damage=4)
                self.character_stats.update_stat("dexterity", 4)
                self.format_text("You feel the tension of the bowstring as you draw it back, the arrow poised to strike. +4 dexterity has been added to your stats.")
                break
            elif weapon_choice == "4":
                self.player_inventory.add_weapon("staff", damage=4)
                self.character_stats.update_stat("intelligence", 4)
                self.format_text("You feel the power of the staff coursing through your veins, the magic within it waiting to be unleashed. +4 intelligence has been added to your stats.")
                break
            else:
                self.format_text("That is not a valid weapon choice. Choose again.")

    def continue_arena(self):
        arena_text = """Ahh, the prisoner has chosen their weapon. Very well, let us proceed to the arena where their fate shall be decided.
They are dragged through a series of winding corridors, the torchlight flickering off the ancient stones. The air grows colder with each step, and the sense of foreboding in their chest deepens.
Finally, they emerge into a vast, circular chamber, the walls lined with towering statues and the floor covered in sand and bloodstains. The crowd roars as they are led to the center of the arena, the sound echoing in their ears like thunder.
They steel themselves for the battle to come, their heart pounding in their chest. The figure who spoke before steps forward once more, their voice ringing out over the crowd.
'Let the battle begin!'
"""
        self.format_text(arena_text)

    def start_introduction(self):
        intro_text = """The first thing you notice as you regain consciousness is the cold, unyielding stone beneath you.
The air is thick with the scent of dust and decay, and the only sound is the distant echo of your own heartbeat.
You open your eyes to find yourself in a dimly lit chamber, the walls lined with ancient runes and symbols that seem to pulse with an otherworldly energy.
As you struggle to your feet, you realize that you have no memory of how you came to be here, or even who you are.
An angry voice yells in the darkness, 'Take that prisoner to the arena where he shall be masecured in front of our people.'
You feel a surge of panic as you realize that you are not alone.
A group of shadowy figures surrounds you, their faces obscured by hoods and masks. You try to speak, but your voice catches in your throat.
One of the figures steps forward, a glint of malice in their eyes. 'You have been chosen, mortal. Chosen to face the trials of the arena, to prove your worth in the eyes of the gods.'
        """

        self.format_text(intro_text)

        self.set_weapon()

        self.continue_arena()

        self.battle()

    def battle(self):
        battle_text = """You stand in the center of the arena, your weapon at the ready, your heart pounding in your chest.
Your opponent emerges from the shadows, a massive, hulking figure clad in armor and wielding a wicked-looking blade.
You steel yourself for the battle to come, your muscles tensed, your mind focused.
The figure charges at you, their blade raised high, a battle cry on their lips.
You raise your weapon to meet their attack, the clash of steel ringing out through the arena.
    """

        self.format_text(battle_text)

        #  Dice roll.. might get removed.
        user_roll = self.dice.d20_roll()
        self.format_text(f"You roll a {user_roll}")

        enemy_roll = self.dice.d20_roll()
        self.format_text(f"The enemy rolls a {enemy_roll}")

        if user_roll > enemy_roll:
            self.format_text("You strike a mighty blow, the force of your attack sending your opponent reeling.")
            self.enemy.take_damage(5)
        elif user_roll < enemy_roll:
            self.format_text("Your opponent's blade finds its mark, cutting through your defenses and drawing blood.")
            self.player.take_damage(5)
        else:
            self.format_text("Your weapons clash, the two of you locked in a fierce struggle for dominance.")
