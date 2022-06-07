from data.graphics import render_map

"""
Map structure
    Each map is a dict named after the map, and in it, it's required to have:
        - "size" - a tuple, which determines the size of the map (width, height)
        - "player_starting_coordinates" - tuple of tuples containing starting coordinates for the player
        - "wall_config" - a tuple of four values, determines, if the (left, top, right, bottom) wall should be rendered, and can teleport the player. For explanation see line 34


    The map has by default walls on the edges and nothing in the middle. This basic configuration is then overwritten by adding terms in this format:
        - (x, y): "entity_name"
    For possible entity names, see graphics.py

    Then, if you want any interactions, you add them separately in this format:
        - ((x, y), "interaction_type"): {interaction_data}

    Interaction types:
    - "interaction"
        - Data: "interaction_name"
        - executes an interaction from the interaction() function

    - "monologue"
        - Data: "dialog_strings_name"
        - plainly says smth from dialog_strings

    - "teleport"
        - Data: ["map_name", "position_index"]
        - loads a map of the name, with a player on the position determined by the index (choosen from the "player_string_coordinates" list)

    "wall_config" explanation:
        Values:
            - True - normal wall
            - ("map_name", coord_shift) - loads the map depending on the name. Then, the coordinates are choosen like this:
                - depending on the direction, one coordinate is choosen to get the player opposite the wall (ie, if you go left, it makes x = map_lenght[0] etc.)
                - the other coordinate = current coordinate (the same one) + coord_shift
"""

world = {
    "village": {
        "size": (25, 15),
        "player_starting_coords": ((23, 7), (4, 4), (8, 7), (9, 11), (12, 6)),
        "wall_config": (True, True, True, True),

        (3, 3): "wall",
        (3, 5): "wall",
        (2, 4): "wall",
        (3, 4): "door",
        ((3, 4), "teleport"): ("house_1", 0),

        (7, 6): "wall",
        (7, 8): "wall",
        (6, 7): "wall",
        (7, 7): "door",
        ((7, 7), "teleport"): ("house_2", 0),

        (8, 10): "wall",
        (8, 12): "wall",
        (7, 11): "wall",
        (8, 11): "door",
        ((8, 11), "teleport"): ("starting_house", 1),

        (11, 5): "wall",
        (11, 7): "wall",
        (10, 6): "wall",
        (11, 6): "door",
        ((11, 6), "teleport"): ("house_with_key", 0),
        (12, 6): "enemy",
        ((12, 6), "interaction"): "wolf_fight",

        (14, 8): "friend",
        ((14, 8), "interaction"): "villager_wolf_attack",

        (23, 6): "wall",
        (23, 8): "wall",
        (22, 6): "friend",
        ((22, 6), "interaction"): "gatekeeper",
        (24, 7): "door",
        ((24, 7), "interaction"): "gate",
        ((24, 7), "teleport"): ("village_path", 0),

        (3, 1): "collectable",
        ((3, 1), "interaction"): "collect_weapon"
    },

    "house_1": {
        "size": (6, 6),
        "player_starting_coords": ((4, 4),),
        "wall_config": (True, True, ("house_2", 1), True),

        (1, 1): "collectable",
        ((1, 1), "interaction"): "collect_coins",
        (5, 4): "door",
        ((5, 4), "teleport"): ("village", 1)
    },

    "house_2": {
        "size": (6, 6),
        "player_starting_coords": ((4, 4),),
        "wall_config": (("house_1", 0), True, True, True),

        (1, 1): "friend",
        ((1, 1), "monologue"): "old_friend_village",
        (5, 4): "door",
        ((5, 4), "teleport"): ("village", 2)
    },

    "starting_house": {
        "size": (6, 6),
        "player_starting_coords": ((1, 1), (4, 4)),
        "wall_config": (True, True, True, True),

        (4, 1): "collectable",
        ((4, 1), "interaction"): "collect_coins",
        (4, 4): "friend",
        ((4, 4), "interaction"): "Vorin_first_meet",
        (5, 4): "door",
        ((5, 4), "teleport"): ("village", 3)
    },

    "house_with_key": {
        "size": (6, 6),
        "player_starting_coords": ((4, 4), (5, 5)),
        "wall_config": (True, True, True, True),

        (1, 1): "collectable",
        ((1, 1), "interaction"): "gate_key_collect",
        (5, 4): "door",
        ((5, 4), "teleport"): ("village", 4)
    },

    "village_path": {
        "size": (30, 7),
        "player_starting_coords": ((1, 3),),
        "wall_config": (True, True, ("crossroad", 1), True),

        (0, 3): "door",
        ((0, 3), "teleport"): ("village", 0),

        (3, 2): "friend",
        ((3, 2), "interaction"): "vorin_gangdalf_explanation",
        (3, 4): "friend",
        ((3, 4), "interaction"): "vorin_gangdalf_explanation",


        # test
        (7, 5): "enemy",
        ((7, 5), "interaction"): "gum",
        (10, 5): "friend",
        ((10, 5), "interaction"): "elolnd_first_meet",
        (15, 5): "enemy",
        ((15, 5), "interaction"): "elven_king_first_meet",
        (19, 5): "wall",
        (21, 5): "wall",
        (20, 5): "blank",
        ((20, 5), "interaction"): "dragon_sneak"
    },

    "crossroad": {
        "size": (9, 9),
        "wall_config": (("village_path", -1), ("coming_soon", -1), True, ("forest_path_vertical", -1)),

        (0, 0): "wall",
        (0, 1): "wall",
        (1, 0): "wall",

        (0, 7): "wall",
        (0, 8): "wall",
        (1, 8): "wall",

        (7, 0): "wall",
        (7, 8): "wall",

        (4, 3): "friend",
        ((4, 3), "interaction"): "vorin_gangdalf_crossroad",
        (7, 4): "friend",
        ((7, 4), "monologue"): "crossroad_sign",
        (4, 5): "friend",
        ((4, 5), "interaction"): "vorin_gangdalf_crossroad",
    },

    "forest_path_vertical": {
        "size": (7, 15),
        "wall_config": (True, ("crossroad", 1), True, ("forest_path_turn", 0)),
    },
    "forest_path_turn": {
        "size": (7, 7),
        "wall_config": (True, ("forest_path_vertical", 0), ("forest_path_horizontal", 0), True),

        (6, 0): "wall"
    },
    "forest_path_horizontal": {
        "size": (15, 7),
        "wall_config": (("forest_path_turn", 0), True, ("forest", -1), True),

        (14, 1): "wall",
        (14, 5): "wall",
    },

    "forest": {
        "size": (20, 15),
        "player_starting_coords": ((1, 12),),
        "wall_config": (("forest_path_horizontal", 1), True, ("elolnd_path_horizontal", 1), True),
        
    },

    "elolnd_path_horizontal": {
        "size": (15, 7),
        "wall_config": (("forest", -1), True, ("", 0), True),

        (0, 1): "wall",
        (0, 5): "wall",
    },

    "elolnd_garden": {
        "size": (20, 15),
        "player_starting_coords": ((13, 5),),
        "wall_config": (("coming_soon", 0), True, ("coming_soon", 0), True),

        (9, 9): "wall",
        (9, 10): "wall",
        (11, 9): "wall",
        (11, 10): "wall",

        (14, 5): "door",
        ((14, 5), "teleport"): ("elolnd_house", 0),
        (10, 10): "friend",
        ((10, 10), "interaction"): "elolnd_first_meet",
    },

    "elolnd_house": {
        "size": (8, 8),
        "player_starting_coords": ((1, 6),),
        "wall_config": (True, True, True, True),

        (4, 2): "friend",
        ((4, 2), "interaction"): "elolnd_dialog_inside",
        (0, 6): "door",
        ((0, 6), "teleport"): ("elolnd_garden", 0),
    },

    "mountains": {
        "size": (20, 15),
        "player_starting_coords": ((7, 6), (4, 3)),
        "wall_config": (("coming_soon", 0), True, ("coming_soon", 0), ("coming_soon", 0)),

        (4, 1): "wall",
        (5, 1): "wall",
        (6, 1): "wall",
        (5, 2): "wall",
        (6, 2): "wall",
        (5, 3): "wall",
        (5, 4): "wall",
        (4, 5): "wall",
        (8, 5): "wall",
        (4, 6): "wall",
        (9, 6): "wall",
        (5, 8): "wall",
        (6, 8): "wall",
        (7, 8): "wall",
        (8, 8): "wall",
        (9, 8): "wall",
        (5, 7): "wall",
        (3, 4): "wall",
        (3, 5): "wall",
        (9, 7): "wall",
        (8, 7): "wall",
        (8, 3): "wall",
        (9, 3): "wall",
        (10, 3): "wall",
        (11, 3): "wall",
        (10, 2): "wall",
        (11, 2): "wall",
        (12, 3): "wall",
        (13, 4): "wall",
        (6, 10): "wall",
        (6, 9): "wall",
        (7, 9): "wall",
        (7, 9): "wall",
        (6, 10): "wall",
        (13, 5): "wall",
        (12, 13): "wall",
        (13, 13): "wall",
        (13, 12): "wall",
        (11, 12): "wall",
        (10, 13): "wall",
        (11, 13): "wall",
        (12, 12): "wall",
        (12, 11): "wall",
        (13, 10): "wall",
        (14, 10): "wall",
        (14, 9): "wall",
        (14, 8): "wall",
        (14, 7): "wall",
        (15, 6): "wall",
        (14, 6): "wall",
        (13, 5): "wall",
        (13, 4): "wall",
        (16, 6): "wall",
        (17, 5): "wall",
        (18, 5): "wall",
        (19, 4): "wall",
        (18, 6): "wall",
        (18, 7): "wall",
        (17, 6): "wall",
        (13, 14): "wall",
        (13, 11): "wall",
        (15, 7): "wall",
        (15, 8): "wall",
        (10, 4): "wall",
        (5, 12): "wall",
        (4, 11): "wall",
        (4, 12): "wall",

        # small patches near edges
        (15, 1): "wall",
        (16, 1): "wall",

        (1, 7): "wall",
        (1, 8): "wall",

        (4, 13): "wall",
        (5, 13): "wall",
        (6, 13): "wall",

        (18, 12): "wall",
        (18, 13): "wall",
        (18, 14): "wall",

        # the rest
        (12, 8): "enemy",
        (10, 9): "enemy",
        (11, 6): "enemy",

        (12, 1): "enemy",
        ((12, 1), "interaction"): "coming_coon",
        
        # (9, 5): "blank",                         # oh no, enemies i won't go there they could capture me
        # ((9, 5), "monologue"): "coming_soon",
        # (6, 11): "blank",
        # ((6, 11), "monologue"): "coming_soon",

        (4, 4): "door",
        ((4, 4), "teleport"): ("coming_coon", 0),
        (8, 6): "door",
        ((8, 6), "teleport"): ("coming_coon", 0)
    }
}
"""
    "louka": { #text něco jako napadli vás skřeti schovej se do jeskyně
        "size": (9, 9),
        "player_starting_coords": ((1, 1), (1, 2)),
        (3, 3): "wall",
        (3, 5): "wall",
        (2, 4): "wall",
        (3, 4): "door",
        ((3, 4), "teleport"): ("jeskyne1", 0)
        
    },

    "jeskyne1": {
        "size": (8, 8),
        "player_starting_coords": ((1, 1), (1, 2)),
        (1, 2): "collectable", #meč žihadlo
        (6, 6): "door",
        ((6, 6), "teleport"): ("jeskyne2", 0)
    },

    "jeskyne2": {
        "size": (8, 8),
        "player_starting_coords": ((1, 1), (1, 2)),
        (6, 5): "friend", #glum
        (4, 4): "collectable", #prsten
        (6, 6): "door",
        ((6, 6), "teleport"): ("hvozd", 0),
        
    },

     "hvozd": { #úkol zabít pavouky a zachránit ostatní
        "size": (10, 10),
        "player_starting_coords": ((1, 1), (1, 2)),
        (2, 3): "friend",
        (4, 3): "friend",
        (6, 3): "friend",
        (2, 4): "enemy", #pavouk1
        (4, 4): "enemy", #pavouk2
        (6, 4): "enemy", #pavouk3
        (8, 8): "door",
        ((8, 8), "teleport"): ("hora1", 0),
    },

    "hora1": { #před horou
        "size": (13, 13),
        "player_starting_coords": ((1, 1), (1, 2)),
        (6, 4): "wall",
        (7, 4): "wall",
        (4, 5): "wall",
        (8, 5): "wall",
        (4, 6): "wall",
        (9, 6): "wall",
        (3, 7): "wall",
        (10, 7): "wall",
        (4, 8): "wall",
        (5, 8): "wall",
        (6, 8): "wall",
        (7, 8): "wall",
        (8, 8): "wall",
        (9, 8): "wall",
        (5, 4): "door",
        ((5, 4), "teleport"): ("hora2", 0)
    },

    "hora2": { #úkol zabít draka
        "size": (9, 9),
        "player_starting_coords": ((1, 1), (1, 2)),
        (4, 4): "enemy", #drak
    },
}
"""

# adds long stretches of walls
for i in range(4, 14):
    world["forest"][(0, i)] = "wall"
    world["forest"][(19, i)] = "wall"


for i in range(1, 11):
    world["elolnd_garden"][(0, i)] = "wall"
    world["elolnd_garden"][(19, i)] = "wall"
for i in list(range(9)) + list(range(12, 19)):
    world["elolnd_garden"][(i, 10)] = "wall"
for i in range(1, 5):
    world["elolnd_garden"][(14, i)] = "wall"
for i in range(14, 19):
    world["elolnd_garden"][(i, 6)] = "wall"
for i in range(11, 14):
    world["elolnd_garden"][(7, i)] = "blank"

for i in range(1, 11):
    world["mountains"][(0, i)] = "wall"
for i in range(4, 15):
    world["mountains"][(19, i)] = "wall"
for i in range(15):
    world["mountains"][(i, 14)] = "wall"

def transform_world(name):
    if name == "elolnd":
        for i in range(11, 14):
            del world["elolnd_garden"][(7, i)]

# loads a map from world
def load_map(name, position_index = 0):         
    map = world[name]                                                       # chooses the map from world depending on the name
    map["player"] = list(map["player_starting_coords"][position_index])     # overwrites the player coordinates to be on the right spot
    render_map(map)                                                         # map is then rendered
    return map                                                              # and returned
