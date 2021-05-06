# Birdy-Bot
A Birdy Bot is a Telegram bot that helps you watch birds online. It's also absolute birbs about birds.
Host it on Raspberry Pi in an enclosure and set it up near the birds feeder.

## How it works
Interact with birdy bot to see which commands it understands.
It can send you pictures one at a time, streaming link; or it could notify you of birds online with messages and pictures.
Feel free to explore **`@birbs_watching_bot`** in Telegram! 

## Deploy
If you want to deploy your own birdy bot, follow steps below or let [SETUP.sh](https://github.com/Incomprehensible/Birdy-Bot/blob/main/SETUP.sh "Auto deploy") setup the system for you.
* Get your token from BotFather. Insert it into [config.py](<https://github.com/Incomprehensible/Birdy-Bot/blob/main/config.py>):

```python
TOKEN='your token'
```

* Upgrade your system and install dependencies:

```zsh
pi@home:~$ sudo apt-get update && sudo apt-get upgrade
pi@home:~$ sudo apt-get install python3-pip
pi@home:~$ pip3 install pyTelegramBotAPI                              # we need Telegram API
pi@home:~$ pip3 install opencv-contrib-python                         # and OpenCV for motion detection
pi@home:~$ sudo apt-get install libjpeg8-dev imagemagick libv4l-dev   # also packages for MJPG-Streamer
```

* Build MJPG-Streamer:

```console
pi@home:~$ wget 'https://sourceforge.net/code-snapshots/svn/m/mj/mjpg-streamer/code/mjpg-streamer-code-r182.zip'
pi@home:~$ unzip mjpg-streamer-code-182.zip
pi@home:~$ cd mjpg-streamer-code-182/mjpg-streamer
pi@home:~$ make mjpg_streamer input_file.so output_http.so            # see troubleshooting if this fails
```

* Prepare system files:
```console
pi@home:~$ sudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h
pi@home:~$ sudo cp mjpg_streamer /usr/local/bin
pi@home:~$ sudo cp output_http.so input_file.so /usr/local/lib/
pi@home:~$ sudo cp -R www /usr/local/www && cd -
pi@home:~$ mkdir /tmp/stream
pi@home:~$ rm -rf mjpg-streamer-182
```

* Build streaming code and prepare database path:

```console
pi@home:~$ cd Birdy-Bot; make all
pi@home:~$ mkdir db
```

* Finally, launch everything:

```zsh
pi@home:~$ $DIR/Birdy-Bot/birdy_client &
pi@home:~$ LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www" &
pi@home:~$ python3 $DIR/Birdy-Bot/birdy_bot.py
```

## Troubleshooting notes
Make sure your camera is enabled with raspi-config. Or you can enable it with the command:

```console
pi@home:~$ sed -i "s/start_x=0/start_x=1/g" /boot/config.txt
```
