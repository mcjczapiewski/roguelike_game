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

first_line = "\n\n\n\n\n\t"


def open_text(txt, s=6, countdown_screen=False):
    if countdown_screen is False:
        print(txt)
        # wciśnięcie klawisza zamiast sleep, żeby można było przejść szybciej dalej
        print("\n\n\nWciśnij dowolny klawisz, aby kontynuować...")
        key = util.key_pressed()
        util.clear_screen()
    if countdown_screen is True:
        for second in reversed(range(1, 6)):
            print(f"{first_line}Uważaj, grę zaczniesz za: \033[91m{second}\033[0m")
            sleep(1)
            util.clear_screen()


def main():
    util.clear_screen()
    # player info setup
    name = input(f'{first_line}Podaj swoje imię: ')
    interaction.characters["hero"]["name"] = name
    util.clear_screen()
    text = f'{first_line}Witaj przybyszu!\n\tSłyszałem, że zwą Cię {name}.\
\n\n\tDzisiaj Twój chrześniak ma urodziny. Gówniak musi, MUSI dostać świeżaka.\
\n\tRozpieszczony smarkacz...'
    open_text(text)
    text = f'{first_line}Jak ja nie lubię szczeniaka, ale jak mus to mus, w końcu chrześniak.'
    open_text(text)
    text = f'{first_line}Niestety, we wszystkich sklepach z rozjechanym robakiem już nie mają naklejek.\
\n\tZostaje Ci zebrać w inny sposób te wszystkie naklejki.\
\n\n\tRuszaj do boju, bo bez tego wstrętnego świeżaka nie uda Ci się wbić na imprezę.\
\n\tW końcu 8. urodziny to nie przelewki!'
    open_text(text, 20)
    text = f'{first_line}Przygotuj się na ciężkie boje, bo te wszystkie moherowe berety,\
\n\tJanusze oraz cała gimbaza nie dadzą Ci ich za darmo.\
\n\n\tAle najbardziej musisz uważać na strażników miejskich (cholerne pasożyty, nawet piwa nie można się napić) i Madki.\
\n\tZ nimi to już nie przelewki.\
\n\n\tNa szczęście pracownicy biedronki są zawsze po Twojej stronie, w końcu kończyli razem z Tobą studia.'
    open_text(text, 20)
    text = f'{first_line}A więc ruszaj do boju, bo PICCOLO i 0,5l wody gazowanej już się dla Ciebie chłodzą!'
    open_text(text, 5)
    open_text("", 5, True)

    # level 1
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    engine.get_spawn_pos(board, player)
    util.clear_screen()

    engine.put_friends_on_board(board, engine.friend_list)
    engine.put_enemies_on_board(board, engine.enemy_list)
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
                print(f'{first_line}Czy na pewno chcesz wyjść z gry? Y/N')
                exit_game = util.key_pressed().upper()
                if exit_game == 'Y':
                    is_running = False
        else:
            # movement
            level_change = engine.movement(key, player, board)
            if level_change:
                board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
                engine.get_spawn_pos(board, player)
        util.clear_screen()
        engine.mobs_movement(board, engine.mobs_on_board, player)
        engine.mobs_movement(board, engine.friends_on_board, player)


if __name__ == '__main__':
    main()
