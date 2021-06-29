from logging import Logger
import os
from discord import embeds, message
from discord.ext import commands
import discord
from discord.flags import flag_value
from dotenv import load_dotenv
import asyncio
import random

intents = discord.Intents.default()
intents.members = True
intents.presences = True

load_dotenv("env") // env is the file containing the discord bot token
TOKEN = os.getenv('TOKEN')
client=commands.Bot(command_prefix='~',intents=intents)
members=[]
kicked = 0
pm_msg = ["*You were kicked because of your visibility issues\nDo join again, but mind you links are scarce*"
,"*You were kicked because you were caught being invisible\nDo join again, but mind you links are scarce*"
,"*You were kicked because you refused to surrender \nyour crown of invisibility\nDo join again, but mind you links are scarce*"
,"*To be or Not to be Invisible, that is the Question.\nI hope you found your answer.\nDo join again, but mind you links are scarce.*"
,"*Oops! You got kicked .... Sometimes you just gotta be online*"+ r"¯\_(ツ)_/¯" + " \n*Do join again, but mind you links are scarce.*"
,"*I am 99% pro-invisibility, but oh, that 1%... \nDo join again, but mind you links are scarce.*"]
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    member = message.author
    if message.author == client.user:
        return

    if ((str(member.status) == "offline") and ("Club" in str(member.roles))):
        if member not in members:
            members.append(member)         
            await message.channel.send("**{} IS MESSAGING WHILE INVISIBLE**".format(member))
            await count(message , member)
            # await on_typing(channel,member,when)

            if ((str(member.status) == "offline") and ("Club" in str(member.roles))and (member in members)) and (kicked == 0):
                emb = discord.Embed(title=member , description=member.mention , color = discord.Colour.random())
                emb.add_field(name="Reason" , value= "KICKED! DUE TO INVISIBILITY" , inline=False)
                emb.set_thumbnail(url=member.avatar_url)
                emb.add_field(name="Note" , value=random.choice(pm_msg), inline=True)
                await member.create_dm()
                await member.dm_channel.send(embed=emb)    
                await kick(member)
                members.remove(member)
                embed = discord.Embed(title=member , description=member.mention , color = discord.Colour.random())
                embed.add_field(name = "ID" , value = member.id , inline = True)
                embed.add_field(name="Reason" , value= "Dont Be JOHN CENA!" , inline=False)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text="You have been kicked!")
                await message.channel.send(embed=embed)
        
        
        
@client.command()
async def kick(member , reason="Due to invisibility"):
    await member.kick(reason=reason)
    return


@client.command()
async def count(message , member, number=int(60)):
    embed = discord.Embed(title=member , description=member.mention , color = discord.Colour.random())
    embed.add_field(name="Timer" , value= number , inline= True)
    embed.set_thumbnail(url="https://t4.ftcdn.net/jpg/03/31/29/83/360_F_331298353_73gUe2q6b36bwaCv1EDAHxbToOlUYZRV.jpg")
    embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0yF77CyIo4EMYsU1wxIM70D-dJ3kxmNrNfavlXEQN8qrvoPzbCo60YmHz9vAi9skuZno&usqp=CAU")
    msg = await message.channel.send(embed=embed)
    while (number != 0) and (member in members):
        number -= 1
        embed.set_field_at(index=0,name="Timer" , value=number , inline=True)
        await msg.edit(embed=embed)
        await asyncio.sleep(1)
    embed.set_field_at(index=0,name="Timer" , value="Ended!" , inline=True)
    await msg.edit(embed=embed)
    await asyncio.sleep(3) 
    await msg.delete()
    return

@client.event
async def on_typing(channel, user, when):
    #await asyncio.sleep(20)
    if user in members and (str(user.status) == "offline"):
        await asyncio.sleep(25)
        emb = discord.Embed(title=user , description=user.mention , color = discord.Colour.random())
        emb.add_field(name="Reason" , value= "KICKED! DUE TO INVISIBILITY" , inline=False)
        emb.set_thumbnail(url=user.avatar_url)
        emb.add_field(name="Note" , value=random.choice(pm_msg), inline=True)
        await user.create_dm()
        await user.dm_channel.send(embed=emb)    
        await kick(user)
        kicked = 1
        try:
            members.remove(user)
        except:
            pass
        embed = discord.Embed(title=user , description=user.mention , color = discord.Colour.random())
        embed.add_field(name = "ID" , value = user.id , inline = True)
        embed.add_field(name="Reason" , value= "Dont Be JOHN CENA!" , inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text="You have been kicked!")
        await channel.send(embed=embed)
          
client.run(TOKEN)
