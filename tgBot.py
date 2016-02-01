import telebot
import random
import json
from telebot import types

# Create the bot with the token

with open('./iron.token') as TOKEN:
  bot = telebot.TeleBot(TOKEN.read())

# Used files

with open('./data/data.json', 'r') as data:
  js = json.load(data)
  start = js['start']

# Used functions

def random_line(afile): # Obtiene una linea aleatoria de un archivo
  line = next(afile)
  for num, aline in enumerate(afile):
    if random.randrange(num + 2): continue
    line = aline
  return line

def listener(messages):
  # When new messages arrive TeleBot will call this function.
  for m in messages:
    if m.content_type == 'text':
      # Prints the sent message to the console
      if m.chat.type == 'private':
        print ("Chat -> " + str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
      else:
        print ("Group -> " + str(m.chat.title) + " [" + str(m.chat.id) + "]: " + m.text)

def is_user_waiting(user, userList):
  for u in userList:
    if user == u:
      return True

  return False

# Listener

bot.set_update_listener(listener)

# User tracing

user_tracing = []

# Keyboards

refranKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
refranKeyboard.add('Otro!', 'Suficiente')

hideBoard = types.ReplyKeyboardHide()

# Commands

commands = { # Used commands
  'start':'Explica de que es este bot',
  'help':'Muestra esta ayuda',
  'lmgtfy':'Let Me Google That For You',
  'refran':'Manda un refran aleatorio'
}

# Mensaje para saber que el bot esta funcionando

print("Running...")

# Handlers de mensajes

@bot.message_handler(commands=['start'])
def send_start(message):
  bot.send_message(message.chat.id, start)

@bot.message_handler(commands=['help'])
def send_help(message):
  help_text = "Puedes usar los siguientes comandos:\n"
  for key in commands:
    help_text += "/" + key + " : " + commands[key] + "\n"

  bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['lmgtfy'])
def send_tldr(message):
  if message.text == '/lmgtfy' or message.text == '/lmgtfy@theIron_bot':
    bot.reply_to(message, "Que quieres que busque?\nEscribe /lmgtfy [BUSQUEDA]")
  else:
    lmgtfy_url = "http://lmgtfy.com/?q=" + "+".join(message.text.split()[1:])
    bot.send_message(message.chat.id, lmgtfy_url)

@bot.message_handler(commands=['refran'])
def send_refran(message):
  with open('./data/refranes.txt') as refranes:
    bot.send_message(message.chat.id, random_line(refranes))

bot.polling()
