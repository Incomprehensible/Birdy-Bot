# THIS SCRIPT SETS UP BIRDY BOT FOR YOU
# PASS BOT TOKEN TO IT

DIR="."
token=""

while [[ $# -ge 1 ]]; do
    i="$1"
    case $i in
        -t|--token)
            token=$2
            shift
            ;;
        *)
            echo "Unrecognized option $1"
            exit 1
            ;;
    esac
    shift
done

if [ -z "$token" ]; then
  echo "Token for bot is required (-t | --token)" >&2
  exit 1
fi

git clone "$DIR/https://github.com/Incomprehensible/Birdy-Bot.git"

# insert token into config.py
sed -i.bak "s/^\(TOKEN=\).*/\1'${token}'/" config.py

sudo apt-get update
sudo apt-get upgrade

cd $DIR/Birdy-Bot
# build streaming code
make all
cd -

# install bot dependencies
sudo apt-get install python3-pip
pip3 install pyTelegramBotAPI
pip3 install opencv-contrib-python

print 'Building MJPG-Streamer...'
# install dependencies
sudo apt-get install libjpeg8-dev imagemagick libv4l-dev
# mjpeg-streamer needs missing videodev.h
sudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h
# download MJPG-Streamer
wget 'https://sourceforge.net/code-snapshots/svn/m/mj/mjpg-streamer/code/mjpg-streamer-code-r182.zip'
if [ $? -ne 0 ]; then
    echo "Download link didn't work. Replace with the new one from here: http://sourceforge.net/p/mjpg-streamer/code/HEAD/tarball." ;
    exit -1;
    fi

unzip mjpg-streamer-code-182.zip
cd mjpg-streamer-code-182/mjpg-streamer
# build MJPG-Streamer
make mjpg_streamer input_file.so output_http.so
if [ $? -ne 0 ]; then
    echo "Make failed. See troubleshooting notes in README.md." ;
    exit -1;
    fi

# copy needed files to sys directories
sudo cp mjpg_streamer /usr/local/bin
sudo cp output_http.so input_file.so /usr/local/lib/
sudo cp -R www /usr/local/www

# prepare streaming path
mkdir /tmp/stream
# launch streaming
print 'Make sure your camera is ready for streaming in case code fails to execute.'
$DIR/Birdy-Bot/birdy_client &

# start MJPG-Streamer
print 'Starting MJPG-Streamer...'
LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www" &

rm -rf mjpg-streamer-182
# prepare database path
mkdir $DIR/Birdy-Bot/db
# launch bot
python3 $DIR/Birdy-Bot/birdy_bot.py


print 'Your streaming link is: http://localhost:8080'

