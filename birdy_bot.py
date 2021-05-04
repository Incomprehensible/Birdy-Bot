import telebot
import config
from secrets import token_urlsafe
import subprocess
import cv2
import threading
from time import sleep
from birdy_DB import Birdy_DB

token = token_urlsafe(8)

bot = telebot.TeleBot(config.TOKEN)

subcall = subprocess.call

THRESHOLD = 1000
firstFrame = None

DB = Birdy_DB()

notify_chat_ids = []
photo_chat_ids = []
#stream_chat_ids = []

DB.fetch_notify_data(notify_chat_ids)
DB.fetch_photos_data(photo_chat_ids)
#DB.fetch_streams_data(stream_chat_ids)


client_path = "/home/pi/birdy_bot/bot_client"

birb_event = threading.Event()
cam_event = threading.Event()

# MOTION
vidCap = cv2.VideoCapture
cvColor = cv2.cvtColor
cvResize = cv2.resize

def birb_online():
	global firstFrame
	cap = vidCap(-1)
	gray = None
	#firstFrame = None
	while True:
		ret, frame = cap.read()

		if frame is None:
			print("[ERROR]: No camera connection")
			break
		frame = cvResize(frame, (500,500))#(195,150))
		gray = cvColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		if firstFrame is None:
			firstFrame = gray
			print('got first frame')
			continue
		frameDelta = cv2.absdiff(firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)
		(cnts,_) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for c in cnts:
			if cv2.contourArea(c) < THRESHOLD:
				continue
			else:
				print('motion detected')
				cap.release()
				firstFrame = gray
				return True

		break

	#release camera
	print('no motion')
	cap.release()
	firstFrame = gray
	return False

def snap_photo():
	global cam_event
	cam_event.set()
	subcall(client_path)
	cam_event.clear()

def birbs_monitor(birb_event):
	while True:
		if cam_event.is_set():
			sleep(3)
			continue
		#if birb present
		if birb_online():
			birb_event.set()
		else:
			birb_event.clear()
		sleep(3)

def notify(birb_event, watcher):
	global notify_chat_ids
	global photo_chat_ids
	watcher.start()
	while True:
		birb_event.wait()
		print('birb event is set')
		msg = '<b>Birbs are present!</b> Enjoy birbs for a limited time!'
		try:
			sticker = open('static/enthusiastic.webp', 'rb')
		except:
			print('error opening sticker')
			raise
		for id in notify_chat_ids:
			print('looking through notify chat ids')
			bot.send_chat_action(id, 'typing')
			bot.send_message(id, msg, parse_mode='html')
			bot.send_sticker(id, sticker)
		while birb_event.is_set():
			if not photo_chat_ids:
				continue
			snap_photo()
			photo = open('photo.jpg', 'rb')
			for id in photo_chat_ids:
				bot.send_photo(id, photo)
			sleep(5)
		msg = '<b>Birbs are gone.</b> This is life, nothing last!'
		sticker = open('static/cry.png', 'rb')
		for id in notify_chat_ids:
			bot.send_chat_action(id, 'typing')
			bot.send_message(id, msg, parse_mode='html')
			bot.send_sticker(id, sticker)

		sleep(3)

watcher = threading.Thread(target=birbs_monitor, args=(birb_event,))
watcher.daemon = True
notifier = threading.Thread(target=notify, args=(birb_event,watcher))
notifier.daemon = True
notifier.start()

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
	/send_birbs - Ask me to send you nudes, oops I mean, pictures of birbs the moment I detect them.
	/send_none - After this command I'll stop auto-sending you photos of birbs.'''
	bot.send_message(msg.chat.id, help_msg, parse_mode='html')
	help_msg ="\nThat's it! Good luck, {0.first_name}!\n".format(msg.from_user)
	bot.send_message(msg.chat.id, help_msg)
	bot.send_message(msg.chat.id, "\nI'm a busy Bot, I'll hurry to my ebanaya rabota!")
	sticker = open('static/hurry.png', 'rb')
	bot.send_sticker(msg.chat.id, sticker)

@bot.message_handler(commands=['photo'])
def take_photo(msg):
	snap_photo()
	photo = open('photo.jpg', 'rb')
	bot.send_photo(msg.chat.id, photo)

@bot.message_handler(commands=['notify_me'])
def notify_on(msg):
	global notify_chat_ids
	global DB
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/yessir.webp', 'rb')
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_sticker(msg.chat.id, sticker)
	bot.send_message(msg.chat.id, "\nNotifications turned on!")
	notify_chat_ids.append(msg.chat.id)
	DB.add_to_notify(msg.chat.id)

@bot.message_handler(commands=['notify_off'])
def notify_off(msg):
	global notify_chat_ids
	global DB
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_message(msg.chat.id, "\nNotifications turned off. You broke my birby heart...")
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/drama.png', 'rb')
	bot.send_sticker(msg.chat.id, sticker)
	notify_chat_ids.remove(msg.chat.id)
	DB.unassign_notify(msg.chat.id)

@bot.message_handler(commands=['send_birbs'])
def send_birbs(msg):
	global photo_chat_ids
	#global stream_chat_ids
	global DB
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/ok.png', 'rb')
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_sticker(msg.chat.id, sticker)
	bot.send_message(msg.chat.id, "\nOk, I'll send you photos!")
	photo_chat_ids.append(msg.chat.id)
	DB.add_to_photos(msg.chat.id)
	# if msg.chat.id in stream_chat_ids:
	# 	stream_chat_ids.remove(msg.chat.id)
	# 	DB.unassign_streams(msg.chat.id)

@bot.message_handler(commands=['send_none'])
def send_no_birbs(msg):
	global photo_chat_ids
	global DB
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/disappointed.webp', 'rb')
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_sticker(msg.chat.id, sticker)
	bot.send_message(msg.chat.id, "\nOk, I'll stop sending you photos.")
	try:
		photo_chat_ids.remove(msg.chat.id)
		DB.unassign_photos(msg.chat.id)
	except ValueError:
		pass

@bot.message_handler(commands=['stream'])
def stream(msg):
	bot.send_message(msg.chat.id, "Unimplemented.")

@bot.message_handler(commands=['status'])
def get_status(msg):
	global birb_event
	bot.send_chat_action(msg.chat.id, 'typing')
	if not birb_event.is_set():
		sticker = open('static/full.png', 'rb')
		status='It seems all birbs are full already or have trouble finding us.'
	else:
		sticker = open('static/fun.png', 'rb')
		status='Hooray! Birbs detected.'
	bot.send_message(msg.chat.id, status)
	bot.send_sticker(msg.chat.id, sticker)

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
		bot.send_chat_action(msg.chat.id, 'typing')
		bot.send_sticker(msg.chat.id, sticker)
		bot.send_message(msg.chat.id, 'See ya again at Birbs Temple!')
	elif msg.text == 'fuck':
		bot.send_chat_action(msg.chat.id, 'typing')
		sticker = open('static/rude.png', 'rb')
		bot.send_chat_action(msg.chat.id, 'typing')
		bot.send_sticker(msg.chat.id, sticker)
		bot.send_message(msg.chat.id, "I'm getting bullied... I thought we were birbrends!")


bot.polling(none_stop=True)
