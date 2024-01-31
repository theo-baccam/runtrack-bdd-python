from datetime import datetime

import mysql.connector

from . import job8_connect as conn

# FONCTIONS POUR ANIMAUX
def valid_date(input_string):
    if len(input_string) != 10:
        return False
    try:
        datetime.strptime(input_string, "%Y-%m-%d")
        return True
    except:
        return False


def create_animal(nom, race, id_cage, date_naissance, pays_origine):
    if not isinstance(nom, str):
        raise ValueError("Le nom doit être un string")
    elif not isinstance(race, str):
        raise ValueError("La race doit être un string")
    elif not isinstance(id_cage, int):
        raise ValueError("Le numéro de la cage doit être un integer")
    elif not valid_date(date_naissance):
        raise ValueError("La date de naissance est invalide")
    elif not isinstance(pays_origine, str):
        raise ValueError("Le pays d'origine doit être un string")
    
    laplateforme = conn.connect()

    cursor = laplateforme.cursor()

    cursor.execute("SELECT id FROM animal")
    animals = cursor.fetchall()
    if len(animals) == 0:
        increment_start = 1
    else:
        id_list = []
        for animal in animals:
            id_list.append(animal[0][0])
        increment_start = max(id_list) + 1

    cursor.execute(f"ALTER TABLE animal AUTO_INCREMENT = {increment_start}")
    laplateforme.commit()

    cursor.execute(
        f"INSERT INTO animal (nom, race, id_cage, date_naissance, pays_origine) "
        f"VALUES ('{nom}', '{race}', {id_cage}, '{date_naissance}', '{pays_origine}')"
    )
    laplateforme.commit()
    cursor.close()

    laplateforme.close()


def read_animals():
    laplateforme = conn.connect()

    cursor = laplateforme.cursor()
    cursor.execute("SELECT * FROM animal")
    animals = cursor.fetchall()
    for animal in animals:
        output = (
            f"Nom: {animal[1]}\n"
            f"Race: {animal[2]}\n"
            f"Né(e) le {animal[4]}\n"
            f"Pays d'origine: {animal[5]}\n"
            f"Numéro cage: {animal[3]}\n"
        )
        print(output)
    cursor.close()

    laplateforme.close()


def update_animal(animal_id, value_name, new_value):
    if not isinstance(animal_id, int):
        raise ValueError("L'ID de l'animal doit être un integer")
    elif not isinstance(value_name, str):
        raise ValueError("Le nom de l'attribut doit être un string")

    laplateforme = conn.connect()

    cursor = laplateforme.cursor()
    cursor.execute(f"UPDATE animal SET {value_name} = {new_value} WHERE id = {animal_id}")
    laplateforme.commit()
    cursor.close()

    laplateforme.close()


def delete_animal(animal_id):
    if not isinstance(animal_id, int):
        raise ValueError("L'ID de l'animal doit être un integer")
    
    laplateforme = conn.connect()

    cursor = laplateforme.cursor()
    cursor.execute(f"DELETE FROM animal WHERE id = {animal_id}")
    laplateforme.commit()
    cursor.close()

    laplateforme.close()


# FONCTIONS MENUS ANIMAUX
def create_animal_menu():
    while True:
        nom = input("Quel est le nom de l'animal?\n")
        if len(nom) == 0:
            print("Nom invalide")
            continue
        break

    while True:
        race = input("Quel est la race de l'animal?\n")
        if len(race) == 0:
            print("Race invalide")
            continue
        break

    while True:
        id_cage = input("Quel est le numéro de la cage?\n")
        if not id_cage.isdigit():
            print("Numéro invalide")
            continue
        id_cage = int(id_cage)
        break

    while True:
        date_naissance = input("Quelle est la date de naissance? (AAAA-MM-JJ)\n")
        if not valid_date(date_naissance):
            print("Date de naissance invalide")
            continue
        break

    while True:
        pays_origine = input("Quel est le pays d'origine de l'animal?\n")
        if len(pays_origine) == 0:
            print("pays_origine invalide")
            continue
        break

    while True:
        confirmation = input(
            "Êtes-vous sûr d'ajouter cet animal?\n"
            "[O]ui ou [N]on?\n"
        )
        if confirmation == "O":
            create_animal(nom, race, id_cage, date_naissance, pays_origine)
            break
        elif confirmation == "N":
            break
        else:
            print("Choix invalide")


def update_animal_menu():
    while True:
        animal_id = input("Quelle est l'ID de l'animal?\n")
        if not animal_id.isdigit():
            print("ID invalide")
            continue
        animal_id = int(animal_id)
        break

    attributes = {
        "1": "nom",
        "2": "race",
        "3": "id_cage",
        "4": "date_naissance",
        "5": "pays_origine"
    }
    while True:
        choice = input(
            "Quel attribut souhaitez vous modifiez?\n"
            "1) Nom\n"
            "2) Race\n"
            "3) Numéro de la cage\n"
            "4) Date de naissance\n"
            "5) Le pays d'origine\n"
        )
        if choice in attributes:
            attribute = attributes[choice]
            break
        else:
            print("Choix invalide")

    while True:
        new_value = input("A quoi modifier cette attribut?\n")
        if attribute == "date_naissance" and not valid_date(new_value):
            print("Date invalide")
            continue
        elif attribute == "id_cage" and not new_value.isdigit():
            print("Numéro cage invalide")
            continue
        else:
            new_value = "'" + new_value + "'"
        break

    while True:
        confirmation = input(
            "Êtes-vous sûr?\n"
            "[O]ui ou [N]on?"
        )
        if confirmation == "O":
            update_animal(animal_id, attribute, new_value)
            break
        elif confirmation == "N":
            break
        else:
            print("Choix invalide")


def delete_animal_menu():
    while True:
        animal_id = input("Quelle est l'ID de l'animal?\n")
        if not animal_id.isdigit():
            print("ID invalide")
            continue
        animal_id = int(animal_id)
        break
    
    while True:
        confirmation = input(
            "Êtes-vous sûr?\n"
            "[O]ui ou [N]on?\n"
        )
        if confirmation == "O":
            delete_animal(animal_id)
            break
        elif confirmation == "N":
            break
        else:
            print("Choix invalide")


def animals_menu():
    options = {
        "1": create_animal_menu,
        "2": read_animals,
        "3": update_animal_menu,
        "4": delete_animal_menu
    }

    while True:
        choice = input(
            "Que souhaitez vous faire?\n"
            "1) Ajouter un animal\n"
            "2) Afficher les animaux\n"
            "3) Mettre à jour les infos d'un animal\n"
            "4) Supprimer un animal\n"
            "5) Revenir en arrière\n"
        )
        if choice == "5":
            break
        elif choice in options:
            options[choice]()
        else:
            print("Choix invalide")

