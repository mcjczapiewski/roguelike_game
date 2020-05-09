from time import sleep
import util
import engine
import ui
import interaction

PLAYER_ICON = '@'
PLAYER_START_X = 0
PLAYER_START_Y = 0

BOARD_WIDTH = 80
BOARD_HEIGHT = 30

player = {
    "icon": PLAYER_ICON,
    "column_position": PLAYER_START_X,
    "row_position": PLAYER_START_Y,
    "temp_field": "",
}


def main():
    util.clear_screen()
    # player info setup
    name = input('\n\n\n\n\n\tPodaj swoje imię: ')
    interaction.characters["hero"]["name"] = name
    # level 1
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    engine.get_spawn_pos(board, player)
    util.clear_screen()
    for second in reversed(range(1, 2)):
        print(f'\n\n\n\n\n\tWitaj {name}!')
        print(f"\n\n\tYour game will begin in \033[91m{second}\033[0m")
        sleep(1)
        util.clear_screen()
    is_running = True
    while is_running:
        engine.put_player_on_board(board, player)
        ui.display_stats()
        ui.display_board(board)

        key = util.key_pressed()
        if key == 'q':
            exit_game = ''
            while exit_game not in ['Y', 'N']:
                util.clear_screen()
                print('\n\n\n\n\n\tCzy na pewno chcesz wyjsc z gry? Y/N')
                exit_game = util.key_pressed().upper()
                if exit_game == 'Y':
                    is_running = False
        else:
            # movement
            engine.movement(key, player, board)
        util.clear_screen()


if __name__ == '__main__':
    main()
