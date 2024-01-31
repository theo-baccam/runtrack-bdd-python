import mysql.connector


# Connection à base de données
laplateforme = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CV&$i7mx$oZDrq",
    database="laplateforme"
)

# Curseur pour intéragir avec la base de données
cursor = laplateforme.cursor(buffered=True)
cursor.execute("SELECT * FROM etudiant")
etudiant = cursor.fetchall()
cursor.close()

laplateforme.close()

for person in etudiant:
    print(person)