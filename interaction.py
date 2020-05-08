import random
import sys
import ui


characters = {
    "hero": {
        "name": "player",
        "live": 75,
        "attack": 10,
        "chances critical hit": 3,  # podczas atachu tyle razy losujemy, żeby był max atak
        "inventory": [],
        "points": 0,
    },
    "enemy low": {
        "name": "Moherowy beret",
        "live": 25,
        "attack": 2,
        "chances critical hit": 1,
        "inventory": ["laska"],
    },
    "enemy middle low": {
        "name": "moherowy beret z torebka",
        "live": 30,
        "attack": 4,
        "chances critical hit": 2,
        "inventory": ["laska", "torebka"],
    },
    "enemy middle": {
        "name": "gimbaza",
        "live": 50,
        "attack": 10,
        "chances critical hit": 5,
        "inventory": ["glosnik blutuf", "czipsy", "plecak"],
    },
    "enemy middle upper 1": {
        "name": "Biznesmen Janusz",
        "live": 55,
        "attack": 20,
        "chances critical hit": 6,
        "inventory": ["teczka", "wyzwiska"],
    },
    "enemy middle upper 2": {
        "name": "Madka Karyna",
        "live": 55,
        "attack": 20,
        "chances critical hit": 6,
        "inventory": ["wyzwiska", "czipsy", "torebka podróbka"],
    },
    "enemy upper": {
        "name": "Straznik Miejski",
        "live": 55,
        "attack": 70,
        "chances critical hit": 8,
        "inventory": ["mandat", "pączek"],
    },
    "enemy king": {
        "name": "madka z horom curkom",
        "live": 250,
        "attack": 100,
        "chances critical hit": 10,
        "inventory": ["bluzgi", "wyzwiska"],
    },
}


# chwilowo dla bohatera pod zmienną podstawiamy określonego wroga, który traci życie
# podczas walki tak, żeby wiele razy wygrywać z tym samym wrogiem.
def fight(enemy):
    # zwroty przy ataku
    hit_words = ["a masz", "Osz ty koczkodanie złap to", "teraz obroń się przed tym",
                 "trzeba było ze mną nie zaczynać", "osz ty łobuzie, nie uciekniesz mi"]
    # zwroty kiedy obrywam
    offence_words = ["ała", "a to za co", "nie po twarzy", "zaraz ci oddam bambaryło",
                     "tylko na tyle cie stać?", "a to za co", "ajjj.. znowu w klejnoty"]
    check_value = True
    enemy_name = enemy["name"]
    ui.display_fight('Spotykasz na swojej drodze ' + enemy_name + '. Ktoś tu jak zwykle szuka zaczepki...')
    ui.display_fight(input("Czy chcesz tej walki?"))
    ui.display_fight("Nie martw się, " + enemy_name + " nie odpuści i Cię atakuje")
    while check_value:
        hero_random = characters["hero"]["attack"]  # zapisuje max atak bohatera
        enemy_random = enemy["attack"]  # zapisuje max atak wroga
        hero_attack = random.randint(1, hero_random)  # losuje atak bohatera
        enemy_attack = random.randint(1, enemy_random)  # losuje atak wroga
        enemy["live"] = enemy["live"] - hero_attack  # od życia wroga odejmuje atak bohatera
        ui.display_fight(enemy_name + " loses " + hero_attack + " health")
        ui.display_fight(random.choice(hit_words))

        if enemy["live"] < 1:  # jeżeli wróg przegra
            ui.display_fight("Ojoj, " + enemy_name + " już się nie rusza.")
            hero_add = random.randint(1, 7)  # losuję co zdobędzie bohater
            if hero_add < 4:
                ui.display_fight("Brawo, rośnie Ci atak")
                characters["hero"]["attack"] = characters["hero"]["attack"] + 1
            if hero_add > 5:
                ui.display_fight("Brawo, rośnie Ci szansa uderzenia krytycznego")
                characters["hero"]["chances critical hit"] = characters["hero"]["chances critical hit"] + 1
            if hero_add == 4:
                characters["hero"]["chances critical hit"] = characters["hero"]["chances critical hit"] + 1
                characters["hero"]["attack"] = characters["hero"]["attack"] + 1
                ui.display_fight("Brawo, rośnie Ci szansa uderzenia krytycznego i atak")
            if hero_add == 5:
                characters["hero"]["live"] = characters["hero"]["live"] + 5
                ui.display_fight("Brawo, rośnie Ci zdrowie")
            check_value = False
            # wala z bossem
            if enemy_name == "madka z horom curkom":
                win_text = (
                    "Nieźle wymiatasz, Nie jesteś leszczem, a nowym BOSSEM\n" +
                    "Pokonałeś głównego bohatera, Madke z Horom curkom, teraz wygrywasz"
                )
                end_game(win_text)
        # od życia bohatera odejmuje  atak wroga
        characters["hero"]["live"] = characters["hero"]["live"] - enemy_attack
        ui.display_fight("Tracisz ", enemy_attack, " życia.")
        ui.display_fight(random.choice(offence_words))
        if characters["hero"]["live"] < 1:  # jeżeli bohater przegra
            check_value = False
            death_text = (
                '\n\n\n\n\n\Dałeś ciała, przegrałeś z takim leszczem.\n' +
                enemy_name +
                "\nNastępnym razem postaraj się bardziej"
            )
            end_game(death_text)

        inventory_chosen = random.choice(enemy["inventory"])
        # teraz w zależności którą torbę wylosuje, dostanie tyle naklejek na świeżaki/słodziaki
        if inventory_chosen == "laska":
            add_attack = random.randint(5, 10)
            ui.display_fight('podniosłeś laskę, dostajesz dodatkowy atak w ilości ', add_attack)
            characters["hero"]["attack"] = characters["hero"]["attack"] + add_attack
        if inventory_chosen == "glosnik blutuf":
            ui.display_fight(inventory_chosen, ", a na kij mi to?")
        if inventory_chosen == "wyzwiska" or inventory_chosen == "bluzgi" or inventory_chosen == 'mandat':
            ui.display_fight('A to %^$$%*^@# jeden')
            if inventory_chosen == "mandat":
                ui.display_fight("Ten #^%&^* chciał mi wlepić mandat. Dobrze mu tak")
        if inventory_chosen == "czipsy" or inventory_chosen == "pączek":
            add_health = random.randint(10, 40)
            ui.display_fight("O! ", inventory_chosen, "\n Tego mi było trzeba, czuje się ", add_health, " razy lepiej")
            characters["hero"]["live"] = characters["hero"]["live"] + add_health
        if inventory_chosen == "torebka":
            ui.display_fight("O! ", inventory_chosen, "\n co my tu mamy w środku? Napój energetyk?")
            ui.display_fight("Tego mi było trzeba, czuje się 2 razy lepiej")
            characters["hero"]["live"] = characters["hero"]["live"] + 60
            ui.display_fight('Teraz mam już ', characters["hero"]["live"], " życia")
            ui.display_fight("A co tu mi wypadło? \n Naklejki ze świeżakami, aż 5! ")
            characters["hero"]["points"] = characters["hero"]["points"] + 5
        if inventory_chosen == "teczka":
            ui.display_fight("O! ", inventory_chosen, "\n  co my tu mamy w środku? Mała cytrynówka?")
            ui.display_fight("Tego mi było trzeba, czuje się 5 razy lepiej")
            characters["hero"]["live"] = characters["hero"]["live"] + 70
            ui.display_fight('Teraz mam już ', characters["hero"]["live"], " życia")
            ui.display_fight("A co tu mi wypadło? \n Naklejki ze świeżakami, aż 10! ")
            characters["hero"]["points"] = characters["hero"]["points"] + 10
        if inventory_chosen == "torebka podróbka":
            ui.display_fight("O! ", inventory_chosen, "\n  co my tu mamy w środku? Napój energetyk i elemy linki?")
            ui.display_fight("Tego mi było trzeba, czuje się 5 razy lepiej")
            characters["hero"]["live"] = characters["hero"]["live"] + 90
            ui.display_fight('Teraz mam już ', characters["hero"]["live"], " życia")
            ui.display_fight("A co tu mi wypadło? \n Naklejki ze świeżakami, aż 15! ")
            characters["hero"]["points"] = characters["hero"]["points"] + 15
        if inventory_chosen == "plecak":
            ui.display_fight("O! ", inventory_chosen, "\n  co my tu mamy w środku? Skąd gówniaki biorą tyle piwa? Nie ważne.")
            ui.display_fight("Tego mi było trzeba, czuje się 5 razy lepiej")
            characters["hero"]["live"] = characters["hero"]["live"] + 40
            ui.display_fight('Teraz mam już ', characters["hero"]["live"], " życia")
            ui.display_fight("A co tu mi wypadło? \n Naklejki ze świeżakami, całe 5! ")
            characters["hero"]["points"] = characters["hero"]["points"] + 5

        # ustalam, że jak po walce ma ponad 100 pkt, to wygrywa
        if characters["hero"]["points"] > 100:
            win_text = (
                enemy_name, " wygrałeś!\n" +
                "Zebrałeś ponad 100 naklejek na świeżaki"
            )
            end_game(win_text)


def end_game(some_text):
    for second in reversed(range(1, 6)):
        print(f'\n\n\n\n\n\t{some_text}')
        print(f"\n\n\tYour game will end in \033[91m{second}\033[0m")
        sleep(1)
        util.clear_screen()
    sys.exit(0)