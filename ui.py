import interaction
import engine
import main


def display_board(board):
    '''
    Displays complete game board on the screen

    Returns:
    Nothing
    '''
    # for row in board:
    #     print("".join(row))

    corners = engine.room_corn()
    monkey = [engine.monkey["row"], engine.monkey["col"]]
    for item in corners:
        if (
            item[0][0] < monkey[0] < item[1][0]
            and item[1][1] < monkey[1] < item[2][1]
        ):
            this_square = item
            break
    i = 0
    for row in board:
        show_row = ""
        if this_square[0][0] <= i <= this_square[1][0]:
            j = 0
            for point in row:
                if this_square[1][1] <= j <= this_square[2][1]:
                    show_row += point
                else:
                    show_row += " "
                j += 1
        print(show_row)
        i += 1


def display_stats():
    stat = interaction.characters['hero']
    print(
        f'Player: {stat["name"]}  ' +
        f'Life: {stat["live"]}  ' +
        f'Attack: {stat["attack"]}  ' +
        f'Crit: {stat["chanses critical hit"]}  ' +
        f'Points: {stat["points"]}\n'
        )


# add opening screen with game info, story line and player setup
# add display dialog box
# add display palyer stats
# add display inventory
