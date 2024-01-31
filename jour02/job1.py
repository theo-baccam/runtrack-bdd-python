import mysql.connector

laplateforme = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CV&$i7mx$oZDrq",
    database="laplateforme"
)

cursor = laplateforme.cursor(buffered=True)
cursor.execute("SELECT * FROM etudiant")
etudiant = cursor.fetchall()
cursor.close()

laplateforme.close()

for person in etudiant:
    print(person)