import mysql.connector

# fonction séparé pour connection
def connect():
    laplateforme = mysql.connector.connect(
        host="localhost",
        user="root",
        password="CV&$i7mx$oZDrq",
        database="laplateforme"
    )
    return laplateforme