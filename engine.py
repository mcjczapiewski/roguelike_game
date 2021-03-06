import random
import interaction
import ui
import main


# characters used on the map
floor_ch = ","
wall_ch = "#"
path_ch = "."
door_ch = "+"
enemy_list = ["M", "T", "G", "J", "K", "S", "H"]
friend_list = ["F"]
level_corr_list = ["1", "2", "3"]
key_choice = ["w", "s", "a", "d"]
column_next = [0, 0, -1, 1]
row_next = [-1, 1, 0, 0]

room_corners = []
mobs_on_board = []
friends_on_board = []
monkey = {"row": 0, "col": 0}


def create_board(width, height):
    """
    Creates a new game board based on input parameters.

    Args:
    int: The width of the board
    int: The height of the board

    Returns:
    list: Game board
    """
    # create list of lists where:
    # width == sublist length, height == number of sublists
    board = [[" " for x in range(0, width - 2)] for y in range(0, height - 2)]
    # put some rooms on the board, max h/w is half of board h/w
    for room_num in range(0, random.randint(4, 6)):
        room_gen(board)
    # make fake corridor connections
    for fake_num in range(0, 2):
        fake_gen(board)
    # make paths
    path_gen(board, False)
    # make doors
    door_gen(board)
    # return board
    return board


def put_player_on_board(board, player):
    """
    Modifies the game board by placing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    """
    # set temp to what is in the filed before player stands there
    player["temp_field"] = board[player["row_position"]][
        player["column_position"]
    ]
    # put player in the position
    board[player["row_position"]][player["column_position"]] = player["icon"]
    monkey["row"] = player["row_position"]
    monkey["col"] = player["column_position"]


def movement(key, player, board):
    """ moves the player position, if movement is allowed """
    # retrieve the original value of the field
    board[player["row_position"]][player["column_position"]] = player[
        "temp_field"
    ]
    # movement
    walkable = [door_ch, floor_ch, path_ch]
    for option in key_choice:
        if key == option:
            # next position
            check_col = (
                player["column_position"]
                + column_next[key_choice.index(option)]
            )
            check_row = (
                player["row_position"] + row_next[key_choice.index(option)]
            )
            # validate if after the move, player still on board
            if check_col not in range(0, len(board[0])):
                return
            elif check_row not in range(0, len(board)):
                return
            # validate if the fight will happen
            elif board[check_row][check_col] in enemy_list:
                # initiate fight
                for dict_key, dict_value in interaction.characters.items():
                    if (
                        dict_value["print_character"]
                        == board[check_row][check_col]
                    ):
                        enemy_dict = interaction.characters[dict_key]
                        enemy_position = [check_row, check_col]
                        interaction.fight(
                            enemy_dict, mobs_on_board, enemy_position, board
                        )
                # exit movement function
                return
            # Meets the friend
            elif board[check_row][check_col] in friend_list:
                friend_position = [check_row, check_col]
                interaction.friend_meet(
                    friends_on_board, friend_position, board
                )
                return
            # validate if corridor to another level
            elif board[check_row][check_col] in level_corr_list:
                return board[check_row][check_col]
            # validate if walkable field
            elif board[check_row][check_col] not in walkable:
                return
            # move player to the next locations
            player["column_position"] += column_next[key_choice.index(option)]
            player["row_position"] += row_next[key_choice.index(option)]
            return


def room_gen(board):
    """ generates empty room on the board """
    # set room parameters
    try:
        r_height = random.randint(5, len(board) / 2)
        r_width = random.randint(5, len(board[0]) / 2)
    except RecursionError:
        r_height = 5
        r_width = 5
    # step 1: select random place on the board to start
    row_pointer = random.randint(1, len(board) - r_height - 1)
    col_pointer = random.randint(1, len(board[0]) - r_width - 1)
    # step 2: scan if making room is possible, one empty space around room
    can_build = True
    for room_row in range(row_pointer - 1, row_pointer + r_height + 1):
        for room_col in range(col_pointer - 1, col_pointer + r_width + 1):
            if (
                board[room_row][room_col] == wall_ch
                or board[room_row][room_col] == floor_ch
            ):
                can_build = False
    # step 3: draw a room
    if can_build:
        for room_row in range(row_pointer, row_pointer + r_height):
            for room_col in range(col_pointer, col_pointer + r_width):
                board[room_row][room_col] = wall_ch
        corridor_connector_list = []
        for room_row in range(row_pointer + 1, row_pointer + r_height - 1):
            for room_col in range(col_pointer + 1, col_pointer + r_width - 1):
                board[room_row][room_col] = floor_ch
                temp = (room_row, room_col)
                if temp[0] % 2 == 0 and temp[1] % 2 == 0:
                    corridor_connector_list.append(temp)
        # corners of the room
        room_corners.append(
            [
                [row_pointer, col_pointer],
                [row_pointer + r_height - 1, col_pointer],
                [row_pointer, col_pointer + r_width - 1],
                [row_pointer + r_height - 1, col_pointer + r_width - 1],
            ]
        )
        # set corridor connector
        corridor_connector = random.choice(corridor_connector_list)
        board[corridor_connector[0]][corridor_connector[1]] = "C"
    else:
        room_gen(board)


def check_pos_around(board, curr_pos):
    """
    curr_pos: tuple (row, col)
    returns list of fields around a given field
    """
    search_list = []
    for row in range(curr_pos[0] - 1, curr_pos[0] + 2):
        for col in range(curr_pos[1] - 1, curr_pos[1] + 2):
            search_list.append(board[row][col])
    return search_list


def door_gen(board):
    """ make doors where possible """
    for door_candidate in list_of_pos(board, wall_ch):
        checklist = check_pos_around(board, door_candidate)
        if checklist.count(path_ch) == 1 and path_ch in [
            checklist[index] for index in [1, 3, 5, 7]
        ]:
            if [checklist[index] for index in [1, 7]].count(wall_ch) == 2 or [
                checklist[index] for index in [3, 5]
            ].count(wall_ch) == 2:
                board[door_candidate[0]][door_candidate[1]] = door_ch


def path_gen(board, random_match=True):
    """ mark walls where making door is possible """
    # make list of positions of corridor connectors
    corridor_connector_list = list_of_pos(board, "C") + list_of_pos(
        board, path_ch
    )
    # link connectors randomly
    while len(corridor_connector_list) > 1:
        if random_match:
            pointer = random.choice(corridor_connector_list)
            corridor_connector_list.remove(pointer)
            next_pointer = random.choice(corridor_connector_list)
        else:
            pointer = corridor_connector_list[0]
            corridor_connector_list.remove(pointer)
            next_pointer = corridor_connector_list[0]
        # make list of path positions
        path_list = []
        row_range = range(
            min(pointer[0], next_pointer[0]),
            max(pointer[0], next_pointer[0]) + 1,
        )
        col_range = range(
            min(pointer[1], next_pointer[1]),
            max(pointer[1], next_pointer[1]) + 1,
        )
        for path_row in row_range:
            for path_col in col_range:
                if path_row in [
                    min(row_range),
                    max(row_range),
                ] or path_col in [min(col_range), max(col_range)]:
                    temp = (path_row, path_col)
                    path_list.append(temp)
        # change empty positions to path
        for path_row, path_col in path_list:
            if board[path_row][path_col] == " ":
                board[path_row][path_col] = path_ch
        # move pointer
        pointer = next_pointer
    # clear connectors
    for c_row, c_col in list_of_pos(board, "C"):
        board[c_row][c_col] = floor_ch


def fake_gen(board):
    # make list of positions of empty fields
    empty_pos_list = list_of_pos(board, " ")
    # select random positions to make fake corridors
    fake_connection = random.choice(empty_pos_list)
    # check if row and col numbers are even
    if fake_connection[0] % 2 == 0 and fake_connection[1] % 2 == 0:
        board[fake_connection[0]][fake_connection[1]] = path_ch
    else:
        fake_gen(board)


def list_of_pos(board, criteria):
    """ make list of positions of criteria on board """
    pos_list = []
    for row in range(0, len(board)):
        for column in range(0, len(board[0])):
            if board[row][column] == criteria:
                temp = (row, column)
                pos_list.append(temp)
    return pos_list


def get_spawn_pos(board, player):
    """
    get position of player spawn on the map
    return: tuple with (row, col) of spawn position
    """
    new_pos = random.choice(list_of_pos(board, floor_ch))
    player["column_position"] = new_pos[1]
    player["row_position"] = new_pos[0]


def put_enemies_on_board(board, enemies, level_change="1"):
    """
    put 3 enemies on level 1
    put 3 enemies on level 2
    put boss on level 3
    """
    random.shuffle(room_corners)
    lvl_1_mobs = enemies[0:2]
    lvl_2_mobs = enemies[3:5]
    lvl_3_boss = enemies[6]
    for room in room_corners:
        x_range = abs(room[0][0] - room[1][0] - 2)
        y_range = abs(room[1][1] - room[2][1] - 2)
        room_size = x_range * y_range
        if room_size > 300:
            possible_mobs = 3
        elif 100 < room_size <= 300:
            possible_mobs = 2
        else:
            possible_mobs = 1
        for number in range(possible_mobs):
            board_mark = ""
            if level_change == "1":
                enemy = random.choice(lvl_1_mobs)
            elif level_change == "2":
                enemy = random.choice(lvl_2_mobs)
            elif level_change == "3":
                enemy = random.choice(lvl_3_boss)
            while board_mark != ",":
                mob_x = random.randint(room[0][0] + 1, room[1][0] - 1)
                mob_y = random.randint(room[1][1] + 1, room[2][1] - 1)
                if board[mob_x][mob_y] == ",":
                    board_mark = ","
                    board[mob_x][mob_y] = enemy
                    mobs_on_board.append([mob_x, mob_y])


def put_friends_on_board(board, friends):
    """
    put friends on board
    """
    possible_friends_number = random.randint(1, len(room_corners) - 1)
    number_of_friends = 0
    rooms_with_friends = []
    while number_of_friends < possible_friends_number:
        new_room = random.choice(room_corners)
        if new_room not in rooms_with_friends:
            rooms_with_friends.append(new_room)
            number_of_friends += 1
    for room in rooms_with_friends:
        friend = random.choice(friends)
        board_mark = ""
        while board_mark != ",":
            friend_x = random.randint(room[0][0] + 1, room[1][0] - 1)
            friend_y = random.randint(room[1][1] + 1, room[2][1] - 1)
            if board[friend_x][friend_y] == ",":
                board_mark = ","
                board[friend_x][friend_y] = friend
                friends_on_board.append([friend_x, friend_y])


def mobs_movement(board, mobs, player):
    player_xy = [player["row_position"], player["column_position"]]
    for mob in mobs:
        mob_mark = board[mob[0]][mob[1]]
        mobs.remove(mob)
        possible_move = []
        row_col = [[0, -1], [0, 1], [1, 0], [-1, 0], [0, 0]]
        for coordinate in row_col:
            possible_move.append(
                [mob[0] + coordinate[0], mob[1] + coordinate[1]]
            )
        board_mark = ""
        while board_mark != ",":
            new_position = random.choice(possible_move)
            if (
                board[new_position[0]][new_position[1]] in [",", mob_mark]
                and new_position != player_xy
                and new_position not in mobs
            ):
                board_mark = ","
                board[mob[0]][mob[1]] = ","
                board[new_position[0]][new_position[1]] = mob_mark
                mobs.append(new_position)
            else:
                possible_move.remove(new_position)


def levels_generator(next_level):
    if next_level == "2":
        if interaction.characters["hero"]["points"] < 5:
            return False
    if next_level == "3":
        if interaction.characters["hero"]["points"] < 15:
            return False
    ui.player_was_here = [
        [0 for x in range(0, main.BOARD_WIDTH - 2)]
        for y in range(0, main.BOARD_HEIGHT - 2)
    ]
    room_corners.clear()
    mobs_on_board.clear()
    friends_on_board.clear()
    monkey["row"] = 0
    monkey["col"] = 0
    return next_level


def next_level_pass(board, player, level_change="1"):
    random.shuffle(room_corners)
    player_xy = [player["row_position"], player["column_position"]]
    for room in room_corners:
        if (
            room[0][0] <= player_xy[0] <= room[1][0]
            and room[1][1] <= player_xy[1] <= room[2][1]
        ):
            continue
        if level_change == "1":
            mark_x = random.randint(room[0][0] + 1, room[1][0] - 1)
            mark_y = random.randint(room[1][1] + 1, room[2][1] - 1)
            board[mark_x][mark_y] = "2"
            return
        elif level_change == "2":
            mark_x = random.randint(room[0][0] + 1, room[1][0] - 1)
            mark_y = random.randint(room[1][1] + 1, room[2][1] - 1)
            board[mark_x][mark_y] = "3"
            return
