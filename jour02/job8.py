from job8 import job8_cage as cage
from job8 import job8_animal as anim

# Je n'ai pas fait de classes comme dans le job 7 car on a pas besoin
# de gérer les attributs d'objets.


def main_menu():
    options = {
        "1": cage.cages_menu,
        "2": anim.animals_menu
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