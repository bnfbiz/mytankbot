#!/bin/env python3
import RPi.GPIO as GPIO
import time
import evdev
import pirobot


# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

ultrasonic_servo_PIN = 16
LED_R = 22
LED_G = 27
LED_B = 24

ultrasonic_echo_PIN = 0 # BCM = 27, BOARD = 13
ultrasonic_trigger_PIN = 1 # BCM = 28, BOARD = 
ultrasonic_tirgger_time = 0.00002
speed_of_sound_MperS = 343
speed_of_sound_cmPerS = 343 * 100  # 100cm per meter

usonic = pirobot.ultrasonic.Ultrasonic()
usonic.init_us(ultrasonic_echo_PIN,ultrasonic_trigger_PIN,ultrasonic_tirgger_time,pirobot.ultrasonic.UNITS_CM)

GPIO.setup(ultrasonic_servo_PIN,GPIO.OUT)
GPIO.setup(LED_R,GPIO.OUT)
GPIO.setup(LED_G,GPIO.OUT)
GPIO.setup(LED_B,GPIO.OUT)
GPIO.setup(ultrasonic_trigger_PIN,GPIO.OUT)
GPIO.setup(ultrasonic_echo_PIN,GPIO.IN)

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
    # GPIO.output(ultrasonic_trigger_PIN,GPIO.HIGH)
    # time.sleep(ultrasonic_tirgger_time)
    # GPIO.output(ultrasonic_trigger_PIN,GPIO.LOW)

    # # Determine when the ping starts
    # while GPIO.input(ultrasonic_echo_PIN) == 0:
    #     echo_start = time.time()
    
    # # wait until ping ends
    # while GPIO.input(ultrasonic_echo_PIN) == 1:
    #     echo_stop = time.time()

    # echo_duration = echo_stop - echo_start

    # #          Distance
    # # Speed = ----------   ==> Distance = Speed * Time / 2
    # #           Time/2
    # # Time is divided by 2 as it is a round trip
    # #
    # distance = speed_of_sound_cmPerS * echo_duration / 2
    distance = usonic.GetDistance()

    print("Angle is " + str(count) + " Distance is " + str(distance))
    if distance > (shortest + delta):
        GPIO.output(LED_R, GPIO.HIGH)
        GPIO.output(LED_G, GPIO.LOW)
        GPIO.output(LED_B, GPIO.LOW)
    else:
        GPIO.output(LED_R, GPIO.LOW)
        GPIO.output(LED_G, GPIO.HIGH)
        GPIO.output(LED_B, GPIO.LOW)
        shortest = distance

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


