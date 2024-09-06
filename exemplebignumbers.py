import time
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import os
import subprocess
import RPi.GPIO as GPIO
import random
import digitalio

arrayUtilitario = [[False, False], [False, True], [True, True], [True, False]]
received_delta = [0, 0, 0]
contador = [0, 0, 0]
multiplicador = [0, 0, 0]

butx = digitalio.DigitalInOut(board.D17)
butx.direction = digitalio.Direction.INPUT
butx.pull = digitalio.Pull.UP

buty = digitalio.DigitalInOut(board.D24)
buty.direction = digitalio.Direction.INPUT
buty.pull = digitalio.Pull.UP

butcond = digitalio.DigitalInOut(board.D18)
butcond.direction = digitalio.Direction.INPUT
butcond.pull = digitalio.Pull.UP

encoderPrimary1 = digitalio.DigitalInOut(board.D13)
encoderPrimary1.direction = digitalio.Direction.OUTPUT

encoderPrimary2 = digitalio.DigitalInOut(board.D26)
encoderPrimary2.direction = digitalio.Direction.OUTPUT

encoderPrimary3 = digitalio.DigitalInOut(board.D5)
encoderPrimary3.direction = digitalio.Direction.OUTPUT

encoderPrimary = [encoderPrimary1, encoderPrimary2, encoderPrimary3]

encoderSecondary1 = digitalio.DigitalInOut(board.D19)
encoderSecondary1.direction = digitalio.Direction.OUTPUT

encoderSecondary2 = digitalio.DigitalInOut(board.D16)
encoderSecondary2.direction = digitalio.Direction.OUTPUT

encoderSecondary3 = digitalio.DigitalInOut(board.D6)
encoderSecondary3.direction = digitalio.Direction.OUTPUT

encoderSecondary = [encoderSecondary1, encoderSecondary2, encoderSecondary3]

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Use for I2C.
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load default font and resize for larger text.
font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)

# Initialize variables

condition = 1


def generatePulses(num,contagem):
    received_delta[num] = contagem
    #print("received_delta", received_delta)
    for i in range(3):
        if received_delta[i] > 0:
            multiplicador[i] = 1
        elif received_delta[i] < 0:
            multiplicador[i] = -1
        else:
            multiplicador[i] = 0

    while any(multiplicador):
        #print("multiplicador", multiplicador)
        for i in range(3):
            if multiplicador[i] != 0:
                received_delta[i] -= multiplicador[i]
                contador[i] = (4 + contador[i] - multiplicador[i]) % 4
                print(multiplicador,arrayUtilitario[contador[i]][0],arrayUtilitario[contador[i]][1])
                encoderPrimary[i].value = arrayUtilitario[contador[i]][0]
                encoderSecondary[i].value = arrayUtilitario[contador[i]][1]
                #print("encoderPrimary", encoderPrimary)
                if received_delta[i] == 0:
                    multiplicador[i] = 0

def plot(x, y):
    # Clear the display
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
        # Display the letter on the left 1/4 of the screen
        draw.text((WIDTH // 8, HEIGHT // 6), 'x', font=font_large, fill=255)
        # Display the random number on the right 3/4 of the screen
        draw.text((WIDTH // 3, HEIGHT // 6), x, font=font_large, fill=255)

        draw.text((WIDTH // 8, HEIGHT // 2), 'Y', font=font_large, fill=255)
        # Display the random number on the right 3/4 of the screen
        draw.text((WIDTH // 3, HEIGHT // 2), y, font=font_large, fill=255)

        oled.image(image)
        oled.show()

x = 0
y = 0

plot(str(x), str(y))


while True:


    if butx.value:
        x += condition
        generatePulses(0, condition)
        generatePulses(2, condition)
        plot(str(x), str(y))
        

        # Debounce delay
        time.sleep(0.5)

    if buty.value:
        y += condition
        generatePulses(1, condition)
        generatePulses(2, condition)
        plot(str(x), str(y))


        # Debounce delay
        time.sleep(0.5)

    if butcond.value:
        condition = condition * -1

        # Debounce delay
        time.sleep(0.5)
