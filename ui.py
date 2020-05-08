import interaction
import engine
import main
import util


player_was_here = [
    [0 for x in range(0, main.BOARD_WIDTH - 2)]
    for y in range(0, main.BOARD_HEIGHT - 2)
]


def display_board(board, was_here=player_was_here):
    """
    Displays complete game board on the screen

    Returns:
    Nothing
    """
    corners = engine.room_corners
    monkey = [engine.monkey["row"], engine.monkey["col"]]
    FAKE_NUMBER = 100
    this_rectangle = [[FAKE_NUMBER, FAKE_NUMBER], [FAKE_NUMBER, FAKE_NUMBER]]
    for item in corners:
        if (
            item[0][0] <= monkey[0] <= item[1][0]
            and item[1][1] <= monkey[1] <= item[2][1]
        ):
            this_rectangle = item
            break
    row_counter = 0
    current_row = monkey[0]
    current_col = monkey[1]
    for row in board:
        show_row = ""
        if this_rectangle[0][0] <= row_counter <= this_rectangle[1][0]:
            col_counter = 0
            for mark in row:
                if this_rectangle[1][1] <= col_counter <= this_rectangle[2][1]:
                    show_row += mark
                    player_was_here[row_counter][col_counter] = 1
                elif player_was_here[row_counter][col_counter] == 1:
                    show_row += mark
                else:
                    show_row += " "
                col_counter += 1
        elif (
            monkey[0] == row_counter
            or current_row - 2 < row_counter < current_row + 2
        ):
            col_counter = 0
            for mark in row:
                if (
                    current_col - 2 < col_counter < current_col + 2
                    and monkey[1] == col_counter
                    and monkey[0] == row_counter
                ):
                    show_row += mark
                    player_was_here[row_counter][col_counter] = 1
                elif (
                    player_was_here[row_counter][col_counter] == 1
                    or current_col - 2 < col_counter < current_col + 2
                ):
                    show_row += mark
                else:
                    show_row += " "
                col_counter += 1
        else:
            col_counter = 0
            for mark in row:
                if player_was_here[row_counter][col_counter] == 1:
                    show_row += mark
                else:
                    show_row += " "
                col_counter += 1
        print(show_row)
        row_counter += 1


def display_stats():
    stat = interaction.characters["hero"]
    print(
        f'Gracz: {stat["name"]}  '
        + f'Zdrowie: {stat["live"]}  '
        + f'Atak: {stat["attack"]}  '
        + f'Moc: {stat["chances critical hit"]}  '
        + f'Punkty: {stat["points"]}\n'
    )


def display_stats_fight(stat):
    print(
        f'\t{stat["name"]}\n'
        + f'\tZnacznik: {stat["print_character"]}\t'
        + f'Zdrowie: {stat["live"]}\t'
        + f'Atak: {stat["attack"]}\t'
        + f'Moc: {stat["chances critical hit"]}\n'
    )


def display_fight(fight_text, enemy):
    util.clear_screen()
    print("\n\n\tKONFRONTACJA\n")
    display_stats_fight(interaction.characters['hero'])
    display_stats_fight(enemy)
    print(f'\t~ {fight_text}')
    print(
        '\n\tOpcje' +
        '\n\t[1] Wciśnij Q aby przerwac konfrontacje' +
        '\n\t[2] Wciśnij I aby użyć posiadanych przedmiotów' +
        '\n\t[3] Wciśnij dowolny klawisz aby kontynuować'
    )
    key = util.key_pressed().lower()
    if key == 'q':
        return False
    else:
        return True


# add opening screen with game info, story line and player setup
# add display dialog box
# add display palyer stats
# add display inventory
