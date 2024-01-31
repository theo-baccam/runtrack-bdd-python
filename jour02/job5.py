import mysql.connector


laplateforme = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CV&$i7mx$oZDrq",
    database="laplateforme"
)

cursor = laplateforme.cursor(buffered=True)
cursor.execute("SELECT superficie FROM etage")
etage = cursor.fetchall()
cursor.close()

laplateforme.close()

total = 0
for superficie in etage:
    total += superficie[0]
print(f"La superficie de La Plateforme est de {total} m2")