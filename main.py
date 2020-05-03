import util
import engine
import ui
import interaction

PLAYER_ICON = '@'
PLAYER_START_X = 0
PLAYER_START_Y = 0

BOARD_WIDTH = 80
BOARD_HEIGHT = 30


def create_player():
    '''
    Creates a 'player' dictionary for storing all player related informations
     - i.e. player icon, player position.
    Fell free to extend this dictionary!

    Returns:
    dictionary
    '''
    player = {
        "icon": PLAYER_ICON,
        "column_position": PLAYER_START_X,
        "row_position": PLAYER_START_Y,
        "temp_field": "",
    }
    return player


def main():
    player = create_player()
    characters = interaction.characters
    # level 1
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    engine.get_spawn_pos(board, player)

    util.clear_screen()
    is_running = True
    while is_running:
        engine.put_player_on_board(board, player)
        ui.display_board(board)

        key = util.key_pressed()
        if key == 'q':
            is_running = False
        else:
            # movement
            engine.movement(key, player, board)
        util.clear_screen()


if __name__ == '__main__':
    main()
