#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from Adafruit_IO import Client, RequestError
from tkinter import * 
from tkinter import messagebox
import time

#
# Set up the window and a canvas
#
ws = Tk()
ws.title('HackEDbeta 2021')
ws.geometry('496x187+100+100')
ws.config(bg='#345')

hebimage = PhotoImage(file='doc/HackEDbeta2021_496_187.png')
my_canvas = Canvas(ws, width=496, heigh=187)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0, 0, image=hebimage, anchor=("nw"))

#
# Connect to the Adafruit MQTT server
#
ADAFRUIT_IO_KEY = 'aio_thAA80ibSIMlGmAmN8HiMIu8fOZU'
ADAFRUIT_IO_USERNAME = 'eeknud'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY) 

#
# Let's get the last state of the button
#
try:
    hackEDbetaButtonFeed = aio.feeds('hackedbeta-toggle')
except RequestError:
    print("feed error")
sleep(0.1)
hackEDbetaButtonState = aio.receive(hackEDbetaButtonFeed.key)
buttonState = hackEDbetaButtonState.value
print("Initial HackEDbeta button state : %s" % (buttonState) )

#
# Make a label that will reflect the current button state
#
on_off_label = Label(my_canvas, font=("Helvetica", 20))
on_off_label.place(x = 180, y = 82)
if buttonState == 'OFF':
    on_off_label.config(bg = '#FFF000000', text = "OFF")
else:
    on_off_label.config(bg = '#000FFF000', text = " ON")

#
# Make a method that repeats itself to periodically 
# check the MQTT feed for an update
#
def checkFeed():
    global buttonState
    print(time.asctime()+'  checking feed...')
    hackEDbetaButtonState = aio.receive(hackEDbetaButtonFeed.key)
    if hackEDbetaButtonState.value != buttonState:
        print("HackEDbeta button state changed to: %s" % (hackEDbetaButtonState.value) )
        buttonState = hackEDbetaButtonState.value
        if buttonState == 'ON':
            on_off_label.config(bg = '#000FFF000', text = " ON")
        else:
            on_off_label.config(bg = '#FFF000000', text = "OFF")
    ws.after(1000, checkFeed)

#
# Run forever...
#
ws.after(1000, checkFeed)
ws.mainloop()
