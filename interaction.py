import random
import sys
import ui
import util
from time import sleep


characters = {
    "hero": {
        "name": "player",
        "live": 75,
        "attack": 10,
        "chances critical hit": 3,  # podczas ataku tyle razy losujemy, żeby był max atak
        "inventory": [],
        "points": 0,
        "print_character": '@',
    },
    "enemy low": {
        "name": "Moherowy beret",
        "live": 25,
        "attack": 2,
        "chances critical hit": 1,
        "inventory": ["laska"],
        "print_character": 'M',  # change to M after testing
        "column_position": "",
        "row_position": "",
        "temp_field": "",
    },
    "enemy middle low": {
        "name": "moherowy beret z torebka",
        "live": 30,
        "attack": 4,
        "chances critical hit": 2,
        "inventory": ["laska", "torebka"],
        "print_character": 'T',
        "column_position": "",
        "row_position": "",
        "temp_field": "",
    },
    "enemy middle": {
        "name": "gimbaza",
        "live": 50,
        "attack": 10,
        "chances critical hit": 5,
        "inventory": ["glosnik blutuf", "czipsy", "plecak"],
        "print_character": 'G',
        "column_position": "",
        "row_position": "",
        "temp_field": "",
    },
    "enemy middle upper 1": {
        "name": "Biznesmen Janusz",
        "live": 55,
        "attack": 20,
        "chances critical hit": 6,
        "inventory": ["teczka", "wyzwiska"],
        "print_character": 'J',
        "column_position": "",
        "row_position": "",
        "temp_field": "",
    },
    "enemy middle upper 2": {
        "name": "Madka Karyna",
        "live": 55,
        "attack": 20,
        "chances critical hit": 6,
        "inventory": ["wyzwiska", "czipsy", "torebka podróbka"],
        "print_character": 'K',
        "column_position": "",
        "row_position": "",
        "temp_field": "",
    },
    "enemy upper": {
        "name": "Straznik Miejski",
        "live": 55,
        "attack": 70,
        "chances critical hit": 8,
        "inventory": ["mandat", "pączek"],
        "print_character": 'S',
        "column_position": "",
        "row_position": "",
        "temp_field": "",
    },
    "enemy king": {
        "name": "madka z horom curkom",
        "live": 250,
        "attack": 100,
        "chances critical hit": 10,
        "inventory": ["bluzgi", "wyzwiska"],
        "print_character": 'H',
        "column_position": "",  # list
        "row_position": "",  # list
        "temp_field": "",
    },
}


# chwilowo dla bohatera pod zmienną podstawiamy określonego wroga, który traci życie
# podczas walki tak, żeby wiele razy wygrywać z tym samym wrogiem.
def fight(enemy):
    ''' initiates fight with the enemy
    enemy: dictionary with enemy characteristics (taken from the characters dict)
    '''
    # zwroty przy ataku
    hit_words = ["a masz", "osz ty koczkodanie złap to", "teraz obroń się przed tym",
                 "trzeba było ze mną nie zaczynać", "osz ty łobuzie, nie uciekniesz mi"]
    # zwroty kiedy obrywam
    offence_words = ["ała", "a to za co", "nie po twarzy", "zaraz ci oddam bambaryło",
                     "tylko na tyle cie stać?", "a to za co", "ajjj.. znowu w klejnoty"]
    enemy_name = enemy["name"]
    # fight setup
    check_value = ui.display_fight('Ktoś tu jak zwykle szuka zaczepki...' + 
                                   '\n\t  Spotykasz na swojej drodze >> ' + enemy_name + ' << Co robisz?', enemy, quit_possible=True)
    fight_won = False
    while check_value:
        # proceed with the fight
        hero_random = characters["hero"]["attack"]  # zapisuje max atak bohatera
        enemy_random = enemy["attack"]  # zapisuje max atak wroga
        hero_attack = random.randint(1, hero_random)  # losuje atak bohatera
        enemy_attack = random.randint(1, enemy_random)  # losuje atak wroga
        # od życia wroga odejmuje atak bohatera
        enemy["live"] = enemy["live"] - hero_attack  
        ui.display_fight(random.choice(hit_words) + "\n\t" + enemy_name + " traci " + str(hero_attack) + " zdrowia", enemy)

        if enemy["live"] < 1:  # jeżeli wróg przegra
            outcome = ''
            hero_add = random.randint(1, 7)  # losuję co zdobędzie bohater
            if hero_add < 4:
                outcome = "Brawo, rośnie Ci atak"
                characters["hero"]["attack"] = characters["hero"]["attack"] + 1
            if hero_add > 5:
                outcome = "Brawo, rośnie Ci szansa uderzenia krytycznego"
                characters["hero"]["chances critical hit"] = characters["hero"]["chances critical hit"] + 1
            if hero_add == 4:
                outcome = "Brawo, rośnie Ci szansa uderzenia krytycznego i atak"
                characters["hero"]["chances critical hit"] = characters["hero"]["chances critical hit"] + 1
                characters["hero"]["attack"] = characters["hero"]["attack"] + 1
            if hero_add == 5:
                outcome = "Brawo, rośnie Ci zdrowie"
                characters["hero"]["live"] = characters["hero"]["live"] + 5
            # kończe walke
            ui.display_fight("Ojoj, " + enemy_name + " już się nie rusza.\n\t" + outcome, enemy)
            check_value = False
            fight_won = True
            # walka z bossem
            if enemy_name == "madka z horom curkom":
                win_text = (
                    "Nieźle wymiatasz, Nie jesteś leszczem, a nowym BOSSEM\n" +
                    "Pokonałeś głównego bohatera, Madke z Horom curkom, teraz wygrywasz"
                )
                end_game(win_text)
        # od życia bohatera odejmuje  atak wroga
        characters["hero"]["live"] = characters["hero"]["live"] - enemy_attack
        check_value = ui.display_fight(random.choice(offence_words) + 
                                       "\n\t" + "Tracisz " + str(enemy_attack) + 
                                       " zdrowia.", enemy, quit_possible=True)

        if characters["hero"]["live"] < 1:  # jeżeli bohater przegra
            check_value = False
            death_text = (
                '\n\n\n\n\n\tDałeś ciała, przegrałeś z takim leszczem.\n' +
                enemy_name +
                "\n\tNastępnym razem postaraj się bardziej"
            )
            end_game(death_text)

    if fight_won:
        inventory_chosen = random.choice(enemy["inventory"])
        # teraz w zależności którą torbę wylosuje, dostanie tyle naklejek na świeżaki/słodziaki
        if inventory_chosen == "laska":
            add_attack = random.randint(5, 10)
            ui.display_fight('podniosłeś laskę, dostajesz dodatkowy atak w ilości ' + str(add_attack), enemy)
            characters["hero"]["attack"] = characters["hero"]["attack"] + add_attack
        if inventory_chosen == "glosnik blutuf":
            ui.display_fight(inventory_chosen + ", a na kij mi to?", enemy)
        if inventory_chosen == "wyzwiska" or inventory_chosen == "bluzgi" or inventory_chosen == 'mandat':
            ui.display_fight('A to %^$$%*^@# jeden', enemy)
            if inventory_chosen == "mandat":
                ui.display_fight("Ten #^%&^* chciał mi wlepić mandat. Dobrze mu tak", enemy)
        if inventory_chosen == "czipsy" or inventory_chosen == "pączek":
            add_health = random.randint(10, 40)
            ui.display_fight("O! " + inventory_chosen + " Tego mi było trzeba, czuje się " + str(add_health) + " razy lepiej", enemy)
            characters["hero"]["live"] = characters["hero"]["live"] + add_health
        if inventory_chosen == "torebka":
            ui.display_fight("O! " + inventory_chosen + " Co my tu mamy w środku? Napój energetyk?" + 
                            "\n\t  Tego mi było trzeba, czuje się 2 razy lepiej", enemy)
            characters["hero"]["live"] = characters["hero"]["live"] + 60
            ui.display_fight('Teraz mam już ' + str(characters["hero"]["live"]) + " zdrowia" +
                            "\n\t  A co tu mi wypadło? Naklejki ze świeżakami, aż 5! ", enemy)
            characters["hero"]["points"] = characters["hero"]["points"] + 5
        if inventory_chosen == "teczka":
            ui.display_fight("O! " + inventory_chosen + " Co my tu mamy w środku? Mała cytrynówka?" + 
                            "\n\t  Tego mi było trzeba, czuje się 5 razy lepiej", enemy)
            characters["hero"]["live"] = characters["hero"]["live"] + 70
            ui.display_fight('Teraz mam już ' + str(characters["hero"]["live"]) + " zdrowia" +
                            "\n\t  A co tu mi wypadło? Naklejki ze świeżakami, aż 10! ", enemy)
            characters["hero"]["points"] = characters["hero"]["points"] + 10
        if inventory_chosen == "torebka podróbka":
            ui.display_fight("O! " + inventory_chosen + " Co my tu mamy w środku? Napój energetyk i elemy linki?" + 
                            "\n\t  Tego mi było trzeba, czuje się 5 razy lepiej", enemy)
            characters["hero"]["live"] = characters["hero"]["live"] + 90
            ui.display_fight('Teraz mam już ' + str(characters["hero"]["live"]) + " zdrowia" + 
                            "\n\t  A co tu mi wypadło? Naklejki ze świeżakami, aż 15! ", enemy)
            characters["hero"]["points"] = characters["hero"]["points"] + 15
        if inventory_chosen == "plecak":
            ui.display_fight("O! " + inventory_chosen + " Co my tu mamy w środku? Skąd gówniaki biorą tyle piwa? Nie ważne." + 
                            "\n\t  Tego mi było trzeba, czuje się 5 razy lepiej", enemy)
            characters["hero"]["live"] = characters["hero"]["live"] + 40
            ui.display_fight('Teraz mam już ' + str(characters["hero"]["live"]) + " zdrowia" + 
                            "\n\t  A co tu mi wypadło? Naklejki ze świeżakami, całe 5! ", enemy)
            characters["hero"]["points"] = characters["hero"]["points"] + 5

    # ustalam, że jak po walce ma ponad 100 pkt, to wygrywa
    if characters["hero"]["points"] > 100:
        win_text = (
            '\n\n\n\n\n\t' +
            enemy_name +
            " wygrałeś!\n" +
            "Zebrałeś ponad 100 naklejek na świeżaki"
        )
        end_game(win_text)


def end_game(some_text):
    for second in reversed(range(1, 6)):
        print(some_text)
        print(f"\n\n\tYour game will end in \033[91m{second}\033[0m")
        sleep(1)
        util.clear_screen()
    sys.exit(0)
