CC      := g++
#CFLAGS := -O2
CFLAGS := -fno-exceptions -fno-rtti -ffunction-sections -fdata-sections -fno-math-errno
CFLAGS += -ffast-math
LDFLAGS := -s -pthread
LDFLAGS += -fno-exceptions -fno-rtti -ffunction-sections -fdata-sections -Wl,--gc-sections -fno-math-errno
LDFLAGS += -Wl,-z,norelro -Wl,--build-id=none
BUILD    := .
OBJ_DIR  := $(BUILD)/objects
APP_DIR  := $(BUILD)
INC_DIR  := $(BUILD)
TARGET   := bot_client
INCLUDE  := -I$(INC_DIR)

SRC      := bot_client.cpp

OBJ = $(SRC:.cpp=.o)
OBJECTS = $(addprefix $(OBJ_DIR)/, $(OBJ))
SOURCES = $(addprefix $(OBJ_DIR)/, $(SRC))

all: build $(APP_DIR)/$(TARGET)

$(OBJ_DIR)/%.o: %.cpp
	@mkdir -p $(@D)
	$(CC) $(CFLAGS) $(INCLUDE) -o $@ -c $<

$(APP_DIR)/$(TARGET): $(OBJECTS)
	@mkdir -p $(@D)
	$(CC) $(INCLUDE) $(LDFLAGS) -o $@ $^

.PHONY: all build clean debug release

build:
	@mkdir -p $(OBJ_DIR)

debug: CFLAGS += -DDEBUG -g
debug: all

release: CFLAGS += -O2
release: all

clean:
	-@rm -rvf $(OBJ_DIR)/*
	-@rm -rf $(OBJ_DIR)
	-@rm -f $(APP_DIR)/$(TARGET)