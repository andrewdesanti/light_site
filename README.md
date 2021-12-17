# light_site
## _A Python Powered Raspberry Pi and WS281x LED Control WebApp_


light_site is a Flask WebApp that can be used to control an individually addressable LED strip connected to a Raspberry Pi.

## Features

- Connect from any device's web browser while connected to the same network
- Choose from several pre-programmed effects using a simple HTML form
- See your choice in reflected in the LEDs immediately

## How It Works

light_site uses a number of open source projects to work properly:

- [Python3](https://www.python.org/) - This one's pretty self explainatory
- [Flask](https://www.python.org/) - A lightweight Python web framework 
- [psutil](https://github.com/giampaolo/psutil) -  A cross-platform library for retrieving information on running processes and system utilization in Python
- [rpi_ws281x](https://github.com/jgarff/rpi_ws281x) - Userspace Raspberry Pi library for controlling WS281X LEDs in several languages

## Installation

light_site requires a Raspberry Pi to be running a relatively up-to-date raspbian/raspberrypiOS operating system, as well as an open pwm or pcm GPIO pin.

Install the dependencies...

```sh
sudo pip3 install flask rpi_ws281x_python psutil
```
To download this repository...

```sh
git clone https://github.com/andrewdesanti/light_site.git
```

To begin the local dev server that hosts this site locally on your Pi...

```sh
sudo python3 light_site.py
```


## Hardware Setup

### _PLEASE NOTE_:
Incorrectly setting up the hardware can possibly damage the Raspberry Pi, LEDs, or even yourself! While this is compatable with many different LED and Raspberry Pi models, do your own research on how to safely set them up!

A very simple wiring diagram MAY look like this. PLEASE I can not stress how important it is to do this correctly according to your hardware!
 ![alttext](https://tutorials-raspberrypi.com/ezoimgfmt/tutorials-raspberrypi.de/wp-content/uploads/Raspberry-Pi-WS2812-Steckplatine-600x361.png?ezimgfmt=rs:600x361/rscb1/ng:webp/ngcb1)
 
 ### _ALSO!_
 
 The first few lines of light_functs.py require you to input a few parameters according to your own hardware setup! Remember to do this before running!
 

## Functions

There are several light functions to choose from:
- Solid: Turn on all lights a solid color of your choice
- Thirds: Turn on all lights three different solid colors of your choice
- Comet: A 'comet' will travel infinitely around the strip in a color of your choice
- Comet3: The same as comet but in three colors
- Rainbow: The strip cycles through the colors of the rainbow 
- Breathing: The strip fades in and out of a color of your choice
- Strobe: Strobe light of your choice
- ColorWipe: A color wipes across the strip and then wiped away
- Random: All lights turn on a random color of the rainbow. This changes every 5 seconds.

Choose from any color of the rainbow! Note that BLACK indicates "off". (Turning off the lights is equivalent to Solid: Black)

Keep in mind that not all effects require all 3 colors to be set. 
In the event an invalid combo of effect and colors is chosen, the strip will blink red a few times and then turn off.
