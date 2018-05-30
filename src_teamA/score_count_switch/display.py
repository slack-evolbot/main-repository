# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO
from time import sleep
from time import gmtime, strftime
import datetime
import smbus
import re

#initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Define some device parameters
I2C_ADDR  = 0x27
# Maximum characters per line
LCD_WIDTH = 16

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off
 
ENABLE = 0b00000100 # Enable bit
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1
    
class Display():
    def __init__(self):
      # Initialise display
      self.lcd_byte(0x33,LCD_CMD) # 110011 Initialise
      self.lcd_byte(0x32,LCD_CMD) # 110010 Initialise
      self.lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
      self.lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
      self.lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
      self.lcd_byte(0x01,LCD_CMD) # 000001 Clear display
      sleep(E_DELAY)

    def lcd_toggle_enable(self, bits):
      # Toggle enable
      sleep(E_DELAY)
      bus.write_byte(I2C_ADDR, (bits | ENABLE))
      sleep(E_PULSE)
      bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
      sleep(E_DELAY)
      
      
    def lcd_byte(self, bits, mode):
      # Send byte to data pins
      # bits = the data
      # mode = 1 for data
      #        0 for command

      bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
      bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

      # High bits
      bus.write_byte(I2C_ADDR, bits_high)
      self.lcd_toggle_enable(bits_high)

      # Low bits
      bus.write_byte(I2C_ADDR, bits_low)
      self.lcd_toggle_enable(bits_low)

    def lcd_string(self, message,line):
      # Send string to display
      message = message.ljust(LCD_WIDTH," ")
      self.lcd_byte(line, LCD_CMD)
      for i in range(LCD_WIDTH):
        self.lcd_byte(ord(message[i]),LCD_CHR)

    def lcd_string1(self, message):
        self.lcd_string(message , LCD_LINE_1)
        self.lcd_string("" , LCD_LINE_2)
        
    def lcd_string1and2(self, message1, message2):
        self.lcd_string(message1 , LCD_LINE_1)
        self.lcd_string(message2 , LCD_LINE_2)
        
    def lcd_clear(self):
        self.lcd_byte(0x01, LCD_CMD)

    def end_display(self):
        LCD_BACKLIGHT = 0x00  #バックライトオフ
        self.lcd_byte(0x01, LCD_CMD) #表示内容クリア

if __name__ == "__main__":
    try:
        display = Display()
        i = 0
        while True:
            i += 1
            display.lcd_string(str(i) , LCD_LINE_1)
            display.lcd_string(str(i + 1), LCD_LINE_2)
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        LCD_BACKLIGHT = 0x00  #バックライトオフ
        display.lcd_byte(0x01, LCD_CMD) #表示内容クリア
        GPIO.cleanup()

