import telebot
import config
from secrets import token_urlsafe
token = token_urlsafe(8)

bot = telebot.TeleBot(config.TOKEN)

notify_flag = False
send_flag = False

@bot.message_handler(commands=['start'])
def greeting(msg):
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/ya.png', 'rb')
	bot.send_sticker(msg.chat.id, sticker)
	welcome = "Welcome to Birbs Temple, {0.first_name}!\nI'm <b>{1.first_name}</b>. Enjoy Birbs with me!".format(msg.from_user, bot.get_me())
	bot.send_message(msg.chat.id, welcome, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(msg):
	sticker = open('static/ready.png', 'rb')
	bot.send_sticker(msg.chat.id, sticker)
	help_msg = '''As a professional <b>Birbs world-Human world mediator</b>, I understand plenty of commands.\n
	/start - Welcome message.
	/help - Help menu, you're here.
	/stream - Start video streaming.
	/status - Ask me if any birbs are on duty right now.
	/notify_me - Turn notifications on, so I could inform you if any birbs are present.
	/notify_off - Turn notifications off, so to prevent me from irritating you no more.
	/photo - Ask me to take photo.
	/send_birbs - Ask me to send you nudes, I mean, pictures of birbs the moment I detect them.'''
	bot.send_message(msg.chat.id, help_msg, parse_mode='html')
	help_msg ="\nThat's it! Good luck, {0.first_name}!\n".format(msg.from_user)
	bot.send_message(msg.chat.id, help_msg)
	bot.send_message(msg.chat.id, "\nI'm a busy Bot, I'll hurry to my ebanaya rabota!")
	sticker = open('static/hurry.png', 'rb')
	bot.send_sticker(msg.chat.id, sticker)

@bot.message_handler(commands=['photo'])
def take_photo(msg):
	#take photo
	photo = open('/tmp/photo.png', 'rb')
	bot.send_photo(chat_id, photo)

@bot.message_handler(commands=['notify_me'])
def notify_on(msg):
	global notify_flag
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/yessir.webp', 'rb')
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_sticker(msg.chat.id, sticker)
	notify_flag = True
	bot.send_message(msg.chat.id, "\nNotifications turned on!")

@bot.message_handler(commands=['notify_off'])
def notify_off(msg):
	global notify_flag
	bot.send_chat_action(msg.chat.id, 'typing')
	notify_flag = False
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_message(msg.chat.id, "\nNotifications turned off. You broke my birby heart...")
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/drama.png', 'rb')
	bot.send_sticker(msg.chat.id, sticker)

@bot.message_handler(commands=['send_birbs'])
def send_birbs(msg):
	global send_flag
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/ok.png', 'rb')
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_sticker(msg.chat.id, sticker)
	send_flag = True
	bot.send_message(msg.chat.id, "\nOk, I'll send you photos!")

@bot.message_handler(commands=['stream'])
def stream(msg):
	#stream
	bot.send_chat_action(msg.chat.id, 'find_location')

@bot.message_handler(commands=['status'])
def get_status(msg):
	#get status
	bot.send_chat_action(msg.chat.id, 'typing')

@bot.message_handler(content_types=['text'])
def handle(msg):
	if msg.text == 'birbs':
		bot.send_chat_action(msg.chat.id, 'typing')
		sticker = open('static/kirakira.png', 'rb')
		bot.send_sticker(msg.chat.id, sticker)
		bot.send_chat_action(msg.chat.id, 'typing')
		bot.send_message(msg.chat.id, 'I love birbs too!')
	elif msg.text == 'hello':
		bot.send_chat_action(msg.chat.id, 'typing')
		sticker = open('static/hello.png', 'rb')
		bot.send_chat_action(msg.chat.id, 'typing')
		bot.send_sticker(msg.chat.id, sticker)
		bot.send_chat_action(msg.chat.id, 'typing')
		bot.send_message(msg.chat.id, 'Henlo! Nice to see ya!')
	elif msg.text == 'bye':
		bot.send_chat_action(msg.chat.id, 'typing')
		sticker = open('static/bye.png', 'rb')
		bot.send_sticker(msg.chat.id, sticker)
		bot.send_chat_action(msg.chat.id, 'typing')
		bot.send_message(msg.chat.id, 'See ya again at Birbs Temple!')

bot.polling(none_stop=True)
