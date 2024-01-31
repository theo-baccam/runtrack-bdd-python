from functools import partial
from datetime import datetime

import mysql.connector


def connect():
    laplateforme = mysql.connector.connect(
        host="localhost",
        user="root",
        password="CV&$i7mx$oZDrq",
        database="laplateforme"
    )
    return laplateforme


def create_cage(superficie, capacite):
    if not isinstance(superficie, int):
        print("La superficie doit être un integer")
        return
    elif not isinstance(capacite, int):
        print("La capacité doit être un integer")
        return

    laplateforme = connect()
    
    cursor = laplateforme.cursor()

    cursor.execute("SELECT id FROM cage")
    cages = cursor.fetchall()
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
    laplateforme = connect()

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
    laplateforme = connect()

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
    laplateforme = connect()

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
    
    laplateforme = connect()

    cursor = laplateforme.cursor()
    cursor.execute(f"UPDATE cage SET {value_name} = {new_value} WHERE id = {cage_id}")
    laplateforme.commit()
    cursor.close()

    laplateforme.close()


def delete_cage(cage_id):
    if not isinstance(cage_id, int):
        print("L'identifiant de cage doit être un integer")
        return
    
    laplateforme = connect()

    cursor = laplateforme.cursor()
    cursor.execute(f"DELETE FROM cage WHERE id = {cage_id}")
    laplateforme.commit()
    cursor.close()

    laplateforme.close()


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
    
    laplateforme = connect()

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
    laplateforme = connect()

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

    laplateforme = connect()

    cursor = laplateforme.cursor()
    cursor.execute(f"UPDATE animal SET {value_name} = {new_value} WHERE id = {animal_id}")
    laplateforme.commit()
    cursor.close()

    laplateforme.close()


def delete_animal(animal_id):
    if not isinstance(animal_id, int):
        raise ValueError("L'ID de l'animal doit être un integer")
    
    laplateforme = connect()

    cursor = laplateforme.cursor()
    cursor.execute(f"DELETE FROM animal WHERE id = {animal_id}")
    laplateforme.commit()
    cursor.close()

    laplateforme.close()


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


def main_menu():
    options = {
        "1": cages_menu,
        "2": animals_menu
    }

    while True:
        choice = input(
            "Que souhaitez vous consulter?\n"
            "1) Les cages\n"
            "2) Les animaux\n"
            "3) Je veux quitter\n"
        )
        if choice == "3":
            break
        elif choice in options:
            options[choice]()
        else:
            print("Choix invalide")

main_menu()