import random

name = input('Podaj swoje imię')


print(name)
characters = {
    "hero": {
        "name": name,
        "live": 75,
        "attack": 10,
        "chanses critical hit": 3, # podczas atachu tyle razy losujemy, żeby był max atak
        "inventory": []
        "points": 0
    },
    "enemy low": {
        "name": "Moherowy beret",
        "live": 25,
        "attack": 2,
        "chanses critical hit": 1,
        "inventory": ["laska"],
    },
    "enemy middle low": {
        "name": "moherowy beret z torebka",
        "live": 30,
        "attack": 4,
        "chanses critical hit": 2,
        "inventory": ["laska", "trebka"],
    },
    "enemy middle": {
        "name": "gimbaza",
        "live": 50,
        "attack": 10,
        "chanses critical hit": 5,
        "inventory": ["glosnik blutuf", "czipsy", "plecak"],
    },
    "enemy middle upper": {
        "name": "Biznesmen Janusz",
        "live": 55,
        "attack": 20,
        "chanses critical hit": 6,
        "inventory": ["teczka", "wyzwiska"],
    "enemy middle upper": {
        "name": "Madka Karyna",
        "live": 55,
        "attack": 20,
        "chanses critical hit": 6,
        "inventory": ["wyzwiska", "czipsy", "torebka podróbka"],
    "enemy upper": {
        "name": "Straznik Miejski",
        "live": 55,
        "attack": 70,
        "chanses critical hit": 8,
        "inventory": ["mandat", "pączek"],
    },
    "enemy king": {
        "name": "madka z horom curom",
        "live": 250,
        "attack": 100,
        "chanses critical hit": 10,
        "inventory": ["bluzgi", "wyzwiska"],
    },
}

# chwilowo dla bohatera pod zmienną podstawiamy określonego wroga, który traci życie 
# podczas walki tak, żeby wiele razy wygrywać z tym samym wrogiem.
def fight(enemy):
    hit_words = ["a masz", "Osz ty koczkdanie złap to", "teraz obroń się przed tym", 
            "trzeba było ze mną nie zaczynać", "osz ty łobuzie, nie uciekniesz mi"] 
            # zwroty przy ataku
    offence_words = ["ała", "a to za co", "nie po twarzy", "zaraz ci oddam bambaryło", 
                "tylko na tyle cie sztać?", "a to za co", "ajjj.. znowu w klejnoty"] 
                # zwroty kiedy obrywam
    check_value = True
    enemy_name = enemy["name"]   
    print('Spotykasz na swojej drodze ', enemy_name, '. Ktoś tu jak zwykle szuka zaczepki,')
    input_tag = input("Czy chcesz tej walki?")
    print("Nie martw się, ", enemy_name, " nie odpuści i Cię atakuje")
    while check_value:
        hero_random = characters["hero"["attack"]] # zapisuje max atak bohatera
        enemy_random = enemy["attack"] #zapisuje max atak wroga
        hero_attack = random.randint(1, hero_random) # losuje atak bohatera
        enemy_attack = random.randint(1, enemy_attack) # losuje atak wroga     
        enemy["live"] = enemy["live"] - hero_attack # od życia wroga odejmuje atak bohatera
        print(enemy_name, " loose ", hero_attack, " lives")
        print(random.choice(hit_words))

        if enemy[["live"]] < 1: # jeżeli wróg przegra
            print("Ojoj, ", enemy_name, " już się nie rusza.")
            check_value = False
            hero_add = random.randint(1, 7) # losuję co zdobędzie bohater
            if hero_add < 4:
                print("Brawo, rośnie Ci atak")
                characters["hero"["attack"]] = characters["hero"["attack"]] + 1
            if hero_add > 5:
                print("Brawo, rośnie Ci szansa uderzenia krytycznego")
                characters["hero"["chanses critical hit"]] = characters["hero"["chanses critical hit"]] + 1
            if hero_add == 4:
                characters["hero"["chanses critical hit"]] = characters["hero"["chanses critical hit"]] + 1
                characters["hero"["attack"]] = characters["hero"["attack"]] + 1
                print("Brawo, rośnie Ci szansa uderzenia krytycznego i atak")
            if hero_add == 5:
                characters["hero"["live"]] = characters["hero"["live"]] + 5
                print("Brawo, rośnie Ci zdrowie")
            break
            check_value = False
        characters["hero"["live"]] = characters["hero"["live"]] - enemy_attack # od życia bhatera odejmuje  atak wroga
        print("Tracisz ", enemy_attack, " życia.")
        print(random.choice(offence_words))
        if characters["hero"["live"]] < 1: # jeżeli bohater przegra
            check_value = False
            print('Dałeś ciała, przegrałeś z takim leszczem.')
            print(enemy_name)
            print("Następnym razem postaraj się bardziej")

        #inventory_long = len(enemy['inventory']) # ilość w inventarzu  wroga
        #inventory_long = inventory_long - 1
        #inventory_position = random.randit(0, inventory_long)
        #inventory_chosen = enemy["inventory"][inventory_position] # podniesiony artefakt
        inventory_chosen = random.choice(enemy["inventory"])
        # teraz w zależności którą torbę wylosuje, doatanie tyle naklejek na świeżaki/słodziaki
        if inventory_chosen == "laska":
            add_attack = random.randint(5, 10)
            print('podniosłeś laskę, dostajesz dodatkowy atak w ilości ', add_attack)
            characters["hero"["attack"]] = characters["hero"["attack"]] + add_attack
        if inventory_chosen == "glosnik blutuf":
            print(inventory_chosen, ", a na kij mi to?")
        if inventory_chosen == "wyzwiska" or inventory_chosen == "bluzgi" or inventory_chosen == 'mandat':
            print('A to %^$$%*^@# jeden')
            if inventory_chosen == "mandat":
                print("Ten #^%&^* chciał mi wlepić mandat. Dobrze mu tak")
        if inventory_chosen == "czipsy" or inventory_chosen == "pączek":
            add_heatlh = random.randint(10, 40)
            print("O! ", inventory_chosen, "\n Tego mi było trzeba, czuje się ", add_heatlh, " razy lepiej")
            characters["hero"["live"]] = characters["hero"["live"]] + add_heatlh
        if inventory_chosen = "trebka":
            print("O! ", inventory_chosen, "\n co my tu mamy w środku? Napój energetyk? \n Tego mi było trzeba, czuje się 2 razy lepiej")
            characters["hero"["live"]] = characters["hero"["live"]] + 60
            print('Teraz mam już ' characters["hero"["live"]], " życia")
            print("A co tu mi wypadło? \n Naklejki ze świeżakami, aż 5! ")
            characters["hero"["points"]] = characters["hero"["points"]] + 5
        if inventory_chosen = "teczka":
            print("O! ", inventory_chosen, "\n  co my tu mamy w środku? Mała cytrynówka? \n Tego mi było trzeba, czuje się 5 razy lepiej")
            characters["hero"["live"]] = characters["hero"["live"]] + 70
            print('Teraz mam już ' characters["hero"["live"]], " życia")
            print("A co tu mi wypadło? \n Naklejki ze świeżakami, aż 10! ")
            characters["hero"["points"]] = characters["hero"["points"]] + 10
        if inventory_chosen = "torebka podróbka":
            print("O! ", inventory_chosen, "\n  co my tu mamy w środku? Napój energetyk i elemy linki? \n Tego mi było trzeba, czuje się 5 razy lepiej")
            characters["hero"["live"]] = characters["hero"["live"]] + 90
            print('Teraz mam już ' characters["hero"["live"]], " życia")
            print("A co tu mi wypadło? \n Naklejki ze świeżakami, aż 15! ")
            characters["hero"["points"]] = characters["hero"["points"]] + 15
        if inventory_chosen = "plecak":
            print("O! ", inventory_chosen, "\n  co my tu mamy w środku? Skąd gówniaki biorą tyle piwa? Nie ważne. \n Tego mi było trzeba, czuje się 5 razy lepiej")
            characters["hero"["live"]] = characters["hero"["live"]] + 40
            print('Teraz mam już ' characters["hero"["live"]], " życia")
            print("A co tu mi wypadło? \n Naklejki ze świeżakami, całe 5! ")
            characters["hero"["points"]] = characters["hero"["points"]] + 5
        