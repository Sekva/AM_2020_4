OUTPUT := build/prog

SRC_DIR = ./src/
OBJS_DIR = ./objs/

C_SRCS := $(wildcard $(SRC_DIR)*.c)
C_OBJS := $(patsubst %.c,%.o,$(C_SRCS))
C_OBJS := ${subst $(SRC_DIR),$(OBJS_DIR),$(C_OBJS)}

all: $(OUTPUT)


$(OUTPUT): $(C_OBJS)
	clang -o $(OUTPUT) -O2 $(C_OBJS)

$(OBJS_DIR)%.o: $(SRC_DIR)%.c
	clang -c $< -o $@ -O2 

clean:
	@rm $(OBJS_DIR)/* $(OUTPUT)
