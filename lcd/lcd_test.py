import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time
# Setup LCD with digitalio
lcd_rs = digitalio.DigitalInOut(board.D13)
lcd_en = digitalio.DigitalInOut(board.D21)
lcd_d4 = digitalio.DigitalInOut(board.D19)
lcd_d5 = digitalio.DigitalInOut(board.D16)
lcd_d6 = digitalio.DigitalInOut(board.D26)
lcd_d7 = digitalio.DigitalInOut(board.D20)
lcd_coloumns = 16
lcd_rows = 2
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_coloumns, lcd_rows)

# Use LCD with the message sequence

# Boot up
lcd.clear()
lcd.message = "Booting up..."
time.sleep(5)

# Intro
lcd.clear()
lcd.message = "Hello. How can I\nhelp?"
time.sleep(5)

# Conversation Event Loop
lcd.clear()
lcd.message = "Press the small button to speak"
time.sleep(5)
lcd.clear()
lcd.message = "Go ahead"
time.sleep(5)
lcd.clear()
lcd.message = "Processing..."
time.sleep(5)
lcd.clear()
lcd.message = "Press the small button to speak"

# Shutting down
lcd.clear()
lcd.message = "Cleaning up..."
time.sleep(5)
lcd.message = "Going to sleep"
time.sleep(5)
lcd.clear()
