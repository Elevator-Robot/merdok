"""Game Introduction Module"""
from characters.inventory import PlayerInventory
import sys

class GameIntroduction:
    def __init__(self):
        self.player_name = ""
        self.player_inventory = PlayerInventory()

    def shun_player(self):
        print("Cowardice does not become you. The world has no place for those who shirk from destiny. Begone, and let the true heroes forge their path without you.")
        sys.exit(0)

    def get_player_name(self):
        return self.player_name

    def set_player_name(self):
        self.player_name = input("Enter your name, hero: ")
        print(f"\nWelcome, {self.player_name}! Your journey begins now. May the gods watch over you as you face the trials that await...")

    def set_weapon(self):
        while True:
            weapon_choice = input("\nChoose your weapon (sword/bow/staff): ").lower().strip()
            if weapon_choice in ["sword", "bow", "staff"]:
                self.player_inventory.add_weapon(weapon_choice, damage=4)
                print(f"\nYou feel the rush of power as you wield the {weapon_choice}. Blood rushes through your veins... +4 strength has been added to your stats.")
                break
            else:
                print("\nThat is not a weapon of choice prisoner. Choose again.")

    def start_introduction(self):
        print("\nThe first thing you notice as you regain consciousness is the cold, unyielding stone beneath you. The air is thick with the scent of dust and decay, and the only sound is the distant echo of your own heartbeat.")
        print("\nYou open your eyes to find yourself in a dimly lit chamber, the walls lined with ancient runes and symbols that seem to pulse with an otherworldly energy. As you struggle to your feet, you realize that you have no memory of how you came to be here, or even who you are.")
        print("\nAn angry voice yells in the darkness, 'Take that prisoner to the arena where he shall be masecured in front of our people.'")
        print("\nYou feel a surge of panic as you realize that you are not alone. A group of shadowy figures surrounds you, their faces obscured by hoods and masks. You try to speak, but your voice catches in your throat.")
        print("\nOne of the figures steps forward, a glint of malice in their eyes. 'You have been chosen, mortal. Chosen to face the trials of the arena, to prove your worth in the eyes of the gods.'")
        print("\n'You may choose 1 weapon to try and salvage your life... Choose wisely.'")

        self.set_weapon()

        print("\nAhh, the prisoner has chosen his weapon. Very well, let us proceed to the arena where your fate shall be decided.")
        print("\nYou are dragged through a series of winding corridors, the torchlight flickering off the ancient stones. The air grows colder with each step, and the sense of foreboding in your chest deepens.")
        print("\nFinally, you emerge into a vast, circular chamber, the walls lined with towering statues and the floor covered in sand and bloodstains. The crowd roars as you are led to the center of the arena, the sound echoing in your ears like thunder.")
        print("\nYou steel yourself for the battle to come, your heart pounding in your chest. The figure who spoke before steps forward once more, their voice ringing out over the crowd.")
        print("\n'Let the battle begin!'")

        # name selection logic.
        # for attempt in range(3):
        #     response = input("\nDo you dare to embrace your destiny? (yes/no): ").lower().strip()
        #     if response == "yes":
        #         print("\nThen let the winds of fate guide you.")
        #         self.set_player_name()
        #         break
        #     elif attempt == 2:
        #         self.shun_player()
        #     else:
        #         print("\nHesitation is but the first step towards defeat. The sands of time wait for no one. Choose wisely, for this is your final chance.")
