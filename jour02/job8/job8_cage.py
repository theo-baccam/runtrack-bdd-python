import mysql.connector

from . import job8_connect as conn


# FONCTIONS POUR CAGES
def create_cage(superficie, capacite):
    if not isinstance(superficie, int):
        print("La superficie doit être un integer")
        return
    elif not isinstance(capacite, int):
        print("La capacité doit être un integer")
        return

    laplateforme = conn.connect()
    
    cursor = laplateforme.cursor()

    cursor.execute("SELECT id FROM cage")
    cages = cursor.fetchall()

    # Pour reset l'auto-incrémentation, pour empêcher skips
    if len(cages) == 0:
        increment_start = 1
    else:
        id_list = []
        for cage in cages:
            id_list.append(cages[0][0])
        increment_start = max(id_list) + 1
    cursor.execute(f"ALTER TABLE cage AUTO_INCREMENT = {increment_start}")
    laplateforme.commit()

    cursor.execute(
        f"INSERT INTO cage (superficie, capacite) "
        f"VALUES ({superficie}, {capacite})"
    )
    laplateforme.commit()
    cursor.close()

    laplateforme.close()


def get_animal_in_cage(id_cage):
    if not isinstance(id_cage, int):
        print("L'ID de la cage doit être un integer")
    laplateforme = conn.connect()

    cursor = laplateforme.cursor()
    cursor.execute("SELECT id_cage, nom, race FROM animal")
    animals = cursor.fetchall()
    animal_in_cage = []
    for animal in animals:
        if animal[0] == id_cage:
            animal_dict = {
                "id_cage": animal[0],
                "nom": animal[1],
                "race": animal[2]
            }
            animal_in_cage.append(animal_dict)
    cursor.close()

    laplateforme.close()
    return animal_in_cage


def read_cages():
    laplateforme = conn.connect()

    cursor = laplateforme.cursor()
    cursor.execute("SELECT * FROM cage")
    cages = cursor.fetchall()
    for cage in cages:
        output = (
            f"CAGE N°{cage[0]}:\n"
            f" - Superficie: {cage[1]}\n"
            f" - Capacité: {cage[2]}\n"
            f" - Animaux:\n"
        )
        for animal in get_animal_in_cage(cage[0]):
            output += f"   - {animal["nom"]} ({animal["race"]})"
        print(output)
    cursor.close()

    laplateforme.close()


def get_total_area():
    laplateforme = conn.connect()

    cursor = laplateforme.cursor()
    cursor.execute("SELECT superficie from cage")
    superficies = cursor.fetchall()
    area_list = []
    for superficie in superficies:
        area_list.append(superficie[0])
    total = sum(area_list)
    print(f"La superficie totale des cages est {total}m2")
    cursor.close()

    laplateforme.close()


def update_cage(cage_id, value_name, new_value):
    if not isinstance(cage_id, int):
        print("L'identifiant de lage doit être un integer")
        return
    elif not isinstance(value_name, str):
        print("Le nom de la valeur à modifer doit être un string")
        return
    elif not isinstance(new_value, int):
        print("La nouvelle valeur doit être un integer")
    
    laplateforme = conn.connect()

    cursor = laplateforme.cursor()
    cursor.execute(f"UPDATE cage SET {value_name} = {new_value} WHERE id = {cage_id}")
    laplateforme.commit()
    cursor.close()

    laplateforme.close()


def delete_cage(cage_id):
    if not isinstance(cage_id, int):
        print("L'identifiant de cage doit être un integer")
        return
    
    laplateforme = conn.connect()

    cursor = laplateforme.cursor()
    cursor.execute(f"DELETE FROM cage WHERE id = {cage_id}")
    laplateforme.commit()
    cursor.close()

    laplateforme.close()


# FONCTIONS DE "MENUS" POUR CAGES
def create_cage_menu():
    while True:
        superficie = input("Quelle est la superficie?\n")
        if not superficie.isdigit():
            print("La superficie doit être un entier")
            continue
        superficie = int(superficie)
        break

    while True:
        capacite = input("Quelle est la capacité maximale?\n")
        if not capacite.isdigit():
            print("La capacité doit être un entier")
            continue
        capacite = int(capacite)
        break

    choice = input(
        f"Souhaitez-vous bien créer une cage de "
        f"{superficie}m2, avec une capacité de {capacite}?\n"
        f"[O]ui ou [N]on?\n"
    )
    if choice == "O":
        create_cage(superficie, capacite)
    elif choice == "N":
        return
    else:
        print("Choix invalide")


def update_cage_menu():
    options = {
        "1": "superficie",
        "2": "capacite"
    }

    while True:
        cage_id = input(
            "Quelle est l'ID de la cage?\n"
        )
        if not cage_id.isdigit():
            print("Choix invalide")
            continue
        cage_id = int(cage_id)
        break

    while True:
        choice = input(
            "Quelle attribut voulez vous changer?\n"
            "1) La superficie\n"
            "2) La capacité maximale\n"
        )
        if choice in options:
            break
        else:
            print("Choix invalide")

    while True:
        new_value = input("Quelle est la nouvelle valeur?\n")
        if not new_value.isdigit():
            print("Choix invalide")
            return
        new_value = int(new_value)
        break

    while True:
        confirmation = input(
            f"Etes vous sûr?\n"
            f"[O]ui ou [N]on?\n"
        )
        if confirmation == "O":
            update_cage(cage_id, options[choice], new_value)
            break
        elif confirmation == "N":
            break
        else:
            print("Choix invalide")


def delete_cage_menu():
    while True:
        cage_id = input("Quel est l'ID de la cage que vous souhaitez supprimer?\n")
        if not cage_id.isdigit():
            print("Choix invalide")
            continue
        cage_id = int(cage_id)
        break 

    while True:
        confirmation = input(
            "Êtes-vous sûr?\n"
            "[O]ui ou [N]on?"
        )
        if confirmation == "O":
            delete_cage(cage_id)
            break
        elif confirmation == "N":
            break
        else:
            print("Choix invalide")


def cages_menu():
    options = {
        "1": create_cage_menu,
        "2": read_cages,
        "3": get_total_area,
        "4": update_cage_menu,
        "5": delete_cage_menu,
    }

    while True:
        choice = input(
            "Que souhaitez vous faire?\n"
            "1) Ajouter une nouvelle cage\n"
            "2) Afficher les cages\n"
            "3) Afficher la superficie totale des cages\n"
            "4) Mettre à jour les infos d'une cage\n"
            "5) Supprimer une cage\n"
            "6) Je veux revenir en arrière\n"
        )
        if choice == "6":
            break
        elif choice in options:
            options[choice]()
        else:
            print("Choix invalide")