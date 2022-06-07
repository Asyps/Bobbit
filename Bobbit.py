from msvcrt import getch

import data.Andrews_magic
from data.maps import world, load_map
from data.graphics import render_map, overwrite
from data.interactions import *


PlaySound("./data/music/title-theme.wav", SND_FILENAME | SND_LOOP | SND_ASYNC)
fancy_print("\033cBobbit\n\n\n\n\n\nStiskněte cokoliv pro počátek hry ")
getch()
fancy_print("Kdysi dávno...")
sleep(dialog_pace * 3)

PlaySound("./data/music/main-theme.wav", SND_FILENAME | SND_LOOP | SND_ASYNC)

# current_map = "starting_house"
# map = load_map("starting_house", 0)
current_map = "starting_house"
map = load_map(current_map, 0)

# movement and interactions
while True:
    inp = getch()

    if world_flags["ring_mode_on"]:
        player_stats["mhp"] -= 1

    if player_stats["mhp"] < 1:
        interaction("gone_crazy")

    if inp == b'i':
        if world_flags["ring_mode_on"]:
            player_stats["mhp"] += 1
        interaction("view_inventory")
        render_map(map)
        continue

    elif inp == b'r':
        if world_flags["has_ring"]:
            world_flags["ring_mode_on"] = not world_flags["ring_mode_on"]
            player_stats["mhp"] += 1
        continue

    elif inp == b'w':
        a, b = 1, -1          
    elif inp == b'a':
        a, b = 0, -1
    elif inp == b's':
        a, b = 1, 1
    elif inp == b'd':
        a, b = 0, 1
    
    else:
        if world_flags["ring_mode_on"]:
            player_stats["mhp"] += 1
        continue

    # move or interact
    wall_config = map["wall_config"]
    map_size = map["size"]
    coords = (map["player"][0] + (b if a == 0 else 0), map["player"][1] + (b if a == 1 else 0))
    if coords not in map:
        current_coords = map["player"]
        if coords[0] == 0:
            if map["wall_config"][0] != True:
                load_data = map["wall_config"][0]
                current_map = load_data[0]
                map = world[load_data[0]]
                map["player"] = [map["size"][0] - 2, current_coords[1] + load_data[1]]
                render_map(map)
        elif coords[1] == 0:
            if map["wall_config"][1] != True:
                load_data = map["wall_config"][1]
                current_map = load_data[0]
                map = world[load_data[0]]
                map["player"] = [current_coords[0] + load_data[1], map["size"][1] - 2]
                render_map(map)
        elif coords[0] == map_size[0]-1:
            if map["wall_config"][2] != True:
                load_data = map["wall_config"][2]
                current_map = load_data[0]
                map = world[load_data[0]]
                map["player"] = [1, current_coords[1] + load_data[1]]
                render_map(map)
        elif coords[1] == map_size[1]-1:
            if map["wall_config"][3] != True:
                load_data = map["wall_config"][3]
                current_map = load_data[0]
                map = world[load_data[0]]
                map["player"] = [current_coords[0] + load_data[1], 1]
                render_map(map)
        else:
            overwrite(*map["player"], "blank", map["size"][1] + 1)
            map["player"][a] += b
            overwrite(*map["player"], "player", map["size"][1] + 1)


    elif (coords, "interaction") in map:
        current_check = (coords, "interaction")
        deletion_option = interaction(map[current_check])           
        if deletion_option == 1 or deletion_option == 2:
            del map[current_check]
        if deletion_option == 2:
            del map[coords]
        
        render_map(map)

    elif (coords, "monologue") in map:
        say(map[(coords, "monologue")])
        render_map(map)
  
    elif (coords, "teleport") in map:
        current_check = (coords, "teleport")
        world[current_map] = map
        current_map = map[current_check][0]
        map = load_map(*map[current_check])
