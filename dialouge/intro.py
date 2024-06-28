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

    def start_introduction(self):
        armor = self.player_inventory.add_armor("Leather Armor")
        print("In a realm where the scorching fury of embers clashes with the piercing chill of ice, a land stands divided. The ashes of once-great kingdoms lay scattered, whispering tales of heroism and ruin. As the shadows of the past linger and the fate of the world hangs by a thread, a new hero must rise to challenge the encroaching darkness.\n")
        print("Welcome to Endless Ashes of Ember and Ice.\n")
        print("Will you stand against the tide of destruction, braving fire and frost to restore balance to this shattered land? Will you embark on a quest that will test your courage, wits, and willpower to their very limits?\n")

        for attempt in range(3):
            response = input("\nDo you dare to embrace your destiny? (yes/no): ").lower().strip()
            if response == "yes":
                print("\nThen let the winds of fate guide you.")
                self.set_player_name()
                break
            elif attempt == 2:
                self.shun_player()
            else:
                print("\nHesitation is but the first step towards defeat. The sands of time wait for no one. Choose wisely, for this is your final chance.")
