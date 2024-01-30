import mysql.connector

laplateforme = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CV&$i7mx$oZDrq",
    database="laplateforme"
)

cursor = laplateforme.cursor(buffered=True)
cursor.execute("SELECT capacite FROM salle")
salle = cursor.fetchall()
total = 0
for capacite in salle:
    total += capacite[0]
print(total)
cursor.close()

laplateforme.close()