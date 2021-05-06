# Birdy-Bot
A Birdy Bot is a Telegram bot that helps you watch birds online. It's also absolute birbs about birds.
Host it on Raspberry Pi in an enclosure and set it up near the birds feeder.

## How it works
Interact with birdy bot to see which commands it understands.
It can send you pictures one at a time, streaming link; or it could notify you of birds online with messages and pictures.
Feel free to explore **`@birbs_watching_bot`** in Telegram! 

## Deploy
If you want to deploy your own birdy bot, follow steps below or let [SETUP.sh](https://github.com/Incomprehensible/Birdy-Bot/blob/main/SETUP.sh "Auto deploy") setup the system for you.
* Get your token from BotFather. Insert it into [config.py](<>):
* ```python

```
* Upgrade your system and install dependencies:
* ```zsh
    me@home$ sudo apt-get update && sudo apt-get upgrade
    me@home$ sudo apt-get install python3-pip
    me@home$ pip3 install pyTelegramBotAPI                              # we need Telegram API
    me@home$ pip3 install opencv-contrib-python                         # and OpenCV for motion detection
    me@home$ sudo apt-get install libjpeg8-dev imagemagick libv4l-dev   # also packages for MJPG-Streamer
```
* Build MJPG-Streamer
* ```zsh
    me@home$ wget 'https://sourceforge.net/code-snapshots/svn/m/mj/mjpg-streamer/code/mjpg-streamer-code-r182.zip'
    me@home$ unzip mjpg-streamer-code-182.zip
    me@home$ cd mjpg-streamer-code-182/mjpg-streamer
    me@home$ make mjpg_streamer input_file.so output_http.so            # see troubleshooting if this fails
```
* Prepare system files:
* ```zsh
    me@home$ sudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h
    me@home$ sudo cp mjpg_streamer /usr/local/bin
    me@home$ sudo cp output_http.so input_file.so /usr/local/lib/
    me@home$ sudo cp -R www /usr/local/www && cd -
    me@home$ mkdir /tmp/stream
    me@home$ rm -rf mjpg-streamer-182
```
* Build streaming code and prepare database path:
* ```zsh
    me@home$ cd Birdy-Bot; make all
    me@home$ mkdir db
    ```
* Finally, launch everything:
* ```zsh
    pi@home$ $DIR/Birdy-Bot/birdy_client &
    pi@home$ LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www" &
    pi@home$ python3 $DIR/Birdy-Bot/birdy_bot.py
    ```

## Troubleshooting notes
Make sure your camera is enabled with raspiconfig. Or you can enable it with the command:
```zsh
    pi@home$ sed -i "s/start_x=0/start_x=1/g" /boot/config.txt
```
