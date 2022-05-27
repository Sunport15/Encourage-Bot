from replit import db
import os
import discord
import json
import requests
import random
from keep_alive import keep_alive


client = discord.Client()

sad_words = ["sad","depressed","unhappy","angry","down","can't think","overwhelmed","drowning","miserable","depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there!",
  "You are worth so much more than your fears"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")


  
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements
    
  
@client.event 
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user :
    return
  msg = message.content
  if msg.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  if db["responding"]:
    options = starter_encouragements
  
    if "encouragements" in db.keys():
      for sentence in db["encouragements"]:
        options.append(sentence)
      
      
  
    if any(word in msg for word in sad_words ):
      await message.channel.send(random.choice(options))

  if msg.startswith('!new'):
    encouraging_message = msg.split('!new ',1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("Encouraging message has been added to database")

  if msg.startswith('!del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("!del",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith('!list'):
    encourangements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith('!responding'):
    value = msg.split("!responding ",1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off")
      

keep_alive()
client.run(os.getenv('TOKEN'))


