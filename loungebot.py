import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import time
import re
import random
from random import sample
import datetime
#from google import google
import dbhandler
import os


dbhandler.create_table()

       
bot=commands.Bot(description="Lounge bot. This bot was brought to you by royalnoob. Built from scratch.",command_prefix="-",pm_help=False)
       
bot.remove_command('help')
       
t = datetime.datetime.now()


    
@commands.has_role("Manager")
@bot.command()
async def close():
    dbhandler.close()
      
@bot.command(pass_context=True)
async def sync(ctx):
    dbhandler.syncname(ctx)
    await bot.add_reaction(message = ctx.message, emoji = "✅")
       
@bot.command(pass_context=True)
async def prestige(ctx):
    if dbhandler.level(ctx) == "https://cdn.discordapp.com/attachments/426305280955908096/440176045837254677/Level20.png":
        await bot.say("Welcome "+ctx.message.author.display_name+" to prestige 2!")
        dbhandler.prestige(ctx)
    else:
        await bot.say(ctx.message.author.display_name+", You need to be level 20 in the first prestige first!")
       
@commands.has_role("Manager")
@bot.command()
async def setlevel(member:discord.Member,amount):
    dbhandler.setlevel(member,amount)
       

@bot.command(pass_context=True)
async def setmoney(ctx,member:discord.Member,amount):
	if "manager" in [y.name.lower() for y in ctx.message.author.roles]:
		dbhandler.setmoney(member,amount)
		await bot.add_reaction(message = ctx.message, emoji = "✅")
	else:
		await bot.add_reaction(message = ctx.message, emoji = "🚫")
       
@bot.command(pass_context=True)
async def donate(ctx,member:discord.Member,amount):
    await bot.say(dbhandler.donate(ctx,member,amount))

@bot.command(pass_context=True, aliases=["d"])
async def daily(ctx):
	if ctx.message.channel.id == "455856117516337179":
		if dbhandler.daily(ctx) == True:
			await bot.add_reaction(message = ctx.message, emoji = "✅")
			embed = discord.Embed(title="Daily | "+ctx.message.author.display_name,description="**Added 100<:coin:456086215909965825>!**\nBe sure to use -daily again tomorrow to gain another 100<:Coin:439199818447978508>!",colour=0xFF0000)
		else:
			await bot.add_reaction(message = ctx.message, emoji = "🚫")
			embed = discord.Embed(title="Daily | "+ctx.message.author.display_name,description="You have already claimed your daily today!\nYou can use this command again in "+dbhandler.getdaily(ctx)+" !",colour=0xFF0000)
		await bot.say(embed=embed)
	else:
		userID = ctx.message.author.id
		await bot.delete_message(ctx.message)
		await bot.say(" Hey <@%s> You need to be in <#455856117516337179> to use -daily !" % (userID))
		
           
       
@bot.command(pass_context=True)
async def xp(ctx):
    embed=discord.Embed(title=ctx.message.author.display_name+" | XP",description="You have "+dbhandler.xpfind(ctx)+" / "+dbhandler.xplevel(ctx)+"xp!",colour=0xFF0000)
    embed.set_thumbnail(url = ctx.message.author.avatar_url)
    await bot.say(embed=embed)
       
@bot.command(pass_context=True)
async def level(ctx):
    embed = discord.Embed(title="Level | "+ctx.message.author.display_name,description=None,colour=0xFF0000)
    embed.set_thumbnail(url = dbhandler.level(ctx))
    await bot.send_message(ctx.message.channel,embed=embed)
       
@bot.command(pass_context=True, aliases=["b"])
async def balance(ctx,*,member:discord.Member=None):
	if member == None:
		member = ctx.message.author
	dbhandler.add_me(ctx)
	embed=discord.Embed(title="Balance | "+member.display_name,description="**"+str(dbhandler.whoisbalance(member))+"\nNice**!",colour=0xFF0000)
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_footer(text="Requested by : "+ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
	await bot.say(embed=embed)
        
@bot.command(pass_context=True, aliases=["l"])
async def leaderboard(ctx):
	status = str(dbhandler.leaderboard())
	status2 = status.replace("[","")
	status3 = status2.replace("]","")
	status4 = status3.replace("'","")
	status5 = status4.replace("(","")
	status6 = status5.replace(")","")
	status7 = status6.replace(","," -")
	embed = discord.Embed(title="Leaderboard",description=status7, color=0xFF0000)
	embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/426305280955908096/443863093445918731/Untitled.png")
	embed.set_footer(text="Requested by : "+ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
	await bot.say(embed = embed)
      
@commands.has_role("Management")
@bot.command(pass_context=True, aliases=["e"])
async def everyone(ctx):
    status = str(dbhandler.everyone())
    status2 = status.replace("[","")
    status3 = status2.replace("]","")
    status4 = status3.replace("'","")
    status5 = status4.replace("(","")
    status6 = status5.replace(")","")
    status7 = status6.replace(","," -")
    embed = discord.Embed(title="Everyone (name,balance,level)",description=status7, color=0xFF0000)
    await bot.say(embed = embed)
    
@commands.has_role("Management")
@bot.command(pass_context=True, aliases=["en"])
async def everyonenames(ctx):
    status = str(dbhandler.everyonenames())
    status2 = status.replace("[","")
    status3 = status2.replace("]","")
    status4 = status3.replace("'","")
    status5 = status4.replace("(","")
    status6 = status5.replace(")","")
    status7 = status6.replace(","," -")
    embed = discord.Embed(title="Everyone",description=status7, color=0xFF0000)
    await bot.say(embed = embed)
    
@bot.command()
async def chill():
    await bot.say("<@425957421975076864>")
       
keyz = "q"
       
@bot.command(pass_context=True)
async def help(ctx,*,command=None):
    if command == None:
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        embed1 = discord.Embed(title = "Chill Bot" , description = "Hey! Welcome the the -help handbook.\nHere you can find out all the commands you can use in the server!\nEnjoy your stay :)\nTo look at how to use a command do -help [command] to see how it works!\n\nIf you have any questions regarding the bot/commands, PM Royalnoob\nThanks to these amazing people the bot would not be as amazing as it is today!\nRoyalnoob\nCallum\nSesmic",colour = 0xFF0000)
        embed2 = discord.Embed(title = "Utility    Page 1 / 6" , description = "-status - Check if the bot is online\n-ping - Check the relay speed of the bot\n-uptime - See how long the bot has been online for\n-date - Show the date\n-profile - Shows information about the member / yourself if left blank",colour = 0xFF0000)
        embed3 = discord.Embed(title = "Actions    Page 2 / 6" , description = "-hug - Hug a member\n-kiss - Kiss a member\n-lick - Lick another member\n-slap - Slap another member\n-pat - Pat another member\n-cuddle - Cuddle woth another member\n-pout - To pout\n-bite - Bite another member",colour = 0xFF0000)
        embed4 = discord.Embed(title = "Chill Currency    Page 3 / 6" , description = "-balance/-b - Check your balance\n-leaderboard/-l - Check who the top 5 richest people on the server are\n-daily - Collect your daily Chill Coins\n-level - Check what level you are\n-xp - Check how much xp you have\n-donate - Donate your coins to another member",colour = 0xFF0000)
        embed5 = discord.Embed(title = "Games    Page 4 / 6" , description = "-8ball - Ask the Chill Bot a yes or no question\n-guess - Guess a random number between 1 and 10\n-flip - Flip a coin\n-rps - Rock paper scissors\n-coinflip - Flip a coin and earn chill currency\n-slot - (VIP only) Run a slot machine with a max prize of 10x your bet!\n-rtd - Roll The dice. Roll a 5 or 6 and you win!",colour = 0xFF0000)  
        embed6 = discord.Embed(title = "Self Assignable Roles    Page 5 / 6" , description = "-colors - Check what colors you can assign\n-colorme - Add yourself to a color\n-uncolorme - Remove yourself from a color",colour = 0xFF0000)
        embed7 = discord.Embed(title = "Pings    Page 6 / 6" , description = "-mug - Pings the mug himself\n-yiff - Pings our local furry",colour = 0xFF0000)   
        message = await bot.send_message(ctx.message.author,embed=embed1)
        await bot.add_reaction(message = message, emoji = "▶")
        while keyz == "q":
            await bot.wait_for_reaction(emoji = "▶" , message = message)
            await bot.edit_message(message = message , embed=embed1)
            await bot.wait_for_reaction(emoji = "▶" , message = message)
            await bot.edit_message(message = message , embed=embed2)
            await bot.wait_for_reaction(emoji = "▶" , message = message)
            await bot.edit_message(message = message , embed=embed3)
            await bot.wait_for_reaction(emoji = "▶" , message = message)
            await bot.edit_message(message = message , embed=embed4)
            await bot.wait_for_reaction(emoji = "▶" , message = message)
            await bot.edit_message(message = message , embed=embed5)
            await bot.wait_for_reaction(emoji = "▶" , message = message)
            await bot.edit_message(message = message , embed=embed6)
            await bot.wait_for_reaction(emoji = "▶" , message = message)
            await bot.edit_message(message = message , embed=embed7)
    elif command == "status":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-status [no argument needed]")
    elif command == "ping":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-ping [no argument needed]")
    elif command == "uptime":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-uptime [no argument needed]")
    elif command == "profile":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-profile [member] (If no member is given you are selected)")
    elif command == "hug":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-hug [member]")
    elif command == "kiss":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-kiss [member]")
    elif command == "lick":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-lick [member]")
    elif command == "slap":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-slap [member]")
    elif command == "pat":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-pat [member]")
    elif command == "cuddle":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-cuddle [member]")
    elif command == "pout":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-pout [no argument needed]")
    elif command == "bite":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-bite [member]")
    elif command == "balance":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-balance [no argument needed]")
    elif command == "leaderboard":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-leaderboard [no argument needed]")
    elif command == "daily":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-daily [no argument needed]")
    elif command == "level":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-level [no argument needed]")
    elif command == "xp":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-xp [no argument needed]")
    elif command == "donate":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-donate [member] [amount]")
    elif command == "8ball":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-8ball [question]")
    elif command == "guess":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-guess [number between 1 and 10]")
    elif command == "flip":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-flip [no argument needed]")
    elif command == "rps":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-rps [amount] [rock/paper/scissors]")
    elif command == "coinflip":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-coinflip [amount] [heads/tails]")
    elif command == "slot":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-slot [amount]")
    elif command == "mug":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-mug [no argument needed]")
    elif command == "yiff":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-yiff [no argument needed]")
    elif command == "date":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-date [no argument needed]")
    elif command == "rtd":
        await bot.add_reaction(message = ctx.message, emoji = "✅")
        await bot.send_message(ctx.message.author,"-rtd [bet]")
    else:
        await bot.add_reaction(message = ctx.message, emoji = "❌")
        
    
            
            
    
#prototype~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
_suits=("♠️","♣️","♥️","♦️")
_cards=(1,2,3,4,5,6,7,8,9,10,11)
@bot.command(pass_context=True)
async def blackjack(ctx):
    botcard1=random.choice(_cards)
    botcardsuit1 = random.choice(_suits)
    botcard2=random.choice(_cards)
    botcardsuit2 = random.choice(_suits)
    usercard1=random.choice(_cards)
    usercardsuit1 = random.choice(_suits)
    usercard2=random.choice(_cards)
    usercardsuit2 = random.choice(_suits)
    usertotal=usercard1+usercard2
    bottotal=botcard1+botcard2
    botchoice="Chill Bots cards **("+str(bottotal)+")** : "+str(botcard1)+botcardsuit1+" , "+str(botcard2)+botcardsuit2
    userchoice="Your hand **("+str(usertotal)+")** : "+str(usercard1)+usercardsuit1+" , "+str(usercard2)+usercardsuit2
    embed=discord.Embed(title="Blackjack : Chill Bot | "+ctx.message.author.display_name,description="This is blackjack, sometimes known as 21.\nEnjoy your game!\n\n"+botchoice+"\n"+userchoice,colour=0xEE82EE)
    message = await bot.say(embed=embed)
    msg = await bot.wait_for_message(
    author=ctx.message.author,
    timeout=600,
    check=lambda m: m.content.lower() in ['hit', 'stay'])
    msg=msg.content.lower()
    if msg == "hit":
        if usertotal >= 22:
            embed2=discord.Embed(title="Blackjack : Chill Bot | "+ctx.message.author.display_name,description="**Chill Bot Wins!**\n\n"+botchoice+"\n"+userchoice,colour=0xEE82EE)
            await bot.edit_message(message=message,embed=embed2)
        else:
            usercard3=random.choice(_cards)
            usercardsuit3=random.choice(_suits)
            usertotal=usertotal+usercard3
            userchoice="Your hand **("+str(usertotal)+")** : "+str(usercard1)+usercardsuit1+" , "+str(usercard2)+usercardsuit2+" , "+str(usercard3)+usercardsuit3
            embed2=discord.Embed(title="Blackjack : Chill Bot | "+ctx.message.author.display_name,description="This is blackjack, sometimes known as 21.\nEnjoy your game!\n\n"+botchoice+"\n"+userchoice,colour=0xEE82EE)
            await bot.edit_message(message=message,embed=embed2)
                
""" if msg == "stay":
        if not bottotal > usertotal:
            if not usertotal >= 22:
        else:
            embed2=discord.Embed(title="Blackjack : Chill Bot | "+ctx.message.author.display_name,description="**Chill Bot Wins!**\n\n"+botchoice+"\n"+userchoice,colour=0xEE82EE)
            await bot.edit_message(message=message,embed=embed2)
"""
    
    
    
    
    
    
    
    
    
    
    
    
@bot.command(pass_context=True)
async def slot(ctx,bet=None):
    if "vip" in [y.name.lower() for y in ctx.message.author.roles]:
        if bet != None:
            bet = int(bet)
            if dbhandler.checkforbet(ctx,bet) == True:
                if bet >= 1:
                    embed=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Welcome to the slot machine!\n\nThe possible winnings are:\n1. 🍫 🍫 🍫 - "+str(bet*10)+"<:coin:456086215909965825>\n2. 🔔 🔔 🔔/🍫 - "+str(bet*5)+"<:coin:456086215909965825>\n3. 🍇 🍇 🍇/🍫 - "+str(bet*4)+"<:coin:456086215909965825>\n4. 🍊 🍊 🍊/🍫 - "+str(bet*3)+"<:coin:456086215909965825>\n5. 2 🍒's - "+str(bet*2)+"<:coin:456086215909965825>\n6. 1 🍒 - Your "+str(bet)+"<:coin:456086215909965825> back\n\nThe slot machine will spin in 5 seconds!",colour=0xFF0000)
                    message = await bot.say(embed=embed)
                    await asyncio.sleep(1)
                    embed=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Welcome to the slot machine!\n\nThe possible winnings are:\n1. 🍫 🍫 🍫 - "+str(bet*10)+"<:coin:456086215909965825>\n2. 🔔 🔔 🔔/🍫 - "+str(bet*5)+"<:coin:456086215909965825>\n3. 🍇 🍇 🍇/🍫 - "+str(bet*4)+"<:coin:456086215909965825>\n4. 🍊 🍊 🍊/🍫 - "+str(bet*3)+"<:coin:456086215909965825>\n5. 2 🍒's - "+str(bet*2)+"<:coin:456086215909965825>\n6. 1 🍒 - Your "+str(bet)+"<:coin:456086215909965825> back\n\nThe slot machine will spin in 4 seconds!",colour=0xFF0000)
                    await bot.edit_message(message=message,embed=embed)
                    await asyncio.sleep(1)
                    embed=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Welcome to the slot machine!\n\nThe possible winnings are:\n1. 🍫 🍫 🍫 - "+str(bet*10)+"<:coin:456086215909965825>\n2. 🔔 🔔 🔔/🍫 - "+str(bet*5)+"<:coin:456086215909965825>\n3. 🍇 🍇 🍇/🍫 - "+str(bet*4)+"<:coin:456086215909965825>\n4. 🍊 🍊 🍊/🍫 - "+str(bet*3)+"<:coin:456086215909965825>\n5. 2 🍒's - "+str(bet*2)+"<:coin:456086215909965825>\n6. 1 🍒 - Your "+str(bet)+"<:coin:456086215909965825> back\n\nThe slot machine will spin in 3 seconds!",colour=0xFF0000)
                    await bot.edit_message(message=message,embed=embed)
                    await asyncio.sleep(1)
                    embed=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Welcome to the slot machine!\n\nThe possible winnings are:\n1. 🍫 🍫 🍫 - "+str(bet*10)+"<:coin:456086215909965825>\n2. 🔔 🔔 🔔/🍫 - "+str(bet*5)+"<:coin:456086215909965825>\n3. 🍇 🍇 🍇/🍫 - "+str(bet*4)+"<:coin:456086215909965825>\n4. 🍊 🍊 🍊/🍫 - "+str(bet*3)+"<:coin:456086215909965825>\n5. 2 🍒's - "+str(bet*2)+"<:coin:456086215909965825>\n6. 1 🍒 - Your "+str(bet)+"<:coin:456086215909965825> back\n\nThe slot machine will spin in 2 seconds!",colour=0xFF0000)
                    await bot.edit_message(message=message,embed=embed)
                    await asyncio.sleep(1)
                    embed=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Welcome to the slot machine!\n\nThe possible winnings are:\n1. 🍫 🍫 🍫 - "+str(bet*10)+"<:coin:456086215909965825>\n2. 🔔 🔔 🔔/🍫 - "+str(bet*5)+"<:coin:456086215909965825>\n3. 🍇 🍇 🍇/🍫 - "+str(bet*4)+"<:coin:456086215909965825>\n4. 🍊 🍊 🍊/🍫 - "+str(bet*3)+"<:coin:456086215909965825>\n5. 2 🍒's - "+str(bet*2)+"<:coin:456086215909965825>\n6. 1 🍒 - Your "+str(bet)+"<:coin:456086215909965825> back\n\nThe slot machine will spin in 1 seconds!",colour=0xFF0000)
                    await bot.edit_message(message=message,embed=embed)
                    await asyncio.sleep(1)
                    _items = ["🍒","🍋","🍊","🍇","🔔","🍫"]
                    wheel1 = random.choice(_items)
                    wheel2 = random.choice(_items)
                    wheel3 = random.choice(_items)
                    if wheel1 == "🍫" and wheel2 == "🍫" and wheel3 == "🍫":
                        bet = bet*10
                        bet = str(bet)
                        embed1=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed1)
                        bet = int(bet)
                        dbhandler.win(ctx,bet)
                    elif wheel1 == "🔔" and wheel2 == "🔔" and wheel3 == "🔔":
                        bet = bet*5
                        bet = str(bet)
                        embed2=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed2)
                        dbhandler.win(ctx,bet)
                    elif wheel1 == "🔔" and wheel2 == "🔔" and wheel3 == "🍫":
                        bet = bet*5
                        bet = str(bet)
                        embed3=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed3)
                        bet = int(bet)
                        dbhandler.win(ctx,bet)
                    elif wheel1 == "🍇" and wheel2 == "🍇" and wheel3 == "🍇":
                        bet = bet*4
                        bet = str(bet)
                        embed4=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed4)
                        bet = int(bet)
                        dbhandler.win(ctx,bet)
                    elif wheel1 == "🍇" and wheel2 == "🍇" and wheel3 == "🍫":
                        bet = bet*4
                        bet = str(bet)
                        embed5=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed5)
                        bet = int(bet)
                        dbhandler.win(ctx,bet)
                    elif wheel1 == "🍊" and wheel2 == "🍊" and wheel3 == "🍊":
                        bet = bet*3
                        bet = str(bet)
                        embed6=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed6)
                        bet = int(bet)
                        dbhandler.win(ctx,bet)
                    elif wheel1 == "🍊" and wheel2 == "🍊" and wheel3 == "🍫":
                        bet = bet*3
                        bet = str(bet)
                        embed7=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed7)
                        bet = int(bet)
                        dbhandler.win(ctx,bet)
                    elif wheel1 == "🍒" and wheel2 == "🍒" and wheel3 == "🍒":
                        bet = bet*2
                        bet = str(bet)
                        embed8=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed8)
                        bet = int(bet)
                        dbhandler.win(ctx,bet)
                    elif wheel1 == "🍒" and wheel2 == "🍒":
                        bet = bet*2
                        bet = str(bet)
                        embed9=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed9)
                        bet = int(bet)
                        dbhandler.win(ctx,bet)
                    elif wheel1 == "🍒" and wheel3 == "🍒":
                        bet = bet*2
                        bet = str(bet)
                        embed10=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed10)
                        bet = int(bet)
                        dbhandler.win(ctx,bet)
                    elif wheel2 == "🍒" and wheel3 == "🍒":
                        bet = bet*2
                        bet = str(bet)
                        embed11=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou win!! - "+bet+"<:coin:456086215909965825>",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed11)
                        bet = int(bet)
                        dbhandler.win(ctx,bet)
                    elif wheel1 == "🍒" and wheel2 != "🍒" and wheel3 != "🍒" or wheel2 == "🍒" and wheel1 != "🍒" and wheel3 != "🍒" or wheel3 == "🍒" and wheel2 != "🍒" and wheel1 != "🍒" :
                        bet = str(bet)
                        embed12=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou get your "+bet+"<:coin:456086215909965825> back!",colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed12)
                        bet = int(bet)
                    else:
                        bet = str(bet)
                        embed13=discord.Embed(title="Slot Machine | "+ctx.message.author.display_name,description="Your machine has spun :\n\n"+wheel1+" - "+wheel2+" - "+wheel3+"\n\nYou lose!! - "+bet+"<:coin:456086215909965825>" ,colour=0xFF0000)
                        await bot.edit_message(message=message,embed=embed13)
                        bet = int(bet)
                        dbhandler.lose(ctx,bet)
            
                else:
                    await bot.say(ctx.message.author.display_name+", You need to input an amount of 1 or more!")
            else:
                bet=str(bet)
                await bot.say(ctx.message.author.display_name+", You dont have "+bet+"<:coin:456086215909965825>!!")
        else:
            await bot.say(ctx.message.author.display_name+", You need to input an amount to bet!")
    else:
        await bot.say(ctx.message.author.display_name+", This is a VIP command! You can buy VIP for 1000<:coin:456086215909965825>")


       
@bot.command()
async def logs():
    await bot.say("**EXPOSED**") #done
       
@bot.command()
async def lit():
    await bot.say(":fire::penguin: **PINGU** :penguin::fire:") #done

       
@bot.command()
async def date():
    await bot.say(datetime.date.today())
       
@bot.command(aliases=["cheat","broken"])
async def mug():
    await bot.say(":coffee: <@379303619545137152> :coffee:") #done
       
       
@bot.command(aliases=["furry"])
async def yiff():
    await bot.say("<@290866940258418688>") #done
       
       
@bot.command()
async def status():
    await bot.say(":white_check_mark: Bot Online :white_check_mark:") #done
           

@bot.command(pass_context=True)
async def creator(ctx):
    if ctx.message.author.id == "379303619545137152":
        await bot.say("Hello Royal :)")
    else:
        await bot.say("Hmmmm, you're not Royal -_-")



#roles = [role.name for role in member.roles[1:]] - Use for later reference. (Shows all roles)

@bot.command(pass_context=True)
async def profile(ctx,*,member:discord.Member=None):
	if member == None:
		member = ctx.message.author
	toprole = member.top_role
	embed=discord.Embed(title = member.name , description="Top role of : **"+str(toprole)+"**\n\nJoined discord at : "+str(member.created_at)[:10]+"\nJoined this server at : "+str(member.joined_at)[:10]+"\nCurrently playing : "+str(member.game)+"\nCurrent status : "+str(member.status)+"\n\n**Balance :** " +dbhandler.whoisbalance(member), colour = 0xFF0000)
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_image(url = str(dbhandler.whoislevel(member)))
	embed.set_footer(text="Requested by : "+ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
	await bot.say(embed=embed)
       
@bot.command(pass_context=True)
async def avatar(ctx,*,member:discord.Member=None):
	if member == None:
		member = ctx.message.author
	embed=discord.Embed(title="Avatar of "+member.display_name,description=None,colour=0xFF0000)
	embed.set_image(url = member.avatar_url)
	embed.set_footer(text="Requested by : "+ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
	await bot.send_message(ctx.message.channel,embed=embed)


    
       
_rps=["rock","paper","scissors"]
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(pass_context=True)
async def rps(ctx,bet=None,*,choice):
    if bet != None and int(bet) >= 1:
        if dbhandler.checkforbet(ctx,bet) == True:
            if ctx.message.channel.id == "455856117516337179":
                botchoice=random.choice(_rps)
                if choice.lower() == botchoice.lower():
                    await bot.say("Draw! I chose "+str(botchoice)+". You get your money back!")
                elif choice.lower() == "rock" and botchoice == "scissors":
                    await bot.say("You win "+str(bet)+"<:coin:456086215909965825>! I chose scissors")
                    dbhandler.win(ctx,bet)
                elif choice.lower() == "scissors" and botchoice == "paper":
                    await bot.say("You win "+str(bet)+"<:coin:456086215909965825>! I chose paper")
                    dbhandler.win(ctx,bet)
                elif choice.lower() == "paper" and botchoice == "rock":
                    await bot.say("You win "+str(bet)+"<:coin:456086215909965825>! I chose rock")
                    dbhandler.win(ctx,bet)
                elif choice.lower() == "rock" and botchoice == "paper":
                    await bot.say("You lose "+str(bet)+"<:coin:456086215909965825>! I chose paper")
                    dbhandler.lose(ctx,bet)
                elif choice.lower() == "scissors" and botchoice == "rock":
                    await bot.say("You lose "+str(bet)+"<:coin:456086215909965825>! I chose rock")
                    dbhandler.lose(ctx,bet)
                elif choice.lower() == "paper" and botchoice == "scissors":
                    await bot.say("You lose "+str(bet)+"<:coin:456086215909965825>! I chose scissors")
                    dbhandler.lose(ctx,bet)
                elif choice.lower() != "rock" or "paper" or "scissors":
                    await bot.say("Thats not a choice!")
                else:
                    await bot.say("You need to make a choice to play!")
            else:
                userID = ctx.message.author.id
                await bot.delete_message(ctx.message)
                await bot.say(" Hey <@%s> You need to be in <#455856117516337179> to use -rps !" % (userID))
        else:
            await bot.say("You do not have enough coins to do this command! You need at least "+bet+"<:coin:456086215909965825>")
    else:
        await bot.say("You need to input an amount to bet (1 or more)!")
    
_rtd=["1","2","3", "4", "5", "6"]
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(pass_context=True)
async def rtd(ctx,bet=None):
    if bet != None and int(bet) >= 1:
        if dbhandler.checkforbet(ctx,bet) == True:
            if ctx.message.channel.id == "455856117516337179":
                botchoice=random.choice(_rtd)
                if int(botchoice) < 5:
                    await bot.say("Unlucky you rolled a "+str(botchoice)+". You lose "+bet+"<:coin:456086215909965825>")
                    dbhandler.lose(ctx,bet)
                else:
                    await bot.say("Well done. You rolled a "+str(botchoice)+". You win "+bet+"<:coin:456086215909965825>")
                    dbhandler.win(ctx,bet)
            else:
                userID = ctx.message.author.id
                await bot.delete_message(ctx.message)
                await bot.say(" Hey <@%s> You need to be in <#455856117516337179> to use -rtd !" % (userID))
        else:
            await bot.say("You do not have enough coins to do this command! You need at least "+bet+"<:coin:456086215909965825>")
    else:
        await bot.say("You need to input an amount to bet (1 or more)!")
   
   
_coin=["Heads!","Tails!"]
@bot.command()
async def flip():
    await bot.say(random.choice(_coin))
       
_8balllist = ["It is certain :8ball:","It is decidedly so :8ball:","Without a doubt :8ball:","You may rely on it :8ball:","As I see it, yes :8ball:","Most likely :8ball:","Outlook good :8ball:","Yes :8ball:","Signs point to yes :8ball:","Reply hazy try again :8ball:","Ask again later :8ball:","Better not tell you now :8ball:","Cannot predict now :8ball:","Concentrate and ask again :8ball:","Don't count on it :8ball:","My reply is no :8ball:","My sources say no :8ball:","Outlook not so good :8ball:","Very doubtful :8ball:", "Consider it a pass :8ball:", "It may happen to be true :8ball:", "It appears to be false :8ball:", "Go for it :8ball:", "Thats a small secret :8ball:", "Oh sorry I wasn't paying attention :c :8ball:", "You can bet it will be true :8ball:", "Definite yes :8ball:", "Don't count on that too much :8ball:"]
       
@bot.command(name="8ball",pass_context=True)
async def _8ball(ctx):
    if ctx.message.channel.id == "455856117516337179":
        await bot.say(random.choice(_8balllist))
    else:
        userID = ctx.message.author.id
        await bot.delete_message(ctx.message)
        await bot.say(" Hey <@%s> You need to be in <#455856117516337179> to use -8ball !" % (userID))
       
_roulette = ["-cc take 100 <@%s>","-cc take 100 <@%s>","-cc take 100 <@%s>","-cc take 100 <@%s>","-cc take 100 <@%s>","-cc give 100 <@%s>"]
@commands.has_role("Management")
@bot.command(pass_context=True)
async def roulette(ctx):
    if ctx.message.channel.id == "455856117516337179":
        userID = ctx.message.author.id
        await bot.say(random.choice(_roulette) % (userID))
    else:
        userID = ctx.message.author.id
        await bot.delete_message(ctx.message)
        await bot.say("Hey <@%s> You need to be in <#455856117516337179> to use -roulette !" % (userID))
           
   
_guessnum = ["1","2","3","4","5","6","7","8","9","10"]
@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command(pass_context=True)
async def guess(ctx,user_guess=None):
    if user_guess != None:
        userID = ctx.message.author.id
        num = random.choice(_guessnum)
        if user_guess == num:
            await bot.add_reaction(message = ctx.message, emoji = "✅")
            bet = 100
            dbhandler.win(ctx,bet)
        elif not user_guess in _guessnum:
            await bot.say("You have to choose a whole number between 1 and 10!")
        else:
            await bot.add_reaction(message = ctx.message, emoji = "❌")
    else:
        await bot.say(ctx.message.author.display_name," You need to give a number!")
    
@bot.command(pass_context=True)
async def leave(ctx):
    if ctx.message.author.id == "379303619545137152":
        await bot.leave_server(ctx.message.server)
    else:
        await bot.say("Nice try :P You need to be the creator of the bot")
       
_coin=["HEADS","TAILS"]
@bot.command(pass_context=True)
async def coinflip(ctx,bet=None,*,guess):
    if bet != None and int(bet) >=1:
        if dbhandler.checkforbet(ctx,bet) == True:
            if ctx.message.channel.id == "455856117516337179":
                if guess.upper() in _coin:
                    embed=discord.Embed(title="Coinflip! | "+ctx.message.author.display_name,description="Flipping coin....",colour=0xFF0000)
                    message = await bot.say(embed=embed)
                    embed2=discord.Embed(title="Coinflip! | "+ctx.message.author.display_name,description="3",colour=0xFF0000)
                    await asyncio.sleep(1)
                    await bot.edit_message(message=message,embed=embed2)
                    embed3=discord.Embed(title="Coinflip! | "+ctx.message.author.display_name,description="2",colour=0xFF0000)
                    await asyncio.sleep(1)
                    await bot.edit_message(message=message,embed=embed3)
                    embed4=discord.Embed(title="Coinflip! | "+ctx.message.author.display_name,description="1",colour=0xFF0000)
                    await asyncio.sleep(1)
                    await bot.edit_message(message=message,embed=embed4)
                    await asyncio.sleep(1)
                    flippedcoin=random.choice(_coin)
                    if guess.upper() == flippedcoin:
                        embedwin=discord.Embed(title="Coinflip! | "+ctx.message.author.display_name,description=ctx.message.author.display_name+", You win!",colour=0xFF0000)
                        if guess.upper() == "HEADS":
                            embedwin.set_thumbnail(url = "https://cdn.discordapp.com/attachments/426305280955908096/444466474095083521/coinheads_1.png")
                        if guess.upper() == "TAILS":
                            embedwin.set_thumbnail(url = "https://cdn.discordapp.com/attachments/426305280955908096/444466434425225237/cointails_1.png")
                        await bot.edit_message(message=message,embed=embedwin)
                        dbhandler.win(ctx,bet)
                    else:
                        embedlose=discord.Embed(title="Coinflip! | "+ctx.message.author.display_name,description=ctx.message.author.display_name+", You lose!",colour=0xFF0000)
                        if guess.upper() == "TAILS":
                            embedlose.set_thumbnail(url = "https://cdn.discordapp.com/attachments/426305280955908096/444466474095083521/coinheads_1.png")
                        if guess.upper() == "HEADS":
                            embedlose.set_thumbnail(url = "https://cdn.discordapp.com/attachments/426305280955908096/444466434425225237/cointails_1.png")
                        await bot.edit_message(message=message,embed=embedlose)
                        dbhandler.lose(ctx,bet)
                else:
                    await bot.say("You need to pick either heads or tails!")
            else:
                userID = ctx.message.author.id
                await bot.delete_message(ctx.message)
                await bot.say(" Hey <@%s> You need to be in <#455856117516337179> to use -coinflip !" % (userID))
        else:
            await bot.say("You do not have enough coins to do this command! You need at least "+bet+"<:coin:456086215909965825>")
    else:
        await bot.say("You need to input an amount to bet (1 or more)!")
    
# weird anime shit
       
       
_hug = ["http://i.imgur.com/GNUeLdo.gif","https://78.media.tumblr.com/5dfb67d0a674fe5f81950478f5b2d4ed/tumblr_ofd4e2h8O81ub9qlao1_500.gif","https://media.giphy.com/media/CZpro4AZHs436/giphy.gif","https://media.giphy.com/media/KmhVufFZI3sjK/giphy.gif","https://media.giphy.com/media/DjczAlIcyK1Co/giphy.gif","https://media.tenor.co/images/c32141ae982029beaf8db8d4ddf057bd/tenor.gif","https://media.tenor.co/images/e07a54a316ea6581329a7ccba23aea2f/tenor.gif","https://78.media.tumblr.com/0c7d89426f307c2a9849d001acc2ca2c/tumblr_mztjicy5hL1t93vu5o1_250.gif", "https://m.popkey.co/fca5d5/bXDgV.gif", "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif", "https://zboudrie.files.wordpress.com/2017/12/original.gif", "https://i.pinimg.com/originals/91/b2/90/91b2902a70cdb0f76ee5a384120a6e8b.gif", "http://files.57gif.com/webgif/0/d/2b/8eed07f607952531ef2cc5dbff22a.gif", "https://media.giphy.com/media/s4bQmUtduPako/giphy.gif"]
@bot.command(pass_context=True)
async def hug(ctx):
    chars = '0123456789ABCDEF'
    mentions = [member.display_name for member in ctx.message.mentions]
    embed=discord.Embed(title=str(ctx.message.author.name) + " hugs " + ' and '.join(mentions) ,description=None, color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_hug))
    await bot.say(embed=embed)
       
_slap = ["http://i.imgur.com/Ksy8dvd.gif","http://i.imgur.com/d9thUdx.gif","http://i.imgur.com/q7AmR8n.gif","http://i.imgur.com/rk8eqnt.gif", "https://media.giphy.com/media/AkKEOnHxc4IU0/giphy.gif", "https://i.pinimg.com/originals/46/b0/a2/46b0a213e3ea1a9c6fcc060af6843a0e.gif", "https://i.pinimg.com/originals/b1/3a/42/b13a42abbcccbf8470bb4617c51bc080.gif", "https://media.giphy.com/media/zRlGxKCCkatIQ/giphy.gif","http://i0.kym-cdn.com/photos/images/original/001/264/655/379.gif", "https://m.popkey.co/3913ae/OoGdQ_s-200x150.gif", "http://gifimage.net/wp-content/uploads/2017/07/anime-slap-gif-19.gif", "http://gifimage.net/wp-content/uploads/2017/07/anime-slap-gif-20.gif", "http://all.your-base.org/Images/slap.gif"]
@bot.command(pass_context=True)
async def slap(ctx):
    chars = '0123456789ABCDEF'
    mentions = [member.display_name for member in ctx.message.mentions]
    embed=discord.Embed(title= str(ctx.message.author.name) + " slaps " + ' and '.join(mentions)   , description=None, color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_slap))
    await bot.say(embed=embed)
       
_kiss = ["http://i.imgur.com/wx3WXZu.gif","http://i.imgur.com/p6hNamc.gif","http://i.imgur.com/lZ7gAES.gif","http://i.imgur.com/LBWIJpu.gif", "https://media.giphy.com/media/flmwfIpFVrSKI/giphy.gif", "http://pa1.narvii.com/6248/2d96dcde51edeb7c91f194c71e7a15dddc367e13_00.gif", "https://data.whicdn.com/images/158696295/original.gif", "https://media3.giphy.com/media/bGm9FuBCGg4SY/200.gif", "https://media.giphy.com/media/n3lZJyYNbG7aU/giphy.gif", "https://myanimelist.cdn-dena.com/s/common/uploaded_files/1483589430-f951b924a6fd5f59434ad3c63fc6960c.gif", "https://i.pinimg.com/originals/44/16/a8/4416a853b05bb16e88e163286a7950ac.gif", "http://i0.kym-cdn.com/photos/images/original/001/108/304/adf.gif", "https://orig00.deviantart.net/690c/f/2015/251/8/3/kiss_gif_animation_by_psyclopathe-d96tmbk.gif"]
@bot.command(pass_context=True)
async def kiss(ctx):
    chars = '0123456789ABCDEF'
    mentions = [member.display_name for member in ctx.message.mentions]
    embed=discord.Embed(title=str(ctx.message.author.name) + " kisses " + ' and '.join(mentions)   , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_kiss))
    await bot.say(embed=embed)
       
_pat =["http://i.imgur.com/qL5SShC.gif","http://i.imgur.com/1d9y1s1.gif","http://i.imgur.com/HiKI49x.gif", "https://m.popkey.co/a5cfaf/1x6lW.gif", "http://gifimage.net/wp-content/uploads/2017/09/anime-head-pat-gif-4.gif", "http://gifimage.net/wp-content/uploads/2017/09/anime-pat-gif-4.gif", "https://media.giphy.com/media/K1InqndmlQDE4/giphy.gif", "https://i.makeagif.com/media/7-25-2014/yprfox.gif"]
@bot.command(pass_context=True)
async def pat(ctx):
    chars = '0123456789ABCDEF'
    mentions = [member.display_name for member in ctx.message.mentions]
    embed=discord.Embed(title=str(ctx.message.author.name) + " pats " +  ' and '.join(mentions)   , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_pat))
    await bot.say(embed=embed)
       
_cuddle =["http://i.imgur.com/8kLQ55E.gif","http://i.imgur.com/K4lYduH.gif","http://i.imgur.com/Asnv32U.gif","http://i.imgur.com/xWTyaKY.gif", "https://m.popkey.co/2d36e4/RXVj3.gif", "https://thumbs.gfycat.com/JealousFlakyArabianwildcat-max-1mb.gif", "http://i0.kym-cdn.com/photos/images/newsfeed/000/883/447/e26.gif", "http://i0.kym-cdn.com/photos/images/original/001/094/799/80e.gif"]
@bot.command(pass_context=True)
async def cuddle(ctx):
    chars = '0123456789ABCDEF'
    mentions = [member.display_name for member in ctx.message.mentions]
    embed=discord.Embed(title=str(ctx.message.author.name) + " cuddles with " + ' and '.join(mentions) , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_cuddle))
    await bot.say(embed=embed)
           
_bite =["http://gifimage.net/wp-content/uploads/2017/09/anime-bite-gif.gif","http://gifimage.net/wp-content/uploads/2017/09/anime-bite-gif-4.gif","http://i0.kym-cdn.com/photos/images/original/000/783/193/dc2.gif", "http://gifimage.net/wp-content/uploads/2017/09/anime-bite-gif-10.gif", "https://media.giphy.com/media/Qisbk5TesHmjC/giphy.gif", "http://gifimage.net/wp-content/uploads/2017/09/anime-bite-gif-1.gif", "https://i.pinimg.com/originals/ca/eb/32/caeb32ef58807c7563460d96a3f7ecc9.gif", "http://i0.kym-cdn.com/photos/images/newsfeed/000/783/193/dc2.gif"]
@bot.command(pass_context=True)
async def bite(ctx):
    chars = '0123456789ABCDEF'
    mentions = [member.display_name for member in ctx.message.mentions]
    embed=discord.Embed(title=str(ctx.message.author.name) + " bites " + ' and '.join(mentions) , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_bite))
    await bot.say(embed=embed)
_pout =["http://i.imgur.com/sVwdeGn.gif","http://gifimage.net/wp-content/uploads/2017/09/anime-pout-gif-2.gif", "https://thumbs.gfycat.com/ForkedKaleidoscopicCollie-size_restricted.gif", "https://media.giphy.com/media/1Qxk6iux4MVRC/giphy.gif"]
@bot.command(pass_context=True)
async def pout(ctx):
    chars = '0123456789ABCDEF'
    embed=discord.Embed(title=str(ctx.message.author.name) + " pouts" , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_pout))
    await bot.say(embed=embed)
       
_lick=["https://i.imgur.com/QDpVqHe.gif","https://media.giphy.com/media/12MEJ2ArZc23cY/source.gif", "https://m.popkey.co/0565e9/bgq1Y.gif", "http://i0.kym-cdn.com/photos/images/original/001/093/355/909.gif", "http://i0.kym-cdn.com/photos/images/original/000/995/417/60f.gif",]
@bot.command(pass_context=True)
async def lick(ctx):
    if ctx.message.channel.id == "430119885830488067":
        chars = '0123456789ABCDEF'
        mentions = [member.display_name for member in ctx.message.mentions]
        embed=discord.Embed(title=str(ctx.message.author.name) + " licks " + ' and '.join(mentions) , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
        embed.set_image(url = random.choice(_lick))
        await bot.say(embed=embed)
    else:
        await bot.delete_message(ctx.message)
        await bot.say("Wrong channel! Keep it to RP chat")
      
_cry=["https://i.imgur.com/h2sI4qi.gif","https://i.imgur.com/tBMI0nb.gif", "http://gifimage.net/wp-content/uploads/2017/07/anime-cry-gif-18.gif", "https://media.giphy.com/media/qmHGZWQERIEms/giphy.gif",]
@bot.command(pass_context=True)
async def cry(ctx):
    chars = '0123456789ABCDEF'
    embed=discord.Embed(title=str(ctx.message.author.name) + " cries "  , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_cry))
    await bot.say(embed=embed)
      
_smile=["https://i.imgur.com/KGL3lzh.gif","http://i.imgur.com/Y5o48VW.gif","https://thumbs.gfycat.com/InsistentUnnaturalEmu-size_restricted.gif", "https://uploads.disquscdn.com/images/f975bdb1f9ec57621440825425deafd18733d2417cb8f7e0ef4f4c74c78845bb.gif"]
@bot.command(pass_context=True)
async def smile(ctx):
    chars = '0123456789ABCDEF'
    embed=discord.Embed(title=str(ctx.message.author.name) + " smiles "  , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_smile))
    await bot.say(embed=embed)
      
_wave=["http://cdn.ebaumsworld.com/mediaFiles/picture/2192630/83801651.gif","http://i0.kym-cdn.com/photos/images/newsfeed/001/073/005/67f.gif", "https://media.tenor.com/images/250fc8aacb8c89b4b3b8a0384a3df4ea/tenor.gif", "http://gifimage.net/wp-content/uploads/2017/09/anime-wave-gif-11.gif", "https://media.tenor.com/images/830580b86b274e3bf62db4654c635cd3/tenor.gif", "http://gifimage.net/wp-content/uploads/2017/09/anime-wave-gif-4.gif", "https://media.giphy.com/media/qDsa4saXAdQ52/giphy.gif", "http://gifimage.net/wp-content/uploads/2017/09/anime-wave-gif-14.gif", "https://joseinextdoor.files.wordpress.com/2016/04/rei-wave.gif"]
@bot.command(pass_context=True)
async def wave(ctx):
    chars = '0123456789ABCDEF'
    embed=discord.Embed(title=str(ctx.message.author.name) + " waves "  , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_wave))
    await bot.say(embed=embed)
      
_highfive=["https://data.whicdn.com/images/51297205/original.gif","https://68.media.tumblr.com/3d40ebd02c9a3eb87876665f23d9edb7/tumblr_mwd4cmTzLu1rp073lo1_400.gif", "http://gifimage.net/wp-content/uploads/2017/09/anime-high-five-gif.gif", "http://i0.kym-cdn.com/photos/images/original/001/126/190/908.gif", "http://gifimage.net/wp-content/uploads/2017/09/anime-high-five-gif-8.gif"]
@bot.command(pass_context=True)
async def highfive(ctx):
    chars = '0123456789ABCDEF'
    mentions = [member.display_name for member in ctx.message.mentions]
    embed=discord.Embed(title=str(ctx.message.author.name) + " high fives " + ' and '.join(mentions) , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_highfive))
    await bot.say(embed=embed)

_poke=[""]
@bot.command(pass_context=True)
async def poke(ctx):
    chars = '0123456789ABCDEF'
    mentions = [member.display_name for member in ctx.message.mentions]
    embed=discord.Embed(title=str(ctx.message.author.name) + " pokes " + ' and '.join(mentions) , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_poke))
    await bot.say(embed=embed)

_meme=["https://media0dk-a.akamaihd.net/51/16/a09091e279253d4a37e66c70a2ea4220.jpg","https://sayingimages.com/wp-content/uploads/not-wanting-to-leave-the-house-anime-meme.jpg", "https://data.whicdn.com/images/308759712/superthumb.jpg", "https://sayingimages.com/wp-content/uploads/how-chocolate-immediately-melt-anime-meme.jpg", "data:image/jpeg;base64,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", "https://media0dk-a.akamaihd.net/87/59/0ca2aa85b88f8b156dc78fa8702a4c6c.jpg", "https://pm1.narvii.com/6290/38f5b4dd583fff21f7a9bf61be6de8033d3ac0e0_hq.jpg", "https://pa1.narvii.com/6335/9f5da63d25618d59fdf4531b13549233826392b4_hq.gif", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf0Mya8sdt5_NPMDQ5B8FdMU5jZzGPVOUq43FdmB6sdW3Qn2jC", "https://quoteshumor.com/wp-content/uploads/2017/06/29-Anime-Memes-20-anime-Memes-500x676.jpg", "http://animememes.co/wp-content/uploads/2017/11/best-naruto-memes-in-animememes-25.jpg", "http://quotes.girlstalkinsmack.com/wp-content/uploads/2016/07/Top-25-Anime-Memes-13-Anime-Funny.jpg", "https://fthmb.tqn.com/Skr8mT6ilYOuT_miRs0ncItT95Q=/768x0/filters:no_upscale():max_bytes(150000):strip_icc()/FairyTailMeme04-56a014a65f9b58eba4aed6fd.jpg", "http://media.comicbook.com/2017/05/anime-meme-a6b-993895.jpg"]
@bot.command(pass_context=True)
async def meme(ctx):
    chars = '0123456789ABCDEF'
    embed=discord.Embed(title=str(ctx.message.author.name) + " you got it  "  , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_meme))
    await bot.say(embed=embed)
      
_gif=["https://media0.giphy.com/media/4QxQgWZHbeYwM/giphy.gif", "https://img.gifmagazine.net/gifmagazine/images/701770/original.gif", "https://media.giphy.com/media/FtOjlaGBsdL8s/giphy.gif", "https://pa1.narvii.com/6269/b09d0ed3fb501af041587e8cea02d7f0d2480ca6_hq.gif", "http://goboiano.com/wp-content/uploads/2017/03/tumblr_oljobeNiUe1ufw8o4o1_500.gif", "https://weneedfun.com/wp-content/uploads/2017/06/Cute-Anime-Gifs-14.gif", "https://i.pinimg.com/originals/71/61/db/7161db656ac1eb8681cb73b8d4ea4755.gif", "https://i.pinimg.com/originals/63/ae/66/63ae66c7409a0427d4e0351601b4cdef.gif", "http://goboiano.com/wp-content/uploads/2017/03/tumblr_o1oajjgWtw1ufw8o4o1_500.gif", "http://1.media.dorkly.cvcdn.com/74/42/b73f69bc94b9d8df8928cee0ab151c01.gif", "https://i.kinja-img.com/gawker-media/image/upload/t_original/zud8inrzlx54hfpesbuy.gif", "https://data.whicdn.com/images/292280739/original.gif", "http://pa1.narvii.com/5830/8e0ccb82d032c8410a861cfc610fb20df2c5572d_hq.gif", "http://goboiano.com/wp-content/uploads/2017/03/tumblr_ok3zl3GjUJ1ufw8o4o1_500.gif", "https://media0dk-a.akamaihd.net/44/99/916f1eb9735b6b70784ca79889e07208.gif"]
@bot.command(pass_context=True)
async def gif(ctx):
    chars = '0123456789ABCDEF'
    embed=discord.Embed(title=str(ctx.message.author.name) + "  you got it  "  , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    embed.set_image(url = random.choice(_gif))
    await bot.say(embed=embed)

#nsfw------------------------------------------------------

_mount=[""]
@bot.command(pass_context=True)
async def mount(ctx):
	if ctx.message.channel.id == "414641280610598922":
		chars = '0123456789ABCDEF'
		mentions = [member.display_name for member in ctx.message.mentions]
		embed=discord.Embed(title=str(ctx.message.author.name) + " mounts " + ' and '.join(mentions) , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
		embed.set_image(url = random.choice(_mount))
		await bot.say(embed=embed)
	else:
		await bot.add_reaction(message = ctx.message, emoji = "🚫")
		

_69=[""]
@bot.command(name="69",pass_context=True)
async def __69(ctx):
	if ctx.message.channel.id == "414641280610598922":
		chars = '0123456789ABCDEF'
		mentions = [member.display_name for member in ctx.message.mentions]
		embed=discord.Embed(title=str(ctx.message.author.name) + " has 69 with " + ' and '.join(mentions) , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
		embed.set_image(url = random.choice(_69))
		await bot.say(embed=embed)
	else:
		await bot.add_reaction(message = ctx.message, emoji = "🚫")

_spank=[""]
@bot.command(pass_context=True)
async def spank(ctx):
	if ctx.message.channel.id == "414641280610598922":
		chars = '0123456789ABCDEF'
		mentions = [member.display_name for member in ctx.message.mentions]
		embed=discord.Embed(title=str(ctx.message.author.name) + " spanks " + ' and '.join(mentions) , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
		embed.set_image(url = random.choice(_spank))
		await bot.say(embed=embed)
	else:
		await bot.add_reaction(message = ctx.message, emoji = "🚫")

_fuck=[""]
@bot.command(pass_context=True)
async def fuck(ctx):
	if ctx.message.channel.id == "414641280610598922":
		chars = '0123456789ABCDEF'
		mentions = [member.display_name for member in ctx.message.mentions]
		embed=discord.Embed(title=str(ctx.message.author.name) + " fucks " + ' and '.join(mentions) , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
		embed.set_image(url = random.choice(_fuck))
		await bot.say(embed=embed)
	else:
		await bot.add_reaction(message = ctx.message, emoji = "🚫")

_tieup=[""]
@bot.command(pass_context=True)
async def tieup(ctx):
	if ctx.message.channel.id == "414641280610598922":
		chars = '0123456789ABCDEF'
		mentions = [member.display_name for member in ctx.message.mentions]
		embed=discord.Embed(title=str(ctx.message.author.name) + " ties up " + ' and '.join(mentions) , description=None , color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
		embed.set_image(url = random.choice(_tieup))
		await bot.say(embed=embed)
	else:
		await bot.add_reaction(message = ctx.message, emoji = "🚫")
       
@bot.command()
async def uptime():
    await bot.say("`" + str(datetime.datetime.now() - t) + "`" + " uptime!")
           
       
@bot.command(pass_context=True)
async def ping(ctx):
    chars = '0123456789ABCDEF'
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await bot.send_typing(channel)
    t2 = time.perf_counter()
    embed=discord.Embed(title=None, description='Ping: {}ms'.format(round(((t2-t1)*1000)-100)), color = discord.Colour(int('0x'+''.join(sample(chars,6)),16)))
    await bot.say(embed=embed)
       
#Admin commands below-----------------------------------------------------------------------------------------------
       
@bot.command(pass_context=True)
async def admin(ctx):
    if "manager" in [y.name.lower() for y in ctx.message.author.roles]:
        await bot.add_reaction(ctx.message,"✅")
        embed=discord.Embed(title="Staff Commands:", description="1. mute [member] - To mute a member \n2. unmute [muted member] - To unmute a muted member \n3. warn [member] [reason] - Warn a member", color = 0xFF0000)
        await bot.send_message(ctx.message.author,embed=embed)
        if "manager" in [y.name.lower() for y in ctx.message.author.roles]:
            embed=discord.Embed(title="Admin Commands:", description="1. kick [member] - Kicks a member \n2. ban [member] [reason] - Bans a member", color = 0xFF0000)
            await bot.send_message(ctx.message.author,embed=embed)
            if "manager" in [y.name.lower() for y in ctx.message.author.roles]:
                embed=discord.Embed(title="Manager Commands:", description="1. purge [x] - Deletes select amount of messages \n2. say [X] - Makes the bot say something", color = 0xFF0000)
                await bot.send_message(ctx.message.author,embed=embed)
    else:
        await bot.add_reaction(ctx.message,"❌")
        await bot.say("Sorry <@"+str(ctx.message.author.id)+">, you are not an admin.")
       
       
@commands.has_role("Manager")
@bot.command(pass_context=True)
async def purge(ctx,num: int):
    await bot.purge_from(ctx.message.channel,limit=num)
       
@commands.has_role("Manager")
@bot.command()
async def kick(member:discord.Member):
    await bot.kick(member)
           
@commands.has_role("Manager")
@bot.command(pass_context=True)
async def ban(ctx,member:discord.Member,*,message):
    await bot.say('<@{}>, has been banned.'.format(member.id))
    await asyncio.sleep(1)
    await bot.send_message(member,"You have been banned for the following reason : `" + str(message) + "`")
    await bot.send_message(ctx.message.server.get_channel("455859161679265792"), str(ctx.message.author) + " banned " + str(member) + " for the reason : `" + str(message) + "`")
    await bot.ban(member)
       
@commands.has_role("Manager")
@bot.command(pass_context=True)
async def mute(ctx,member:discord.Member):
    await bot.say('<@{}>, you have been muted'.format(member.id))
    await asyncio.sleep(1)
    await bot.add_roles(member,discord.utils.get(ctx.message.server.roles, name="Muted"))
       
@commands.has_role("Manager")
@bot.command(pass_context=True)
async def warn(ctx,user:discord.Member,*,message):
    await bot.send_message(user,"You have been warned for the following reason : `" + str(message) + "`")
    await bot.add_roles(user,discord.utils.get(ctx.message.server.roles, name="Warned"))
    await bot.send_message(ctx.message.server.get_channel("455859161679265792"), str(ctx.message.author) + " warned " + str(user) + " for the reason : `" + str(message) + "`")

       
@commands.has_role("Manager")
@bot.command(pass_context=True)
async def unmute(ctx,member:discord.Member):
    await bot.say('<@{}>, you have been unmuted'.format(member.id))
    await asyncio.sleep(1)
    await bot.remove_roles(member,discord.utils.get(ctx.message.server.roles, name="Muted"))
       
@commands.has_role("Manager")
@bot.command(pass_context=True)
async def say(ctx, *, X):
    await bot.delete_message(ctx.message)
    await bot.say(''+X+'')
       
@bot.command(pass_context=True)
async def pm(ctx):
    await bot.send_message(ctx.message.author, "Hello")
       
       
       
#@bot.command(aliases=['google'])
#async def g(*, query):
#    num_page = 1
#    search_results = google.search(query, num_page)
#    em = discord.Embed(title='Google Search', colour=0xff0000)
#    em.add_field(name=search_results[0].name, value=search_results[0].description)
#    em.add_field(name='Link', value=search_results[0].link)
#    await bot.say(embed=em)
       
       
       
       
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Event Time :P
       
       
chat_filter = ["NIGGER","NIGGA","NIG","NIGG","CHINK","PAKI","NEGRO","NIGNOG","NIG","NOG","COON","GOLLIWOG","GOLLYWOG","FAGGOT","FAGGOTS","FAG","FAGS","FEGGOT","FEGGOTS","FEG","FEGS"]
bypass_list = []
link_bypass = ["Links"]
_random = [1,2,3,4,5,6,7,8,9,10,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,]
 
@bot.event
async def on_message(message,):
    contents = message.content.split(" ")
    for word in contents:
        if word.upper() in chat_filter:
            if not message.author.id in bypass_list:
                try:
                    await bot.delete_message(message)
                    userID = message.author.id
                    await bot.send_message(message.channel, "**Hey!** <@%s> You have just violated rule #6! Shame on you >:(" % (userID))
                except discord.errors.NotFound:
                    return
    if message.content.startswith("https") or message.content.startswith("http"):
        if message.channel.id != "455855974994149406":
            if not "links" in [y.name.lower() for y in message.author.roles]:
                await bot.delete_message(message)
                await bot.send_message(message.server.get_channel("455859161679265792"), "Message deleted because it contained a link. Author was : "+str(message.author.display_name)) 

    mention_match = re.match(r'<@!?(\d+)>', message.content)
    for word in contents:
        if mention_match and mention_match.group(1) == '425957421975076864':
            await bot.add_reaction(message, "\U0001f1f5")
            await bot.add_reaction(message, "\U0001f1ee")
            await bot.add_reaction(message, "\U0001f1f3")
            await bot.add_reaction(message, "\U0001f1ec")
            await bot.add_reaction(message, "\U0001f621")
    if message.author.id != "456048004944625674":
        if message.author.id != "398601531525562369":
            if message.author.id != "170903342199865344":
                if message.author.id != "160105994217586689":
                    if message.author.id != "285480424904327179":
                        if message.author.id != "346702890368368640":
                            if message.author.id != "202930020396564480":
                                if message.author.id != "202930020396564489":
                                    if message.channel.id != "420775325270802452":
                                        dbhandler.addonmessage(message)
                                        dbhandler.xp(message)
                                        randdrop = int(random.choice(_random))
                                        if dbhandler.xpcheck(message) is True:
                                            embed = discord.Embed(title = "Level UP!",description = message.author.display_name,colour=0xFF0000)
                                            embed.set_thumbnail(url = dbhandler.eventlevel(message))
                                            await bot.send_message(message.channel,embed=embed)
                                        elif randdrop == 10:
                                            dbhandler.randomdrop(message)
                                            await bot.send_message(message.channel,message.author.display_name+" has received 100<:coin:456086215909965825> as a random drop!")
    await bot.process_commands(message)
       
    
    
    
    
@bot.event
async def on_message_delete(message):
    if message.author.id != "456048004944625674":
        if message.author.id != "398601531525562369":
            if message.author.id != "170903342199865344":
                if message.author.id != "160105994217586689":
                    if message.author.id != "285480424904327179":
                        if message.author.id != "346702890368368640":
                            if message.author.id != "202930020396564480":
                                if not message.content.startswith("-say"):
                                    if not message.content.startswith("next"):
                                        if not message.content.startswith("hit"):
                                            if not message.content.startswith("stay"):
                                                if not message.content.startswith("-d"):
                                                    fmt = "{0.author.name}'s message has been deleted: \n {0.content} \nFrom the channel : \n #" + str(message.channel.name)
                                                    embed=discord.Embed(title=None, description= fmt.format(message), colour = 0xFF0000)
                                                    await bot.send_message(message.server.get_channel("455886151107084288"), embed=embed)
       
@bot.event
async def on_message_edit(before, after):
    if after.author.id != "456048004944625674":
        if after.author.id != "398601531525562369":
            if after.author.id != "170903342199865344":
                if after.author.id != "160105994217586689":
                    if after.author.id != "285480424904327179":
                        if after.author.id != "346702890368368640":
                            if after.author.id != "202930020396564480":
                                fmt = '**{0.author.name} edited their message from :**\n\n{0.content}\n\n**To:**\n\n{1.content}\n\n**From the channel :**\n\n#' + str(before.channel.name)
                                embed=discord.Embed(title=None,description=fmt.format(before,after),colour = 0xFFB600)
                                await bot.send_message(before.server.get_channel("455886151107084288"), embed=embed)
       
       
@bot.command(pass_context=True)
async def id(ctx):
    await bot.say(str(ctx.message.server.id))
       
@bot.event
async def on_member_join(member):
    if member.server.id == "455851306461167628":
        server = member.server
        fmt = '**Welcome {0.mention} to {1.name}**!'
        await bot.add_roles(member,discord.utils.get(member.server.roles, name="Member"))
        await bot.send_message(bot.get_channel("455851306461167630"), fmt.format(member, server))
       
@bot.event
async def on_member_remove(member):
    if member.server.id == "455851306461167628":
        server = member.server
        fmt = '**{0.display_name} has left {1.name}!**'
        await bot.send_message(bot.get_channel("455851306461167630"), fmt.format(member, server))
 
zkey = "q"
@bot.event
async def on_ready():
	embed=discord.Embed(title="Bot restart",description="✅ All systems good ✅\nTime deployed : "+str(datetime.datetime.utcfromtimestamp(int(time.time())).strftime("`%H:%M:%S UTC` -- `%-d-%b-%Y`")),colour=0xFF0000)
	channel = discord.utils.get(bot.get_all_channels(), server__name="Sesmics friends", name='bot-test')
	await bot.send_message(channel, embed=embed)
	while zkey == "q":
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="with Royalnoob"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="-help"))
		await asyncio.sleep(60)
		await bot.change_presence(game=discord.Game(type=1, name="Same Old, Same Old"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="Wait...What am i playing again?"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="Beep Beep I'm A Sheep"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="Some Anime Stuff"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="For Once, Nothing!"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="Ya Feel Lucky Punk?"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="Royalnoob Sim 2018"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="Lewd 2010"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="Claiming The Nekos"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="Baka Blaster 9000"))
		await asyncio.sleep(30)
		await bot.change_presence(game=discord.Game(type=1, name="RoyalNoob Is A Derp :forsenE:"))
       

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        if error.retry_after <= 59:
            embed=discord.Embed(title="⏳ Cooldown! ⏳",description="The command is on a cooldown of "+str(round(error.retry_after,1))+' seconds!',colour=0xFF0000)
            await bot.send_message(ctx.message.channel, embed=embed)
        if error.retry_after >= 60 and error.retry_after <= 3600:
            embed=discord.Embed(title="⏳ Cooldown! ⏳",description="The command is on a cooldown of "+str(round(error.retry_after/60,1))+' minutes!',colour=0xFF0000)
            await bot.send_message(ctx.message.channel, embed=embed)
        if error.retry_after >= 3601:
            embed=discord.Embed(title="⏳ Cooldown! ⏳",description="The command is on a cooldown of "+str(round(error.retry_after/60**2,1))+' hours!',colour=0xFF0000)
            await bot.send_message(ctx.message.channel, embed=embed)
    raise error
           
token = os.getenv('TOKEN')
bot.run(token)
