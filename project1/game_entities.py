"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name of the item
        - position: current position of the item
        - enabled: whether the item is still useful
        - start_position: the starting position/location of the item
        - target_position: the target position/location of the item
        - target_points: the points earned when depositing item at target position

    Representation Invariants:
        - self.position, self.start_position and self.target_position are valid location ids.
        - self.target_points > 0
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    position: int
    description: str
    enabled: bool
    start_position: int
    target_position: Optional[int]
    target_points: int

    def __init__(self, name: str, description: str, start_position: int, target_position: Optional[int], target_points: int) -> None:
        """Initialize a new item.

        # TODO Add more details here about the initialization if needed
        """

        self.name = name
        self.position = start_position
        self.description = description
        self.start_position = start_position
        self.target_position = target_position
        self.target_points = target_points
        self.enabled = True


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: integer id for this location
        - descriptions: tuple for location descriptions of this location
                        first value is a brief description and whose second value is a long description
        - available_commands: a mapping of available commands at this location to
                              the location executing that command would lead to
        - items: a list of available items at this location
        - visited: whether the player has visited this location (for displaying description)

    Representation Invariants:
        - self.descriptions != tuple()
        - self.available_commands != {}
        - values in self.available_commands are valid location ids.
    """

    id_num: int
    name: str
    descriptions: tuple[str, str]
    available_commands: dict[str, int]
    items: list[Item]
    visited: bool

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    def __init__(self, location_id: int, name: str, descriptions: tuple[str, str],
                 available_commands: dict[str, int], items: list[Item]) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        self.id_num = location_id
        self.name = name
        self.descriptions = descriptions
        self.available_commands = available_commands
        self.items = items
        self.visited = False

    def add_item(self, item: Item) -> None:
        """Add a new item to self.items"""

        self.items.append(item)

    def remove_item(self, item: Item) -> None:
        """Remove given item from self's items attributes.

        Preconditions:
        - item in self.items
        """

        for i in range(len(self.items)):
            if self.items[i].name == item.name:
                self.items.pop(i)

# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

@dataclass
class Player:
    """A player in the text adventure game world.

    Instance Attributes:
        - inventory: the player's inventory
        - score: score of the player
        - moves_left: number of moves the player has left


    Representation Invariants:
        - self.score >= 0
        - self.moves_left >= 0
        - self.item_on_hand in self.inventory
    """

    inventory: list[Item]
    score: int
    moves_left: int
    item_on_hand: Optional[Item] = None

    def __init__(self) -> None:
        """Initialize a new player. The player starts with an empty inventory, score and 50 moves. """

        self.inventory = []
        self.score = 0
        self.item_on_hand = None

        # TODO: decide the number of moves
        self.moves_left = 50

    def inventory_to_string(self) -> str:
        """List all items in inventory in a readable format"""

        str_inventory = "Your inventory: "
        if not self.inventory:
            str_inventory += "empty"
        else:
            str_inventory += ", ".join(item.name for item in self.inventory)

        return str_inventory


if __name__ == "__main__":
    # pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
