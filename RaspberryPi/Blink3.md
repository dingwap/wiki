# Walkthrough of blink3 Python script

## Intro

I've taken a script which was included as part of my awesome Freenove Raspberry Pi makers kit and stepped through it in logical chunks to explain what's going on. 

This is to help me learn, and to remind myself how it works as I'll have 6 months between when I get chance to play with this next, and in the meantime I'll forget.

---
## Importing modules

Firstly, import the relevant modules required for the script. The **time** module is imported as-is, the **RPi.GPIO** module is imported as **GPIO** so you don't have to type out the whole thing each time.

    import RPi.GPIO as GPIO
    import time

## Setting variables

This next bit sets up a **list** for the **ledPin** variable. A list means the variable can contain more than one thing, and each thing is separated by a comma, and you can tell it's a list as it's within square brackets.

In this case it contains two numbers, 11 and 29 which will refer to GPIO pins in the script.

*We'll see in a bit whether this will be physical GPIO numbering or Broadcom numbering, exciting!*

    ledPin = [11, 29]

ledPin refers to the physical numbering on the board, 11 being GPIO17 and 29 being GPIO5

## Creating our first function (setup)

Next, we set up a function called **setup** which will configure the GPIO pins. A function is a collection of commands which are structured together and are a thing which you will re-use more than once in your script.

It saves you typing the same command over and over again, and it also saves space in your script.

    def setup(): 
    for led in ledPin:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(led, GPIO.OUT)   
        GPIO.output(led, GPIO.LOW)  

So, stepping through this in order

    def setup():
This defines the name of the function being created (**Setup**)

    for led in ledPin:

A few things here. Firstly, we're creating a loop in the script and a variable which will run in the script called **led**. You can tell this by the use of **for** and a **colon (:)** at the end.

A loop will start to do something and stop either when something happens or when it runs out of something to do.

In this case it will stop when it runs out of variables within our **list** which we created earlier, called **ledPin**

When you have a **colon** in a script Python then indents the next line to show that it's running within the loop.

This script is used to set up each of the GPIO pins we'll be working with.

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led, GPIO.OUT)   
    GPIO.output(led, GPIO.LOW) 

These lines do three things:

1. Set the mode of the GPIO numbering **(GPIO.BOARD)**, which means physical numbering rather than Broadcom numbering. Broadcom numbering would use **(GPIO.BCM)**
2. Set the mode of each GPIO PIN we're using **(GPIO.OUT)**. This means the PIN will be used to provide an output, which will be used to trigger an action
3. Set the output for the GPIO **(GPIO.LOW)**. This would be the same as turning the GPIO off, which is what we want when the script first runs.

You'll notice the use of the variable **led** in the function. This means that for each cycle of the loop the led variable will be used to set the relevant settings.

* In the first loop of the script it will use the first number in the **list**
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(11, GPIO.LOW)
* For the next loop it will use the next number in the **list**
    GPIO.setup(29, GPIO.OUT)
    GPIO.setup(29, GPIO.LOW)

The loop will then run out of numbers as the **list** only contains two, and will then finish.

***Important Note!*** - the function won't run yet. All that's happened above is the function has been created. It won't actually do anything until it's called later on within the script.

## A quick print statement

    print ('using pin', ledPin)

This is just a basic print statement which outputs which PINs are being used, by outputting the ledPin variable

## Creating our next function (loop)

    def loop():
        while True:    
            for ledOn in ledPin:
                GPIO.output(ledOn, GPIO.HIGH)
                print ('led turned on >>>')
                time.sleep(0.5)
            for ledOff in ledPin:
                GPIO.output(ledOff, GPIO.LOW)
                print ('led turned off <<<')
                time.sleep(0.5)

**Note:** *The above function shows the script with 4 levels of indent. This is because there is the main loop (**while True**) and two other loops which run inside of this (**for ledOn** and **for ledOff**). Python requires this indentation to show where the loops are, and the code editor you're using will automatically indent the code when you finish a line with a **colon(:)*** 

Stepping through this section in order...

    def loop():
This starts again with the definition of function, this time called **loop**

        while True:
The **while true** statement at the start of a loop means it will run for the full extent of the list it's using **(ledPin)**, or until it's interrupted by sometthing.

            for ledOn in ledPin: 

So, as before, the **for** statement defines the start of the loop with the **colon(:)** at the end to signal the start of the loop.

This loop will create the **ledOn** variable for use within the loop, and will read from the contents within the **ledPin** list.

                GPIO.output(ledOn, GPIO.HIGH)
                print ('led turned on >>>')
                time.sleep(0.5)
                
The loop will do 3 things:

1. It will set the relevant GPIO pin output to **HIGH**, which will be the signal for the LED to switch on.
2. It will print a statement to confirm that the led has been switched on.
3. It willl pause **(sleep)** for one second.

 *The loop will complete once all of the values within ledPin have been used. In this case, 11 and 29*. It will set the two GPIO values (held within **ledPin**) to **HIGH** and then complete and progress down the script.

Next is the second part of the function, which is another loop.
            for ledOff in ledPin:

Once again, the **for** statement defines the start of the loop with the **colon(:)** at the end to signal the start of the loop.

This loop will create the **ledOff** variable for use within the loop, and will read from the contents within the **ledPin** list.
                GPIO.output(ledOff, GPIO.LOW)
                print ('led turned off <<<')
                time.sleep(0.5)

The loop will do 3 things:

1. It will set the relevant GPIO pin output to **LOW**, which will be the signal for the LED to switch off.
2. It will print a statement to confirm that the led has been switched on.
3. It willl pause **(sleep)** for one second.

 *The loop will complete once all of the values within ledPin have been used. In this case, 11 and 29*. It will set the two GPIO values (held within **ledPin**) to **LOW** and then complete and progress down the script.

 ## Creating our final function (destroy)

This starts again with the name of function, this time called **destroy**

    def destroy():
        GPIO.cleanup()                      

 This is a basic function defines a clean-up activity (called destroy) which sets all of the GPIOs back to default values. The **GPIO.cleanup()** command runs once to reset all values back to their defaults.

## Now, finally to run the script!

This small number of lines is all that is required to run the script. However, it's only this short because we've spent the time above to create the functions being called within these few lines.

    if __name__ == '__main__':   
        print ('Program is starting ... \n')
This first part just kicks off the script and prints a message to screen to confirm the script is running

        setup()
The first step is to run the **setup()** function above, which:

1. Sets the board numbering
2. Sets the mode for the relevant GPIO pins **(OUTPUT)**
3. Sets the output for the relevant GPIO pins **(LOW)**

        try: 
            loop()
This next step is to run the **loop()** function above, which:
1. Turns each LED on
2. Waits 1 second
3. Turns each LED off
4. Waits one second

This will continue to loop around as there is no condition or **for** loop running which steps through a sequence of items in a **list**

        except KeyboardInterrupt:
            destroy()

The final step is to monitor for a **KeyboardInterrupt**, which is CTRL+C. When it receives this input the final function is called to reset all of the GPIO pins to their defaults and end the script.

Shazam.