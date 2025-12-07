"""
A simple text adventure game - Escape from Castle Gloom.
"""

class GameObject:
    """Simple object system for game entities"""
    
    def __init__(self, parent=None, **slots):
        self.parent = parent
        self.slots = slots
    
    def value(self, slot):
        """Get the value of a slot in this object or its parents"""
        if slot in self.slots:
            return self.slots[slot]
        elif self.parent:
            return self.parent.value(slot)
        return None
    
    def update(self, slot, value):
        """Update a slot in this object"""
        self.slots[slot] = value


# Default handlers
def take_anything(obj):
    print("You can't take that.")

def drop_anything(obj):
    print("You can't drop that.")

def unlock_anything(obj):
    print("You can't unlock that.")

def light_anything(obj):
    print("That's not a good idea.")


# World object
world = GameObject(
    playing=False,
    take=take_anything,
    drop=drop_anything,
    light=light_anything,
    unlock=unlock_anything
)


# Player
player = GameObject(
    world,
    location=None,  # Will be set to hall
    last_location=None,
    items=[]
)


# Item class and handlers
def take_item(obj):
    where = player.value('location')
    items_here = where.value('items')
    
    if obj in items_here:
        print(f"You pick up the {obj.value('name')}.")
        items_here.remove(obj)
        player.value('items').append(obj)
    else:
        print(f"There's no {obj.value('name')} here.")

def drop_item(obj):
    where = player.value('location')
    player_items = player.value('items')
    
    if obj in player_items:
        print(f"You drop the {obj.value('name')}.")
        where.value('items').append(obj)
        player_items.remove(obj)
    else:
        print(f"You're not holding any {obj.value('name')}.")


item = GameObject(world, take=take_item, drop=drop_item)


# Items
key = GameObject(item, name="key", description="a rusty key")
matches = GameObject(item, name="matches", description="a box of matches")


def light_candle(obj):
    holding = player.value('items')
    got_matches = matches in holding
    got_candle = obj in holding
    
    if got_candle and obj.value('lit'):
        print("It's already alight.")
    elif got_matches and got_candle:
        print("You light the candle with a match, and it burns brightly.")
        obj.update('lit', True)
    elif got_candle:
        print("What with?")
    else:
        print("You're not holding a candle.")

def drop_candle(obj):
    if obj.value('lit'):
        print("It's not a good idea to drop a burning candle.")
    else:
        drop_item(obj)


candle = GameObject(
    item,
    name="candle",
    description="a candle",
    light=light_candle,
    drop=drop_candle,
    lit=False
)


# Place and exit classes
place = GameObject(world)
exit_obj = GameObject(world, locked=False, move_text="go through the door")


# Places and exits

# Hall
def unlock_door(what):
    locked = what.value('locked')
    got_key = key in player.value('items')
    
    if locked and got_key:
        print("You unlock the door with the rusty key.")
        what.update('locked', False)
    elif locked:
        print("You haven't got anything to unlock it with.")
    else:
        print("It's not locked.")


door = GameObject(
    exit_obj,
    direction="north",
    description="an oak door",
    leads_to=None,  # Will be set to maze1
    locked=True,
    unlock=unlock_door,
    move_text="go through the oak door"
)

hall_east = GameObject(
    exit_obj,
    direction="east",
    description="a small arch",
    leads_to=None  # Will be set to garden
)

hall_west = GameObject(
    exit_obj,
    direction="west",
    description="a staircase",
    leads_to=None,  # Will be set to study
    move_text="go up the staircase"
)

hall_south = GameObject(
    exit_obj,
    direction="south",
    description="a large metal panel",
    leads_to=None,  # Will be set to dungeon
    move_text="you climb through the metal panel which swings shut behind you"
)

hall = GameObject(
    place,
    description="in a large banqueting hall",
    exits=[door, hall_east, hall_west, hall_south],
    items=[]
)


# Study
study_west = GameObject(
    exit_obj,
    direction="west",
    description="a staircase",
    leads_to=hall,
    move_text="go down the staircase"
)

study = GameObject(
    place,
    description="in a small study",
    exits=[study_west],
    items=[candle, matches]
)


# Garden
garden_west = GameObject(
    exit_obj,
    direction="west",
    description="a small arch",
    leads_to=hall
)

garden = GameObject(
    place,
    description="in a small walled garden full of beautiful flowers",
    items=[key],
    exits=[garden_west]
)


# Dungeon
dungeon_north = GameObject(
    exit_obj,
    direction="north",
    description="a metal panel",
    leads_to=hall
)

dungeon = GameObject(
    place,
    description="in a dark dungeon with no windows.\nThe name 'Wes' is scratched on the wall; you wonder what his fate was",
    exits=[dungeon_north],
    dark=True,
    items=[]
)


# Maze
maze = GameObject(place, description="in a maze of twisty little passages, all alike")
maze_exit = GameObject(exit_obj, description="a passage", move_text="go along the passage")

# Maze 1
maze1_north = GameObject(maze_exit, direction="north", leads_to=None)  # leads to maze1
maze1_south = GameObject(maze_exit, direction="south", leads_to=hall)
maze1_east = GameObject(maze_exit, direction="east", leads_to=None)  # leads to maze1
maze1_west = GameObject(maze_exit, direction="west", leads_to=None)  # leads to maze2

maze1 = GameObject(
    maze,
    exits=[maze1_north, maze1_south, maze1_east, maze1_west],
    items=[]
)

# Maze 2
maze2_north = GameObject(maze_exit, direction="north", leads_to=maze1)
maze2_south = GameObject(maze_exit, direction="south", leads_to=None)  # leads to maze2
maze2_east = GameObject(maze_exit, direction="east", leads_to=None)  # leads to maze3
maze2_west = GameObject(maze_exit, direction="west", leads_to=None)  # leads to maze2

maze2 = GameObject(
    maze,
    exits=[maze2_north, maze2_south, maze2_east, maze2_west],
    items=[]
)

# Maze 3
maze3_north = GameObject(maze_exit, direction="north", leads_to=None)  # leads to maze3
maze3_south = GameObject(
    maze_exit,
    direction="south",
    leads_to=None,  # leads to beach
    move_text="go along the passage and through a cave"
)
maze3_east = GameObject(maze_exit, direction="east", leads_to=maze2)
maze3_west = GameObject(maze_exit, direction="west", leads_to=None)  # leads to maze3

maze3 = GameObject(
    maze,
    exits=[maze3_north, maze3_south, maze3_east, maze3_west],
    items=[]
)

# Beach
beach_north = GameObject(
    exit_obj,
    direction="north",
    description="a cave entrance",
    leads_to=maze3
)

beach = GameObject(
    place,
    description="on a beautiful sandy beach next to an azure-blue sea.\nA boat is moored nearby. Well done! You've escaped from Castle Gloom",
    items=[]
)

# Set up circular references
door.update('leads_to', maze1)
hall_east.update('leads_to', garden)
hall_west.update('leads_to', study)
hall_south.update('leads_to', dungeon)

maze1_north.update('leads_to', maze1)
maze1_east.update('leads_to', maze1)
maze1_west.update('leads_to', maze2)

maze2_south.update('leads_to', maze2)
maze2_east.update('leads_to', maze3)
maze2_west.update('leads_to', maze2)

maze3_north.update('leads_to', maze3)
maze3_south.update('leads_to', beach)
maze3_west.update('leads_to', maze3)

# Initialize player location
player.update('location', hall)
player.update('last_location', hall)


# Game objects registry
game_objects = {
    'key': key,
    'matches': matches,
    'candle': candle
}


# Commands
def take(obj):
    handler = obj.value('take')
    if handler:
        handler(obj)

def drop(obj):
    handler = obj.value('drop')
    if handler:
        handler(obj)

def light(obj):
    handler = obj.value('light')
    if handler:
        handler(obj)

def unlock(obj):
    handler = obj.value('unlock')
    if handler:
        handler(obj)


def walk(direction):
    where = player.value('location')
    exits = where.value('exits')
    
    # Find exit by direction
    way = None
    for exit in exits:
        if exit.value('direction') == direction:
            way = exit
            break
    
    if way and way.value('locked'):
        print("You can't - the door seems to be locked.")
    elif way:
        to = way.value('leads_to')
        print(f"You {way.value('move_text')}.")
        player.update('location', to)
        look()
        player.update('last_location', where)
    elif direction == 'back':
        to = player.value('last_location')
        print("You go back.")
        player.update('location', to)
        player.update('last_location', where)
        look()
    else:
        print(f"There is no exit {direction}.")


def look():
    where = player.value('location')
    is_dark = where.value('dark')
    has_lit_candle = candle in player.value('items') and candle.value('lit')
    
    if is_dark and not has_lit_candle:
        print("It's totally dark and you can't see a thing.")
    else:
        print(f"You are {where.value('description')}.")
        
        for exit in where.value('exits'):
            direction = exit.value('direction')
            desc = exit.value('description')
            print(f"To the {direction} is {desc}.")
        
        for item in where.value('items'):
            print(f"There is {item.value('description')} here.")


def inventory():
    items = player.value('items')
    if items:
        item_names = [item.value('description') for item in items]
        print(f"You are holding: {', '.join(item_names)}.")
    else:
        print("You are not holding anything.")


def adventure():
    """Main game loop"""
    if not world.value('playing'):
        print("Escape from Castle Gloom.")
        print("You slowly come to your senses, and then remember what happened.")
        print("You were kidnapped and brought to this castle by an evil ogre,")
        print("who is asleep on a chair nearby, snoring loudly.")
        world.update('playing', True)
    
    look()
    
    while True:
        try:
            line = input(": ").strip()
            print()
            
            if not line:
                continue
            
            parts = line.split(maxsplit=1)
            verb = parts[0].lower()
            noun = parts[1].lower() if len(parts) > 1 else None
            
            # Single-word commands
            if verb in ['look', 'l']:
                look()
            elif verb in ['inventory', 'i', 'inv']:
                inventory()
            elif verb in ['quit', 'q', 'exit']:
                print("Thanks for playing!")
                break
            
            # Two-word commands
            elif verb in ['go', 'g', 'walk']:
                if noun:
                    walk(noun)
                else:
                    print("Go where?")
            
            elif verb in ['take', 'get', 'pick']:
                if noun and noun in game_objects:
                    take(game_objects[noun])
                elif noun:
                    print("I don't understand.")
                else:
                    print("Take what?")
            
            elif verb == 'drop':
                if noun and noun in game_objects:
                    drop(game_objects[noun])
                elif noun:
                    print("I don't understand.")
                else:
                    print("Drop what?")
            
            elif verb == 'light':
                if noun and noun in game_objects:
                    light(game_objects[noun])
                elif noun:
                    print("I don't understand.")
                else:
                    print("Light what?")
            
            elif verb == 'unlock':
                if noun and noun in game_objects:
                    unlock(game_objects[noun])
                elif noun:
                    print("I don't understand.")
                else:
                    print("Unlock what?")
            
            else:
                print("I don't know how to do that.")
        
        except EOFError:
            print("\nThanks for playing!")
            break
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    adventure()