import mysql.connector

laplateforme = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CV&$i7mx$oZDrq",
    database="laplateforme"
)

cursor = laplateforme.cursor(buffered=True)
cursor.execute("SELECT nom, capacite FROM salle")
salle = cursor.fetchall()
print(salle)
cursor.close()

laplateforme.close()