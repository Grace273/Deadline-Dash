"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from urllib3.util.proxy import connection_requires_http_tunnel

from game_entities import Location, Item, Player
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

import random

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: the ID of the location the game is currently in
        - ongoing: whether the game is still ongoing
        - unlock_location_points: number of points added to player's score when they go to a new location

    Representation Invariants:
        - # TODO add any appropriate representation invariants as needed
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    unlock_location_points: int

    def __init__(self, game_data_file: str, initial_location_id: int, unlock_location_points: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        self._locations, self._items = self._load_game_data(game_data_file)
        self.current_location_id = initial_location_id
        self.unlock_location_points = unlock_location_points
        self.ongoing = True  # whether the game is ongoing

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        items = []
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above
        for item_data in data['items']:  # Go through each element associated with the 'locations' key in the file
            my_item = Item(item_data['name'], item_data['start_position'], item_data['target_position'],
                        item_data['target_points'])
            items.append(my_item)
        item_name_lst = [itm.name for itm in items] #in convenience for initializing items in each location
        print(item_name_lst)

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], (loc_data['brief_description'], loc_data['long_description']),
                                    loc_data['available_commands'], [])
            for item_str in loc_data["items"]: # convert strings of item name into the actual item
                item_index = item_name_lst.index(item_str)
                location_obj.add_item(items[item_index])
            locations[loc_data['id']] = location_obj

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TODO: Complete this method as specified
        if loc_id is not None:
            return self._locations[loc_id]
        else:
            return self._locations[self.current_location_id]

    def play_word_scramble(self) -> None:
        """A word scramble puzzle."""

        f = open("../ex1/common-7-letter-words.txt", "r")
        words = f.read().splitlines()
        word = random.choice(words)
        word_scrambled = "".join(random.sample(word, len(word)))
        player_guess = ""
        hint = 0

        print("Unscramble the word: " + word_scrambled)
        player_guess = input("Enter guess (enter 1 for hint, 0 to give up): ")

        while player_guess != word and player_guess != "0" and hint != len(word):

            if player_guess == "1":
                print("The next letter is: " + word[hint])
                hint += 1
            else:
                print("Try again.")

            player_guess = input("Enter guess (enter 1 for hint, 0 to give up): ")

        if player_guess == "0" or hint == len(word):
            print("Challenge failed... The word was: " + word)
        else:
            print("You Win!")

if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
    def first_event_initializer() -> Event:
        """Initialize the first event."""
        intro = "put introduction here" #TODO: put game background intro and command intro
        first_event = Event(id_num=1, description=intro)
        return first_event

    def undo(log: EventList):
        """Remove the last command """
        # TODO: if command was to do with an item

        log.remove_last_event()
        print(f"Location {log.last.id_num}: {game.get_location(log.last.id_num).name}")
        print(log.last.description)
        print(f"Your inventory: {', '.join([p_item.name for p_item in player.inventory])}")

    player = Player()
    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1, 10)  # load data, setting
    # initial location ID to 1 and unlock_location_points to 10.
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None
    changed_location = True

    #beginning of the game
    game_log.add_event(first_event_initializer())
    print(f"Game Start! \nLocation 1: New College")
    print(game_log.last.description)

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        # TODO: Add completing picking up / depositing an item as an event

        curr_location = game.get_location()

        # Display possible actions at this location
        print("What to do? Choose from: look, hold, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in curr_location.available_commands:
            print("-", action)
        # Display items available for picking up and dropping
        pick_or_drop = []
        for item in curr_location.items:
            choice_name = f"pick up: {item.name}"
            pick_or_drop.append(choice_name)
            print("-", choice_name)
        for item in player.inventory:
            choice_name = f"drop: {item.name}"
            pick_or_drop.append(choice_name)
            print("-", choice_name)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in curr_location.available_commands and choice not in menu and choice not in pick_or_drop:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("You decided to:", choice)
        print("========")

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            if choice == "log":
                game_log.display_events()
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
            elif choice == "look":
                print(curr_location.descriptions[1])
            elif choice == "inventory":
                print(player.inventory_to_string())
            elif choice == "score":
                print(player.score)
            elif choice == "undo":
                undo(game_log)
                game.current_location_id = game_log.last.id_num
                # TODO: handle error for using undo on the first event
            else:  # player choice is "quit"
                # TODO: ask if want to save game, if so, call helper function, else:
                print("Thanks for playing!")
            continue
        else:
            # Handle non-menu actions
            if "pick up" in choice:
                item_name = choice[choice.find(": ") + 2:]
                for i in range(len(curr_location.items)):
                    if curr_location.items[i].name == item_name:
                        player.inventory.append(curr_location.items.pop(i))
                        break
            elif "drop" in choice:
                item_name = choice[choice.find(": ") + 2:]
                for i in range(len(player.inventory)):
                    if player.inventory[i].name == item_name:
                        curr_location.items.append(player.inventory.pop(i))
            else:
                result = curr_location.available_commands[choice]
                game.current_location_id = result

            # TODO: add target points if item is used at target position
            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game

        #TODO: implement pick up and drop item

        # minus the player's moves left by 1
        player.moves_left -= 1

        # create the next event
        next_location = game.get_location()
        event_description = ''

        if next_location != curr_location: # if location changed
            if next_location.visited:
                event_description = next_location.descriptions[0]
            else:
                event_description = next_location.descriptions[1]
                next_location.visited = True
                player.score += game.unlock_location_points
        else:
            event_description = "picked up item or solved puzzle"  #TODO add description for puzzles and items

        new_event = Event(id_num=next_location.id_num, description=event_description)
        game_log.add_event(new_event)

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        print(f"Location {next_location.id_num}: {next_location.name}")
        print(game_log.last.description)
