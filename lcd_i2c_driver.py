import smbus
import time

### Clear whole display instruction
CLEAR_DISPLAY = 0x01

### Return cursor to start instruction
RETURN_HOME = 0x02

### Entry mode set instruction
ENTRYMODE_SET_MODE = 0x04
# After write of data to display move cursor left/right
MOVE_LEFT_AFTER_WRITE = 0x00
MOVE_RIGHT_AFTER_WRITE = 0x02
# Shift entire display after data write
ENTIRE_DISPLAY_SHIFT = 0x01
ENTIRE_DISPLAY_SHIFT_NOT = 0x00

### Control display state instruction
DISPLAY_CONTROL_MODE = 0x08
# Display turned ON/OFF
DISPLAY_ON = 0x04
DISPLAY_OFF = 0x00
# Cursor turned ON/OFF
DISPLAY_CURSOR_ON = 0x02
DISPLAY_CURSOR_OFF = 0x00
# Cursor position visible ON/OFF
DISPLAY_CURSOR_POS_ON = 0x01
DISPLAY_CURSOR_POS_OFF = 0x00

### Move display or cursor position instruction
SHIFT_MODE = 0x10
# Move display or cursor
DISPLAY_MOVE = 0x08
DISPLAY_CURSOR_MOVE = 0x00
# Move left or right
MOVE_LEFT = 0x00
MOVE_RIGHT = 0x04

### Function set instruction
FUNCTIONSET_MODE = 0x20
# Interface data len
EIGHT_BIT = 0x10
FOUR_BIT = 0x00
# Line number
TWO_LINE = 0x08
ONE_LINE = 0x00
# Char size
SIZE_5x10 = 0x04
SIZE_5x8 = 0x00

### Set write cursor address instruction
DDRAM_ADDRESS_SET_MODE = 0x80

### Backlight pins
BACKLIGHT_ON = 0x08
BACKLIGHT_OFF = 0x00

REGISTER_SELECT_BYTE = 0b00000001
READ_WRITE_BYTE = 0b00000010
ENABLE_BYTE = 0b00000100


class LcdDisplay:
    ### Constructor
    def __init__(self, address=0x27):
        self.address = address
        self.bus = smbus.SMBus(1)
        # Put display into 4bit mode (according to docs)
        self.write_lcd_byte(0x03)
        time.sleep(0.0045)
        self.write_lcd_byte(0x03)
        time.sleep(0.0045)
        self.write_lcd_byte(0x03)
        time.sleep(0.001)
        self.write_lcd_byte(0x02)
        # Set lines font size
        self.write_lcd_byte(FUNCTIONSET_MODE | FOUR_BIT | TWO_LINE | SIZE_5x8)
        # Turn display on with cursor turned off
        self.write_lcd_byte(DISPLAY_CONTROL_MODE | DISPLAY_ON | DISPLAY_CURSOR_OFF | DISPLAY_CURSOR_POS_OFF)
        # Clear display
        self.write_lcd_byte(CLEAR_DISPLAY)
        # Set entry mode for data that will be written fo siplay
        self.write_lcd_byte(ENTRYMODE_SET_MODE | MOVE_RIGHT_AFTER_WRITE | ENTIRE_DISPLAY_SHIFT_NOT)
        # Init wait time
        time.sleep(0.1)

    ### Internal write functions
    def write_bus_byte(self, data):
        self.bus.write_byte(self.address, data)
        # Data hold time
        time.sleep(0.0001)

    def write_lcd_four_bits(self, data):
        # Data
        self.write_bus_byte(data | BACKLIGHT_ON)
        # Enable high
        self.write_bus_byte(data | ENABLE_BYTE | BACKLIGHT_ON)
        time.sleep(.0005)
        # Enable low
        self.write_bus_byte((data & ~ENABLE_BYTE) | BACKLIGHT_ON)
        time.sleep(.0001)
    
    def write_lcd_byte(self, data, mode=0b00000000):
        # Write upper 4 bits first
        self.write_lcd_four_bits((data & 0xF0) | mode)
        # Write lower 4 bits after
        self.write_lcd_four_bits(((data << 4) & 0xF0) | mode)

    ### External write functions
    def write_lcd_string(self, string_data):
        for character in string_data:
            lcd.write_lcd_byte(ord(character), REGISTER_SELECT_BYTE)

    ### External utility functions
    def clear_lcd(self):
        self.write_lcd_byte(CLEAR_DISPLAY)

### Main, test driver
if __name__ == "__main__":
    lcd = LcdDisplay()
    while True:
        print("Test lcd i2c driver menu:")
        print("1. Write string to display")
        print("2. Clear display")
        print("4. Exit")
        try:
            in_command = int(input(": "))
            if in_command == 1:
                data_str = int(input("Write string: "))
                lcd.write_lcd_string(data_str)
            elif in_command == 2:
                lcd.clear_lcd()
            elif in_command == 4:
                break
        except Exception as ex:
            continue
