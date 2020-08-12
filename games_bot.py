import discord
from discord.ext import commands
from discord.utils import get
import sqlite3
counter=0
bot = commands.Bot(command_prefix='-', description="This is a Helper Bot")
@bot.command()
async def hi(ctx):
	usuario = ctx.message.author
	embed = discord.Embed(title="", description="Hola, {0.mention}".format(usuario),color=0x3EBA89) #,color=Hex code
	await ctx.send(embed=embed)

@bot.command()	
async def lb(ctx):
	global counter
	conexion=sqlite3.connect("uno.db")
	cursor=conexion.cursor()
	cadena=""
	embed = discord.Embed(title="Marcador UNO!", description="",color=0x3EBA89)
	try:
		cursor.execute('SELECT * from uno ORDER BY score DESC')	
	except sqlite3.OperationalError:
		print("No existe!!")
	else:
		datos=cursor.fetchall()	
		for data in datos:	
			counter+=1
			user = get(bot.get_all_members(), name=str(data[1]))	
			embed.add_field(name="#"+str(counter)+" "+format(user), value=str(data[2]), inline=False)
			#cadena= cadena+format(user)+" "+str(data[2])+"\n"
	counter=0
	print(cadena)	
	await ctx.send(embed=embed)		
	
@bot.listen()
async def on_message(message):
	if "the game is now over" in message.content.lower():
		conexion=sqlite3.connect("uno.db")
		cursor=conexion.cursor()
		usuario = message.author
		cadena=str(message.content)
		x=cadena.find("1.")
		y=cadena.find("2.")
		cadena=cadena[x+3:y-6]		
		
		user = get(bot.get_all_members(), name=cadena)				
		#if usuario.name == 'UNO' and usuario.id==403419413904228352:
		embed = discord.Embed(title="", description="Enhorabuena {0.mention}!!! Has ganado la partida".format(user),color=0x3EBA89) #,color=Hexcode
	
		await message.channel.send(embed=embed)				
		try:
			cursor.execute('SELECT * from uno where id={}'.format(user.id))			
		except sqlite3.OperationalError:
			print("No existe!!")
		
		c=cursor.fetchall()	
		if len(c) == 0:
			print("Vacio")
			consulta = "INSERT INTO uno(id, nombre,score) VALUES (?, ?, ?);"
			cursor.execute(consulta, (format(user.id), format(user.name),0))
			cursor.execute('SELECT * from uno where id={}'.format(user.id))	
			c=cursor.fetchall()	
			
		for data in c:			
			counter=data[2]
			sql_update_query = "update uno set score = ? where id = ?;"
			inputData = (counter+1, format(user.id))
			cursor.execute(sql_update_query, inputData)			
		conexion.commit()
		cursor.close()		
		conexion.close()
		await bot.process_commands(message)		
bot.run('NzM3OTIzMTYzNTEzNTUyOTc2.XyEagA.f5LXyTqButLJ4Qpaj4g1V5hbmTM')
