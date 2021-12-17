from rpi_ws281x import * #import for led driving
import time
import sys
import random as r

#Block for setting up the actual LEDs, hardware definitions etc...
LED_COUNT = 150*1 #150 lights per strip...
LED_PIN = 21 #GPIO pin
LED_FREQ_HZ = 800000 #light signal requency
LED_DMA = 10 #dma pin internally 
LED_BRIGHTNESS = 128 #LED brightness out of 255
LED_INVERT = False #inversion of the light signal... only needed if you include a hardware signal booster
LED_CHANNEL = 0 #pcm channel... only one so choose 0
LED_STRIP = ws.WS2811_STRIP_GRB #brand/type of strrip

global pos #globals for effect logic
pos=0
comet_length = int(LED_COUNT/10)

#create a color dictionary using rpi_ws281x.Color(R,G,B)
RED = Color(255,0,0)
ORANGE = Color(255,165,0)
YELLOW = Color(255,255,0)
GREEN = Color(0,255,0)
BLUE = Color(0,0,255)
INDIGO = Color(75,0,130)
PURPLE = Color(128, 0, 128)
WHITE = Color(255,255,255)
BLACK = Color(0,0,0)

color_dict = {
        "RED" : RED,
        "ORANGE" : ORANGE,
        "YELLOW" : YELLOW,
        "GREEN" : GREEN,
        "BLUE" : BLUE,
        "INDIGO" : INDIGO,
        "PURPLE" : PURPLE,
        "WHITE" : WHITE,
        "BLACK" : BLACK,
        "x": "x" #this is an error case...
        }

RAINBOW = (RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, PURPLE)

def solid(strip, color): #turn on all lights in a strip
    for light in range(strip.numPixels()):
        strip.setPixelColor(light, color)
    strip.show()
    
def thirds(strip, color1, color2, color3): #turn on all lights 3 different colors
    for light in range(int(strip.numPixels()/3)):
        strip.setPixelColor(light, color1)
    for light in range(int(strip.numPixels()/3)):
        strip.setPixelColor(light+int(strip.numPixels()/3), color2)
    for light in range(int(strip.numPixels()/3)):
        strip.setPixelColor(light+2*int(strip.numPixels()/3), color3)
    strip.show()
    
def rainbow(strip, list_of_lights): #cycle through a tuple of colors as solids
    while True:
        for lights in list_of_lights:
            solid(strip, lights)
            time.sleep(.3)
        
def comet(strip, color, comet_length): #comet effect, travel infinitely around the strip and retrun to the begining
    global pos
    while True:
        if pos>strip.numPixels()-comet_length:
            pos=0
            solid(strip, BLACK)
        for light in range(comet_length):
            strip.setPixelColor(pos+light, color)
            strip.setPixelColor(pos-1-light, BLACK)
        pos+=comet_length
        strip.show()
        time.sleep(.1)

def comet3(strip, color1, color2, color3, comet_length): #comet but three colors
    global pos
    while True:
    
        if pos>strip.numPixels()-3*comet_length:
            pos=0
            solid(strip, BLACK)    
        
        for light in range(comet_length):
            strip.setPixelColor(pos+light, color1)
            strip.setPixelColor(pos+comet_length+light, color2)
            strip.setPixelColor(pos+2*comet_length+light, color3)
            strip.setPixelColor(pos-1-light, BLACK)
            strip.setPixelColor(pos-comet_length-1-light, BLACK)
            strip.setPixelColor(pos-(2*comet_length)-1-light, BLACK)
            
        pos+=comet_length*3
        strip.show()
        time.sleep(.3)
            
def fadeToBlack(strip): #fade from solid to black
    currentBrightness = 5*round(strip.getBrightness()/5)
    while currentBrightness > 0:
        newBrightness = currentBrightness - 5
        strip.setBrightness(newBrightness)
        strip.show()
        currentBrightness = newBrightness
        time.sleep(.05)

        
def fadeFromBlack(strip, color, maxBrightness): #fade from black to solid
    currentBrightness = 0
    while currentBrightness <= maxBrightness:
        newBrightness = currentBrightness + 5
        strip.setBrightness(newBrightness)
        solid(strip, color)
        strip.show()
        currentBrightness = newBrightness
        time.sleep(.05)
        
def breathing(strip, color, maxBrightness): #breathing effect using fades
    while True:
        solid(strip, BLACK)
        fadeFromBlack(strip, color, maxBrightness)
        fadeToBlack(strip)
        
def strobe(strip, color): #fast blink effect
    while True:
        solid(strip, BLACK)
        time.sleep(.1)
        solid(strip, color)
        time.sleep(.1)
        
def colorWipe(strip, color): #wipe a color across the strip, then wipe back to black
    """Wipe color across display a pixel at a time."""
    while True:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, BLACK)
            strip.show()
            
def random(strip, color_set): #set all pixels to a new random color every 5 seconds
    while True:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, r.choice(color_set))
        strip.show()
        time.sleep(5)
        
def error_blink(strip): #in the case of an error, blink 5 times red
    for i in range(5):
        solid(strip, RED)
        time.sleep(.5)
        solid(strip, BLACK)
        time.sleep(.5)
    strip.show()    

if __name__ == '__main__':
    #create strip object parse the command line arguements...
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    strip.begin()
    print("strip initialized and began...")
    color1 = color_dict[sys.argv[2]]
    color2 = color_dict[sys.argv[3]]
    color3 = color_dict[sys.argv[4]]
    effect = str(sys.argv[1])
    #elif block to determine the function to actually excecute...
    if effect is not "x":
        if effect == "SOLID" and color1 is not "x":
            solid(strip, color1)
        elif effect == "THIRDS" and color1 is not "x" and color2 is not "x" and color3 is not "x":
            thirds(strip, color1, color2, color3)
        elif effect == "COMET" and color1 is not "x":
            comet(strip, color1, comet_length)
        elif effect == "COMET3" and color1 is not "x" and color2 is not "x" and color3 is not "x":
            comet3(strip, color1, color2, color3, int(comet_length/3))
        elif effect == "RAINBOW":
            rainbow(strip, RAINBOW)
        elif effect == "BREATHING" and color1 is not "x":
            breathing(strip, color1, strip.getBrightness())
        elif effect == "STROBE" and color1 is not "x":
            strobe(strip, color1)
        elif effect == "COLORWIPE" and color1 is not "x":
            colorWipe(strip, color1)
        elif effect == "RANDOM":
            random(strip, RAINBOW)
        else: #input error... blink a few times
            error_blink(strip)
            solid(strip, BLACK)
    else: #input error...blink a few times
        error_blink(strip)
        solid(strip, BLACK)

