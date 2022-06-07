# this dict has all of the escape codes that color the printed spaces 
graphics_strings = {                       
    "wall": "\x9b100m  ",                   # gray
    "player": "\x9b44m  ",                  # blue
    "friend": "\x9b42m  ",                  # green
    "enemy": "\x9b41m  ",                   # red
    "collectable": "\x9b103m  ",            # yellow
    "door": "\x9b107m  ",                   # white (placeholder, but might stay if no better color is chosen)
    "blank": "\x9b0m  "                     # no color
}

# renders the whole map
def render_map(map):
    print("\033c", end = "")                # clears the console                               
    map_size = map["size"]
    wall_config = map["wall_config"]
    last_item = ""

    for y in range(map_size[1]):            # for every row
        for x in range(map_size[0]):        # for every point in the row
            coords = (x, y)                 # make a coordinate tuple for comparing
            
            # what to print?
            if coords == tuple(map["player"]):                                                  # checks if a player is at these coords, if so, player gets printed
                item = "player"                
            elif coords in map:                                                                 # checks if this coordinate has any defined items, if so, they get printed
                item = map[coords]
            elif 0 in coords or coords[0] == map_size[0]-1 or coords[1] == map_size[1]-1:       # checks if the coordinate is at the edge of the map, is so, wall gets printed
                if coords[0] == 0 and wall_config[0] == True:
                    item = "wall"
                elif coords[1] == 0 and wall_config[1] == True:
                    item = "wall"
                elif coords[0] == map_size[0]-1 and wall_config[2] == True:
                    item = "wall"
                elif coords[1] == map_size[1]-1 and wall_config[3] == True:
                    item = "wall"
                else:
                    item = "blank"
            else:                                                                               # if none of these checks are true, blank gets printed
                item = "blank"

            # the printing
            if item == last_item:                                                               # if the item was already printed, doesn't repeat the escape code
                print("  ", end = "")
            else:
                print(graphics_strings[item], end = "")                                         # else it uses the escape code from graphics_strings
                last_item = item
        print("\x9b0m")                                                                         # after a finished row, a colorless enter gets printed
        last_item = ""                                                                          # and last item is reset because the color also got reset

# overwrites a specific item
def overwrite(x, y, item, return_y = 1):                                                        # the print below is just a long escape code + item + another escape code
    print("\x9b" + str(y + 1) + ";" + str(2*x + 1) + "H" + graphics_strings[item] + "\x9b" + str(return_y) + ";1H", end = "", flush = True)

# camera concept
"""
    for y in range(max(0, map["player"][1] - 5), min(map_size[1], map["player"][1] + 6)):            # for every row
        for x in range(max(0, map["player"][0] - 5), min(map_size[0], map["player"][0] + 6)):        # for every point in the row
            coords = (x, y)                 # make a coordinate tuple for comparing
            
            # what to print?
            if coords == tuple(map["player"]):                                                  # checks if a player is at these coords, if so, player gets printed
                item = "player"                
            elif coords in map:                                                                 # checks if this coordinate has any defined items, if so, they get printed
                item = map[coords]
            elif 0 in coords or coords[0] == map_size[0]-1 or coords[1] == map_size[1]-1:       # checks if the coordinate is at the edge of the map, is so, wall gets printed
                if coords[0] == 0 and wall_config[0]:
                    item = "wall"
                elif coords[1] == 0 and wall_config[1]:
                    item = "wall"
                elif coords[0] == map_size[0]-1 and wall_config[2]:
                    item = "wall"
                elif coords[1] == map_size[1]-1 and wall_config[3]:
                    item = "wall"
                else:
                    item = "blank"
            else:                                                                               # if none of these checks are true, blank gets printed
                item = "blank"

            # the printing
            if item == last_item:                                                               # if the item was already printed, doesn't repeat the escape code
                print("  ", end = "")
            else:
                print(graphics_strings[item], end = "")                                         # else it uses the escape code from graphics_strings
                last_item = item
        print("\x9b0m")                                                                         # after a finished row, a colorless enter gets printed
        last_item = ""                                                                          # and last item is reset because the color also got reset
"""