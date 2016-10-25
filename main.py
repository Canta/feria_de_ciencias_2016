# -*- coding: utf-8 -*-
#!/usr/bin/python

import  ifts14
import  RPi.GPIO as GPIO
import  time
import  datetime
from    datetime import date, datetime, timedelta
#import  espeak

ready   = False
run     = True
cam     = 0 #número de dispositivo de obtención de imágenes.
numero  = []
last    = datetime.now()

pines   = {
  "busy"    : 2,
  "status"  : 3,
  "button"  : 4,
  "bin0"    : 14,
  "bin1"    : 15,
  "bin2"    : 16
}

def setup():
  GPIO.setmode(GPIO.BCM)
  
  GPIO.setup( pines["busy"]    , GPIO.IN )
  GPIO.setup( pines["button"]  , GPIO.IN )
  GPIO.setup( pines["status"]  , GPIO.OUT)
  GPIO.setup( pines["bin0"]    , GPIO.OUT)
  GPIO.setup( pines["bin1"]    , GPIO.OUT)
  GPIO.setup( pines["bin2"]    , GPIO.OUT)
  
  #espeak.set_voice("es")

def check_ready():
  st = GPIO.input( pines["busy"] )
  GPIO.output( pines["status"] , GPIO.HIGH if st else GPIO.LOW)
  
  if not st:
    turn_off_number()
    
  return not st

def check_button():
  tmp = datetime.combine(last.date(), last.time()) + timedelta(seconds=10)
  if  datetime.now() <= tmp:
    return
    
  if GPIO.input( pines["button"] ):
    circulos = ifts14.imaging.count_circles(
      ifts14.imaging.take_picture( cam )
    )
    
    numero  = ifts14.binary.to_bin_array( circulos )
    last    = datetime.now()
    #espeak.synth("El número que salió es el " + str(circulos) + "." )

def show_number( num ):
  for i in range(0, len(num) - 1):
    value = GPIO.HIGH if num[i] == '1' else GPIO.LOW
    if "bin" + str(i) in pines:
      GPIO.output( pines["bin" + str(i)], value )
    else:
      return

def turn_off_number():
  show_number(['0', '0', '0', '0', '0'])


setup()

while run:
  
  if ready:
    check_button()
  
  ready = check_ready()
  time.sleep(.3)
