#!/usr/bin/env python3
########################################################################
# Filename    : Blink.py
# Description : Basic usage of GPIO. Let led blink.
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
import time

ledPin = [11, 29]    # defines the ledPin variable, which is used within the script.
# The ledPin variable can contain multiple values as it's within square brackets
# ledPin refers to the physical numbering on the board, 11 being GPIO17 and 29 being GPIO5

def setup(): #creates a function called 'setup' which configures GPIO and sets pins
    for led in ledPin:
        GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
        # This could also be GPIO.BCM for BCM numbering)
        GPIO.setup(led, GPIO.OUT)   # set the ledPin to OUTPUT mode
        # This could also be set to GPIO.IN for INPUT mode
        GPIO.output(led, GPIO.LOW)  # make ledPin output LOW level
        # Setting the PIN to low switches them off, when they're set to HIGH it 'switches on' what's connected

print ('using pin', ledPin) # This is just a basic print statement which outputs which PINs are being used, by outputting the ledPin variable


def loop(): #This defines a loop (called loop) which will run indefinitely as there is no end to it. It's just 'while true'
    while True:
        for ledOn in ledPin: #for starts a sub-loop which will run through all of the values within ledPin
            # ledOn is the variable which will use all of the values within the ledPin 'array'
            GPIO.output(ledOn, GPIO.HIGH)  # make ledPin output HIGH level to turn on led
            #Uses the ledOn variable to define which PIN is set to HIGH
            print ('led turned on >>>')     # print information on terminal
            time.sleep(0.5)                   # Wait for 1 second
            # The loop will complete once all of the values within ledPin have been used. In this case, 11 and 29
        for ledOff in ledPin: #for starts a sub-loop which will run through all of the values within ledPin
            GPIO.output(ledOff, GPIO.LOW)   # make ledPin output LOW level to turn off led
            #Uses the ledOn variable to define which PIN is set to HIGH
            print ('led turned off <<<')
            time.sleep(0.5)                   # Wait for 1 second
            # The loop will complete once all of the values within ledPin have been used. In this case, 11 and 29



def destroy(): # This defines a clean-up activity (called destroy) which sets all of the GPIOs back to default values
    GPIO.cleanup()                      # Release all GPIO

if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    setup() #calls setup to set the board numbering, set the PINs to LOW and OUTPUT mode
    try: #creates a loop which will run until interrupted
        loop() #this calls the loop from earlier and runs it indefinitely
        # The loop will continue indefinitely, until interrupted with CTRL+C from the keyboard
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
    # Once interrupted, the script continues to the final steps
        destroy() #calls the destroy subroutine to clear up


