import time
import datetime
import random
import json
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS loungebot(name TEXT, userid TEXT, balance INTEGER, xp BIGINT, level INTEGER, daily BIGINT)')



def add_me(ctx):
	c.execute("SELECT userid FROM loungebot")
	rows = c.fetchall()
	string = '\n'.join(str(row) for row in rows)
	if not str(ctx.message.author.id) in string:
		c.execute("INSERT INTO loungebot VALUES(%s,%s,0,0,0,0)",(ctx.message.author.display_name,ctx.message.author.id))
		conn.commit()


def addonmessage(message):
	c.execute("SELECT userid FROM loungebot")
	rows = c.fetchall()
	string = '\n'.join(str(row) for row in rows)
	if not str(message.author.id) in string:
		c.execute("INSERT INTO loungebot VALUES(%s,%s,0,0,0,0)",(message.author.display_name,message.author.id))
		conn.commit()

def leaderboard():
	c.execute('SELECT name, balance FROM loungebot ORDER BY balance DESC LIMIT 5')
	rows = c.fetchall()
	lines = '\n'.join(f'{i+1}. {line}<:Coin:439199818447978508>' for i, line in enumerate(rows))
	return lines
	
def everyone():
	c.execute('SELECT name, balance, level FROM loungebot')
	rows = c.fetchall()
	lines = '\n'.join(f'{i+1}. {line}' for i, line in enumerate(rows))
	return lines

def getdaily(ctx):
	c.execute('SELECT daily FROM loungebot WHERE userid= %s', (ctx.message.author.id,))
	inted = str(c.fetchone())
	data1 = inted.replace("(","")
	data2 = data1.replace(")","")
	data3 = data2.replace(",","")
	data4 = int(data3) - int(time.time())
	floated = str(datetime.datetime.utcfromtimestamp(int(data4)).strftime("%H Hours %M Minutes %S Seconds"))
	return floated
	

def daily(ctx):
	now = int(time.time())
	dailytime = now + 86400
	c.execute('SELECT daily FROM loungebot WHERE userid= %s', (ctx.message.author.id,))
	inted = str(c.fetchone())
	data1 = inted.replace("(","")
	data2 = data1.replace(")","")
	data3 = data2.replace(",","")
	floated = int(data3)
	if floated <= now:
		c.execute('UPDATE loungebot SET balance = balance + 100 WHERE userid = %s', (ctx.message.author.id,))
		c.execute('UPDATE loungebot SET daily = %s WHERE userid = %s', (dailytime,ctx.message.author.id,))
		return True
	else:
		return False

def syncname(ctx):
	c.execute('UPDATE loungebot SET name = %s WHERE userid = %s', (ctx.message.author.display_name,ctx.message.author.id,))

def setlevel(member,amount):
	c.execute("SELECT userid FROM loungebot")
	rows = c.fetchall()
	string = '\n'.join(str(row) for row in rows)
	if not str(member.id) in string:
		c.execute("INSERT INTO loungebot VALUES(%s,%s,100,0,0,0)",(member.display_name,member.id))
		conn.commit()
	c.execute('UPDATE loungebot SET level = %s WHERE userid = %s', (amount,member.id,))

def setmoney(member,amount):
	c.execute('UPDATE loungebot SET balance = %s WHERE userid = %s', (amount,member.id,))

def donate(ctx,member,amount):
	c.execute('SELECT balance FROM loungebot WHERE userid= %s', (ctx.message.author.id,))
	inted = str(c.fetchone())
	data1 = inted.replace("(","")
	data2 = data1.replace(")","")
	data3 = data2.replace(",","")
	inted = int(data3)
	if inted >= int(amount):
		if int(amount) >= 1:
			c.execute('UPDATE loungebot SET balance = balance + %s WHERE userid = %s', (amount,member.id,))
			c.execute('UPDATE loungebot SET balance = balance - %s WHERE userid = %s', (amount,ctx.message.author.id,))
			message = ctx.message.author.mention+" gave "+member.mention+" "+amount+"<:Coin:439199818447978508>"
		else:
			if int(amount) == 0:
				message = ctx.message.author.mention+", you can't give someone nothing!"
			else:
				message = ctx.message.author.mention+", you can't steal from someone :wink:"
	else:
		message = "You do not have enough <:Coin:439199818447978508> to do this!"
	return message

	
def balance(ctx):
	c.execute('SELECT balance FROM loungebot WHERE userid=  %s', (ctx.message.author.id,))
	data = c.fetchone()
	if data is None:
		data4 = "None? How did you even manage this?"
	else:
		data = str(data)
		data1 = data.replace("(","")
		data2 = data1.replace(")","")
		data3 = data2.replace(",","")
		data4 = data3+" <:Coin:439199818447978508>"
	return data4
	
	
def xpfind(ctx):
	c.execute('SELECT xp FROM loungebot WHERE userid= %s', (ctx.message.author.id,))
	data = c.fetchone()
	if data is None:
		data4 = "None? How did you even manage this?"
	else:
		data = str(data)
		data1 = data.replace("(","")
		data2 = data1.replace(")","")
		data3 = data2.replace(",","")
		data4 = data3
	return data4
	
def whoisbalance(member):
	c.execute('SELECT balance FROM loungebot WHERE userid= %s' , (member.id,))
	data = c.fetchone()
	if data is None:
		data4 = "Not added to chill bot!"
	else:
		data = str(data)
		data1 = data.replace("(","")
		data2 = data1.replace(")","")
		data3 = data2.replace(",","")
		data4 = data3+" <:Coin:439199818447978508>"
	return data4

def whoislevel(member):
    c.execute('SELECT level FROM loungebot WHERE userid= %s', (member.id,))
    data = c.fetchone()
    if data is None:
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175663001894932/Level0.png"
    else:
        data = str(data)
        data1 = data.replace("(","")
        data2 = data1.replace(")","")
        data3 = data2.replace(",","")
        if data3 == "0":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175663001894932/Level0.png"
        elif data3 == "1":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175684338581504/Level1.png"
        elif data3 == "2":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175723752456193/Level2.png"
        elif data3 == "3":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175738193182721/Level3.png"
        elif data3 == "4":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175760729440257/Level4.png"
        elif data3 == "5":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175775761694721/Level5.png"
        elif data3 == "6":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175791389802507/Level6.png"
        elif data3 == "7":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175806266867733/Level7.png"
        elif data3 == "8":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175824440786975/Level8.png"
        elif data3 == "9":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175838324064257/Level9.png"
        elif data3 == "10":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175853754908673/Level10.png"
        elif data3 == "11":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175872247463946/Level11.png"
        elif data3 == "12":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175888013721601/Level12.png"
        elif data3 == "13":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175908750622735/Level13.png"
        elif data3 == "14":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175950517370880/Level14.png"
        elif data3 == "15":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175965985832991/Level15.png"
        elif data3 == "16":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175979688886272/Level16.png"
        elif data3 == "17":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175996612771840/Level17.png"
        elif data3 == "18":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440176014895742976/Level18.png"
        elif data3 == "19":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440176028027977738/Level19.png"
        elif data3 == "20":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440176045837254677/Level20.png"
        elif data3 == "21":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532412521906182/level1.png"
        elif data3 == "22":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532429257048077/level2.png"
        elif data3 == "23":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532437498855424/level3.png"
        elif data3 == "24":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532444750675969/level4.png"
        elif data3 == "25":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532451541254145/level5.png"
        elif data3 == "26":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532456947843082/level6.png"
        elif data3 == "27":
            data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532462819999744/level7.png"
        elif data3 == "28":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532469673361418/level8.png"
        elif data3 == "29":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532474903527424/level9.png"
        elif data3 == "30":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532480956170240/level10.png"
        elif data3 == "31":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532486236536862/level11.png"
        elif data3 == "32":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532490913185822/level12.png"
        elif data3 == "33":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532490913185822/level12.png"
        elif data3 == "34":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532504402067461/level14.png"
        elif data3 == "35":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532510408441866/level15.png"
        elif data3 == "36":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532515324166144/level16.png"
        elif data3 == "37":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532523951980544/level17.png"
        elif data3 == "38":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532529521754133/level18.png"
        elif data3 == "39":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532534647324682/level19.png"
        elif data3 == "40":
            data3 = "https://media.discordapp.net/attachments/426305280955908096/444532538434781185/level20.png"
    return data3

def numblevel(member):
	c.execute('SELECT level FROM loungebot WHERE userid= %s', (member.id,))
	data = c.fetchone()
	if data is None:
		data3 = 0
	else:
		data = str(data)
		data1 = data.replace("(","")
		data2 = data1.replace(")","")
		data3 = data2.replace(",","")
	return int(data3)


def win(ctx,bet):
	c.execute('UPDATE loungebot SET balance = balance + %s WHERE userid = %s',  (bet,ctx.message.author.id,))
	conn.commit()

def lose(ctx,bet):
	c.execute('UPDATE loungebot SET balance = balance - %s WHERE userid = %s', (bet,ctx.message.author.id,))
	conn.commit()

_to10=[100,110,120,130,140,150]
def xp(message):
	if not "vip" in [y.name.lower() for y in message.author.roles]:
		c.execute('UPDATE loungebot SET xp = xp + %(rand)s WHERE userid = %(id)s', {
		'rand': random.choice(_to10), 
		'id': message.author.id
		})
		conn.commit()
	else:
		c.execute('UPDATE loungebot SET xp = xp + %(rand)s WHERE userid = %(id)s', {
		'rand': random.choice(_to10)*2,
		'id': message.author.id
		})
		conn.commit()

def xpcheck(message):
    c.execute('SELECT xp FROM loungebot WHERE userid= %s', (message.author.id,))
    inted = str(c.fetchone())
    data1 = inted.replace("(","")
    data2 = data1.replace(")","")
    data3 = data2.replace(",","")
    inted = int(data3)
    c.execute('SELECT level FROM loungebot WHERE userid= %s', (message.author.id,))
    inted2 = str(c.fetchone())
    data11 = inted2.replace("(","")
    data12 = data11.replace(")","")
    data13 = data12.replace(",","")
    inted2 = int(data13)
    if inted >= 1100 and inted2 <= 0:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 2200 and inted2 <= 1:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 3300 and inted2 <= 2:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 4400 and inted2 <= 3:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 5500 and inted2 <= 4:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 6600 and inted2 <= 5:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 7700 and inted2 <= 6:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 8800 and inted2 <= 7:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 9900 and inted2 <= 8:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 11000 and inted2 <= 9:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 22000 and inted2 <= 10:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 33000 and inted2 <= 11:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 44000 and inted2 <= 12:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 55000 and inted2 <= 13:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 66000 and inted2 <= 14:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 77000 and inted2 <= 15:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 88000 and inted2 <= 16:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 99000 and inted2 <= 17:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 110000 and inted2 <= 18:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 220000 and inted2 <= 19:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 330000 and inted2 <=22:    # <--- start of prestige 2 so level 1
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 440000 and inted2 <=23:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 550000 and inted2 <= 24:
        c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
        return True
        conn.commit()
    elif inted >= 660000 and inted2 <= 25:
	    c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
	    return True
	    conn.commit()
    elif inted >= 770000 and inted2 <= 26:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 880000 and inted2 <= 27:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 990000 and inted2 <= 28:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 1100000 and inted2 <= 29:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 1200000 and inted2 <= 30:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 1300000 and inted2 <= 31:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 1400000 and inted2 <= 32:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 1500000 and inted2 <= 33:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 1600000 and inted2 <= 34:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 1700000 and inted2 <= 35:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 1800000 and inted2 <= 36:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 1900000 and inted2 <= 37:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 2000000 and inted2 <= 38:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 2100000 and inted2 <= 39:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
    elif inted >= 2200000 and inted2 < 40:
       c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (message.author.id,))
       return True
       conn.commit()
	

def prestige(ctx):
	c.execute('UPDATE loungebot SET level = level + 1 WHERE userid = %s', (ctx.message.author.id,))


def level(ctx):
    c.execute('SELECT level FROM loungebot WHERE userid = %s', (ctx.message.author.id,))
    data = c.fetchone()
    data = str(data)
    data1 = data.replace("(","")
    data2 = data1.replace(")","")
    data3 = data2.replace(",","")
    if data3 == "0":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175663001894932/Level0.png"
    if data3 == "1":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175684338581504/Level1.png"
    if data3 == "2":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175723752456193/Level2.png"
    if data3 == "3":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175738193182721/Level3.png"
    if data3 == "4":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175760729440257/Level4.png"
    if data3 == "5":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175775761694721/Level5.png"
    if data3 == "6":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175791389802507/Level6.png"
    if data3 == "7":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175806266867733/Level7.png"
    if data3 == "8":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175824440786975/Level8.png"
    if data3 == "9":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175838324064257/Level9.png"
    if data3 == "10":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175853754908673/Level10.png"
    if data3 == "11":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175872247463946/Level11.png"
    if data3 == "12":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175888013721601/Level12.png"
    if data3 == "13":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175908750622735/Level13.png"
    if data3 == "14":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175950517370880/Level14.png"
    if data3 == "15":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175965985832991/Level15.png"
    if data3 == "16":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175979688886272/Level16.png"
    if data3 == "17":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175996612771840/Level17.png"
    if data3 == "18":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440176014895742976/Level18.png"
    if data3 == "19":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440176028027977738/Level19.png"
    if data3 == "20":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440176045837254677/Level20.png"
    if data3 == "21":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532412521906182/level1.png"
    if data3 == "22":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532429257048077/level2.png"
    if data3 == "23":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532437498855424/level3.png"
    if data3 == "24":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532444750675969/level4.png"
    if data3 == "25":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532451541254145/level5.png"
    if data3 == "26":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532456947843082/level6.png"
    if data3 == "27":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532462819999744/level7.png"
    if data3 == "28":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532469673361418/level8.png"
    if data3 == "29":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532474903527424/level9.png"
    if data3 == "30":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532480956170240/level10.png"
    if data3 == "31":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532486236536862/level11.png"
    if data3 == "32":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532490913185822/level12.png"
    if data3 == "33":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532490913185822/level12.png"
    if data3 == "34":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532504402067461/level14.png"
    if data3 == "35":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532510408441866/level15.png"
    if data3 == "36":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532515324166144/level16.png"
    if data3 == "37":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532523951980544/level17.png"
    if data3 == "38":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532529521754133/level18.png"
    if data3 == "39":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532534647324682/level19.png"
    if data3 == "40":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532538434781185/level20.png"
    return data3

def eventlevel(message):
    c.execute('SELECT level FROM loungebot WHERE userid = %s', (message.author.id,))
    data = c.fetchone()
    data = str(data)
    data1 = data.replace("(","")
    data2 = data1.replace(")","")
    data3 = data2.replace(",","")
    if data3 == "0":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175663001894932/Level0.png"
    if data3 == "1":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175684338581504/Level1.png"
    if data3 == "2":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175723752456193/Level2.png"
    if data3 == "3":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175738193182721/Level3.png"
    if data3 == "4":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175760729440257/Level4.png"
    if data3 == "5":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175775761694721/Level5.png"
    if data3 == "6":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175791389802507/Level6.png"
    if data3 == "7":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175806266867733/Level7.png"
    if data3 == "8":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175824440786975/Level8.png"
    if data3 == "9":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175838324064257/Level9.png"
    if data3 == "10":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175853754908673/Level10.png"
    if data3 == "11":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175872247463946/Level11.png"
    if data3 == "12":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175888013721601/Level12.png"
    if data3 == "13":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175908750622735/Level13.png"
    if data3 == "14":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175950517370880/Level14.png"
    if data3 == "15":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175965985832991/Level15.png"
    if data3 == "16":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175979688886272/Level16.png"
    if data3 == "17":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440175996612771840/Level17.png"
    if data3 == "18":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440176014895742976/Level18.png"
    if data3 == "19":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440176028027977738/Level19.png"
    if data3 == "20":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/440176045837254677/Level20.png"
    if data3 == "21":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532412521906182/level1.png"
    if data3 == "22":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532429257048077/level2.png"
    if data3 == "23":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532437498855424/level3.png"
    if data3 == "24":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532444750675969/level4.png"
    if data3 == "25":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532451541254145/level5.png"
    if data3 == "26":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532456947843082/level6.png"
    if data3 == "27":
        data3 = "https://cdn.discordapp.com/attachments/426305280955908096/444532462819999744/level7.png"
    if data3 == "28":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532469673361418/level8.png"
    if data3 == "29":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532474903527424/level9.png"
    if data3 == "30":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532480956170240/level10.png"
    if data3 == "31":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532486236536862/level11.png"
    if data3 == "32":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532490913185822/level12.png"
    if data3 == "33":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532490913185822/level12.png"
    if data3 == "34":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532504402067461/level14.png"
    if data3 == "35":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532510408441866/level15.png"
    if data3 == "36":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532515324166144/level16.png"
    if data3 == "37":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532523951980544/level17.png"
    if data3 == "38":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532529521754133/level18.png"
    if data3 == "39":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532534647324682/level19.png"
    if data3 == "40":
        data3 = "https://media.discordapp.net/attachments/426305280955908096/444532538434781185/level20.png"
    return data3
	


def xplevel(ctx):
	c.execute('SELECT level FROM loungebot WHERE userid = %s', (ctx.message.author.id,))
	data = c.fetchone()
	data = str(data)
	data1 = data.replace("(","")
	data2 = data1.replace(")","")
	data3 = data2.replace(",","")
	if data3 == "0":
		data3 = "1100"
	if data3 == "1":
		data3 = "2200"
	if data3 == "2":
		data3 = "3300"
	if data3 == "3":
		data3 = "4400"
	if data3 == "4":
		data3 = "5500"
	if data3 == "5":
		data3 = "6600"
	if data3 == "6":
		data3 = "7700"
	if data3 == "7":
		data3 = "8800"
	if data3 == "8":
		data3 = "9900"
	if data3 == "9":
		data3 = "11000"
	if data3 == "10":
		data3 = "22000"
	if data3 == "11":
		data3 = "33000"
	if data3 == "12":
		data3 = "44000"
	if data3 == "13":
		data3 = "55000"
	if data3 == "14":
		data3 = "66000"
	if data3 == "15":
		data3 = "77000"
	if data3 == "16":
		data3 = "88000"
	if data3 == "17":
		data3 = "99000"
	if data3 == "18":
		data3 = "110000"
	if data3 == "19":
		data3 = "220000"
	if data3 == "20":
		data3 = "∞"
	if data3 == "21":      # <---- start of prestige 2
		data3 = "330000"
	if data3 == "22":
		data3 = "440000"
	if data3 == "23":
		data3 = "550000"
	if data3 == "24":
		data3 = "660000"
	if data3 == "25":
		data3 = "770000"
	if data3 == "26":
		data3 = "880000"
	if data3 == "27":
		data3 = "990000"
	if data3 == "28":
		data3 = "1100000"
	if data3 == "29":
		data3 = "1200000"
	if data3 == "30":
		data3 = "1300000"
	if data3 == "31":
		data3 = "1400000"
	if data3 == "32":
		data3 = "1500000"
	if data3 == "33":
		data3 = "1600000"
	if data3 == "34":
		data3 = "1700000"
	if data3 == "35":
		data3 = "1800000"
	if data3 == "36":
		data3 = "1900000"
	if data3 == "37":
		data3 = "2000000"
	if data3 == "38":
		data3 = "2100000"
	if data3 == "39":
		data3 = "2200000"
	if data3 == "40":
		data3 = "∞"
	return data3



def checkforbet(ctx,bet):
    c.execute('SELECT balance FROM loungebot WHERE userid= %s', (ctx.message.author.id,))
    inted = str(c.fetchone())
    data1 = inted.replace("(","")
    data2 = data1.replace(")","")
    data3 = data2.replace(",","")
    inted = int(data3)
    if inted >= int(bet):
        return True


		
def checkbal(message):
	c.execute('SELECT balance FROM loungebot WHERE userid=  %s', (message.author.id,))
	data = c.fetchone()
	if data is None:
		data4 = "None? How did you even manage this?"
	else:
		data = str(data)
		data1 = data.replace("(","")
		data2 = data1.replace(")","")
		data3 = data2.replace(",","")
	return data3


def randomdrop(message):
	c.execute('UPDATE loungebot SET balance = balance + 100 WHERE userid = %s',  (message.author.id,))
	conn.commit()

create_table()
