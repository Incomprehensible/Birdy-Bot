import telebot
import config
from secrets import token_urlsafe
import subprocess
import cv2
import threading
from time import sleep

token = token_urlsafe(8)

bot = telebot.TeleBot(config.TOKEN)

subcall = subprocess.call

THRESHOLD = 30

notify_chat_ids = []
photo_chat_ids = []

client_path = "/home/pi/birdy_bot/bot_client"

birb_event = threading.Event()
cam_event = threading.Event()

# MOTION
vidCap = cv2.VideoCapture
cvColor = cv2.cvtColor
cvResize = cv2.resize

def birb_online():
	cap = vidCap(-1)
	while True:
		ret, frame = cap.read()

    	if (frame is None):
        	print("[ERROR]: No camera connection")
			break
    	frame = cvResize(frame,(195,150))
    	gray = cvColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		if firstFrame is None:
			firstFrame = gray
			continue
		frameDelta = cv2.absdiff(firstFrame, gray)
		if frameDelta > THRESHOLD:
			cap.release()
			return True

	#release camera
	cap.release()
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
	watcher.start()
	while True:
		birb_event.wait()
		msg = '<b>Birbs are present!</b> Enjoy birbs for a limited time!'
		sticker = open('static/enthusiastic.webp', 'rb')
		for id in notify_chat_ids:
			bot.send_chat_action(id, 'typing')
			bot.send_message(id, msg)
			bot.send_sticker(id, sticker)
		while birb_event.is_set():
			snap_photo()
			photo = open('/tmp/photo.jpg', 'rb')
			for id in photo_chat_ids:
				bot.send_photo(id, photo)
			sleep(5)
		msg = '<b>Birbs are gone.</b> This is life, nothing last!'
		sticker = open('static/cry.png', 'rb')
		for id in notify_chat_ids:
			bot.send_chat_action(id, 'typing')
			bot.send_message(id, msg)
			bot.send_sticker(id, sticker)

		sleep(3)

watcher = threading.Thread(target=birbs_monitor, args=(birb_event,))
watcher.daemon = True
notifier = threading.Thread(target=notify, args=(birb_event,watcher))

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
	/send_birbs - Ask me to send you nudes, I mean, pictures of birbs the moment I detect them.
	/send_none - After this command I'll stop auto-sending you photos of birbs.'''
	bot.send_message(msg.chat.id, help_msg, parse_mode='html')
	help_msg ="\nThat's it! Good luck, {0.first_name}!\n".format(msg.from_user)
	bot.send_message(msg.chat.id, help_msg)
	bot.send_message(msg.chat.id, "\nI'm a busy Bot, I'll hurry to my ebanaya rabota!")
	sticker = open('static/hurry.png', 'rb')
	bot.send_sticker(msg.chat.id, sticker)

@bot.message_handler(commands=['photo'])
def take_photo(msg):
	#take photo
	snap_photo()
	photo = open('/tmp/photo.jpg', 'rb')
	bot.send_photo(msg.chat.id, photo)

@bot.message_handler(commands=['notify_me'])
def notify_on(msg):
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/yessir.webp', 'rb')
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_sticker(msg.chat.id, sticker)
	bot.send_message(msg.chat.id, "\nNotifications turned on!")
	notify_chat_ids.append(msg.chat.id)

@bot.message_handler(commands=['notify_off'])
def notify_off(msg):
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_message(msg.chat.id, "\nNotifications turned off. You broke my birby heart...")
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/drama.png', 'rb')
	bot.send_sticker(msg.chat.id, sticker)
	notify_chat_ids.remove(msg.chat.id)

@bot.message_handler(commands=['send_birbs'])
def send_birbs(msg):
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/ok.png', 'rb')
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_sticker(msg.chat.id, sticker)
	notify_chat_ids
	bot.send_message(msg.chat.id, "\nOk, I'll send you photos!")
	photo_chat_ids.append(msg.chat.id)

@bot.message_handler(commands=['send_none'])
def send_no_birbs(msg):
	bot.send_chat_action(msg.chat.id, 'typing')
	sticker = open('static/ok.png', 'rb')
	bot.send_chat_action(msg.chat.id, 'typing')
	bot.send_sticker(msg.chat.id, sticker)
]	bot.send_message(msg.chat.id, "\nOk, I'll stop sending you photos.")
	photo_chat_ids.remove(msg.chat.id)

@bot.message_handler(commands=['stream'])
def stream(msg):
	#stream
	bot.send_chat_action(msg.chat.id, 'find_location')

@bot.message_handler(commands=['status'])
def get_status(msg):
	global birb_event
	bot.send_chat_action(msg.chat.id, 'typing')
	if not birb_event.is_set():
		sticker = open('static/full.png', 'rb')
		msg='It seems all birbs are full already or have trouble finding us.'
	else:
		sticker = open('static/fun.png', 'rb')
		msg='Hooray! Birbs detected.'
	bot.send_message(msg.chat.id, msg)
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
		bot.send_sticker(msg.chat.id, sticker)
		bot.send_chat_action(msg.chat.id, 'typing')
		bot.send_message(msg.chat.id, 'See ya again at Birbs Temple!')

# def birbs_monitor()
# 	face_cascade = cv2.CascadeClassifier('/home/pi/abbro/daemon_recognition/haarcascade_frontalface_default.xml')
# 	vidCap = cv2.VideoCapture
# 	cvColor = cv2.cvtColor
# 	cvResize = cv2.resize
# 	faceCas = face_cascade.detectMultiScale
# 	ret, frame = cap.read()

#         if (frame is None):
#             #print("[ERROR]: No camera connection")
#             break
#         # Resize with original aspect 4:3
#         frame = cvResize(frame,(195,150))
#         # Bounds with faces, if None so no faces
#         gray = cvColor(frame, cv2.COLOR_BGR2GRAY)


#face_cascade = cv2.CascadeClassifier('/home/pi/abbro/daemon_recognition/haarcascade_frontalface_default.xml')

bot.polling(none_stop=True)
