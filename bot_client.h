#include <sys/types.h>
#include <unistd.h>
#include <errno.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <linux/ioctl.h>
#include <linux/types.h>
#include <linux/v4l2-common.h>
#include <linux/v4l2-controls.h>
#include <linux/videodev2.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <string.h>
#include <fstream>
#include <string>
//#include <vector>

using namespace std;

//#define PICNAME "photo.jpg"
#define PICNAME "/tmp/stream/pic.jpg"
#define CVPIC "/tmp/stream/cvpic.jpg"

#define BUFSIZE 1024
