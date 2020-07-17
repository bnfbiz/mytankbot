#!/bin/env python3
import RPi.GPIO as GPIO
import time
import evdev
import pirobot


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ultrasonic_servo_PIN = 23
LED_R = 22
LED_G = 27
LED_B = 24

GPIO.setup(ultrasonic_servo_PIN,GPIO.OUT)
GPIO.setup(LED_R,GPIO.OUT)
GPIO.setup(LED_G,GPIO.OUT)
GPIO.setup(LED_B,GPIO.OUT)
p = GPIO.PWM(ultrasonic_servo_PIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization

MAX_SERVO_SWEEP=180
count_up = True
count = 0
shortest = 1000
delta = 100       

while True:
    # sweep back and forth, turn on the LED's Green when closest, RED when far
    p.ChangeDutyCycle(2.5+ ( 10 * count/MAX_SERVO_SWEEP))
    print("Angle is " + str(count))
    # if distance > (shortest + delta):
    #     GPIO.output(LED_R, GPIO.HIGH)
    #     GPIO.output(LED_G, GPIO.LOW)
    #     GPIO.output(LED_B, GPIO.LOW)
    # else:
    #     GPIO.output(LED_R, GPIO.LOW)
    #     GPIO.output(LED_G, GPIO.HIGH)
    #     GPIO.output(LED_B, GPIO.LOW)
    #     shortest = distance

    if count > MAX_SERVO_SWEEP:
        count_up = False
    elif  count < 0:
        count_up = True

    if count_up:
        count += 1
    else:
        count -= 1

    time.sleep(0.01)
 
p.stop()
GPIO.cleanup


