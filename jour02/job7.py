import mysql.connector


laplateforme = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CV&$i7mx$oZDrq",
    database="laplateforme"
)

cursor = laplateforme.cursor(buffered=True)
cursor.execute("SELECT * FROM employe WHERE salaire > 3000")
employes = cursor.fetchall()
for employe in employes:
    print(employe)

cursor.execute("SELECT nom, prenom, id_service FROM employe")
employes = cursor.fetchall()
print(employes)
cursor.execute("SELECT * FROM service")
services = cursor.fetchall()
print(services)
for employe in employes:
    string = (
        f"{employe[1]} {employe[0]}: "
        f"{services[employe[2] - 1][1]}"
        )
    print(string)

cursor.close()

laplateforme.close()


class Employe:
    def open_connection(self):
        laplateforme = mysql.connector.connect(
            host="localhost",
            user="root",
            password="CV&$i7mx$oZDrq",
            database="laplateforme"
        )
        return laplateforme

    def create(self, nom, prenom, salaire, id_service):
        if not isinstance(nom, str):
            raise ValueError("Le nom doit être un string")
        elif not isinstance(nom, str):
            raise ValueError("Le prénom doit être un string")
        elif not isinstance(salaire, float):
            raise ValueError("Le salaire doit être un float")
        elif not isinstance(id_service, int):
            raise ValueError("L'id service doit être un integer")

        laplateforme = self.open_connection()
        cursor = laplateforme.cursor(buffered = True)
        cursor.execute("SELECT id FROM employe")
        employes_id = cursor.fetchall()
        id_list = []
        for i in employes_id:
            id_list.append(i[0])
        increment_start = max(id_list) + 1
        cursor.execute(f"ALTER TABLE employe AUTO_INCREMENT = {increment_start}")
        cursor.execute(
            f"INSERT INTO employe (nom, prenom, salaire, id_service) "
            f"VALUES ('{nom}', '{prenom}', {salaire}, {id_service})"
        )
        laplateforme.commit()
        cursor.close()
        laplateforme.close()

    def read(self):
        laplateforme = self.open_connection()
        cursor = laplateforme.cursor(buffered = True)
        cursor.execute("SELECT * FROM employe")
        employe = cursor.fetchall()
        print(employe)
        cursor.close()
        laplateforme.close()

    def update(self, id_employe, value_name, new_value):
        if not isinstance(id_employe, int):
            raise ValueError("ID doit être un integer")
        if not isinstance(value_name, str):
            raise ValueError("Le nom de la valeur doit être un string")
        laplateforme = self.open_connection()
        cursor = laplateforme.cursor(buffered = True)
        cursor.execute(
            f"UPDATE employe set {value_name} = {new_value} WHERE id = {id_employe}"
        )
        laplateforme.commit()
        cursor.close()
        laplateforme.close()

    def delete(self, id_employe):
        if not isinstance(id_employe, int):
            raise ValueError("ID doit être un integer")
        laplateforme = self.open_connection()
        cursor = laplateforme.cursor(buffered = True)
        cursor.execute(f"DELETE FROM employe WHERE id = {id_employe}")
        laplateforme.commit()
        cursor.close()
        laplateforme.close()

employe = Employe()
employe.create("Doe", "Jane", 3800.72, 2)
employe.read()
employe.update(5, "salaire", 3900.29)
employe.read()
employe.delete(5)
employe.read()