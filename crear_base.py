import sqlite3
print("Base de datos del bot...")
def crear_bd():
	conexion=sqlite3.connect("uno.db")
	cursor=conexion.cursor()
	try:
		cursor.execute('''CREATE TABLE uno(id integer primary KEY, nombre varchar(50),score integer)''')
	except sqlite3.OperationalError :
		print("La tabla ya existe!!!")
	else:
		print("La tabla se ha creado correctamente")
	conexion.close()
	
print("Creando bases de datos!!!")
crear_bd()
