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

def clear_screen(s):
    for second in reversed(range(1, s)):
        print(f'\n\n\n\n\n\tWitaj {name}!')
        print(f"\n\n\tYour game will begin in \033[91m{second}\033[0m")
        sleep(1)
        util.clear_screen()
        
def open_text(txt, s=6, check=True):
    if check == True:
        print(txt)
        sleep(s)
        util.clear_screen()
    if check == False:
        for second in reversed(range(1, 6)):
            if check == False:
                print(f"\n\n\tUważaj, grę zaczniesz za: \033[91m{second}\033[0m")
                sleep(1)
            util.clear_screen()

def main():
    util.clear_screen()
    # player info setup
    name = input('\n\n\n\n\n\tPodaj swoje imię: ')
    interaction.characters["hero"]["name"] = name
    util.clear_screen()
    text = 'Witaj przybyszu. \n Słyszałem, że zwą Cie '+  name + '\n\n Dzisiaj Twój chrzesniak ma urdziny. Gówniak musi, MUSI dostać świeżaka. \n Rozpieszczony smarkacz.'
    open_text(text)
    text = 'Jak ja nie lubie szczeniaka, ale jak mus to mus, w końcu chrześniak'
    open_text(text)
    text = 'Niestety we wszystkich sklepach z rozjechanym robakiem już nie mają naklejek. Zostaje Ci zebrać w inny sposób te wszystkie naklejki \n\n\n Ruszaj do boju, bo bez tego wstrętnego świeżaka nie uda Ci się wbić na impreże. W końcu 8. urodziny to nie przelewki'
    open_text(text, 20)
    text = 'przygotuj się na ciężkie boje, bo te wszystkie moherowe berety, Janusze oraz cała gimbaza nie dadzą Ci ich za darmo, \n\n Ale najbardziej musisz uważać na strażników miejskich (cholerne pasożyty, nawet piwa nie mozna się napić) i Madki.\n Z nimi to już nie przelewki \n\n Na szczęście pracownicy biedronki są zawsze po Twojej stronie, w końcu kończyli razem z Tobą studia'
    open_text(text, 20)
    text = 'A więc ruszaj do boju, bo PICCOLO i 0,5l wody gazowanej już się dla Ciebie chłodzą'
    open_text(text, 5)
    text = ''
    open_text(text, 5, False)
 
    # level 1
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    engine.get_spawn_pos(board, player)
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
            level_change = engine.movement(key, player, board)
            if level_change:
                board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
                engine.get_spawn_pos(board, player)
        util.clear_screen()


if __name__ == '__main__':
    main()
