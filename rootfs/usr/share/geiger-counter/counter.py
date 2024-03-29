#!/usr/bin/python3
# THE GEIGER COUNTER (at last)
"""
   Copyright 2020-2023 Chris Crocker-White https://github.com/chrisys
   Modifications Copyright 2023 Ramon F Kolb https://github.com/kx1t

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import exixe
import spidev
import time
import datetime
import os
import RPi.GPIO as GPIO
from collections import deque
from influxdb import InfluxDBClient

try:
    geiger_pin=int(os.environ.get("GEIGER_PIN"))
except: 
    geiger_pin=7

print(f'Starting Counter, input from pin {geiger_pin}; output to {os.environ.get("DB_OUTPUT")}...', flush=True)

counts = deque()
hundredcount = 0
usvh_ratio = 0.00812037037037 # This is for the J305 tube

# This method fires on edge detection (the pulse from the counter board)
def countme(channel):
    global counts, hundredcount
    timestamp = datetime.datetime.now()
    counts.append(timestamp)

    # Every time we hit 100 counts, run count100 and reset
    hundredcount = hundredcount + 1
    if hundredcount >= 100:
        hundredcount = 0
        count100()

# This method runs the servo to increment the mechanical counter
def count100():
    GPIO.setup(12, GPIO.OUT)
    pwm = GPIO.PWM(12, 50)

    pwm.start(4)
    time.sleep(1)
    pwm.start(9.5)
    time.sleep(1)
    pwm.stop()


# Set the input with falling edge detection for geiger counter pulses
GPIO.setup(geiger_pin, GPIO.IN)
GPIO.add_event_detect(geiger_pin, GPIO.FALLING, callback=countme)

# Initialize everything needed for the Exixe Nixie tube drivers
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 7800000

cs_pin = 15
cs_pin_m = 13
cs_pin_r = 11

my_tube = exixe.Exixe(cs_pin, spi)
my_tube_m = exixe.Exixe(cs_pin_m, spi, overdrive=True)
my_tube_r = exixe.Exixe(cs_pin_r, spi)

my_tube.set_led(127, 28, 0)
my_tube_m.set_led(127, 28, 0)
my_tube_r.set_led(127, 28, 0)

# Setup influx client (this is using a modified version of balenaSense)
if os.environ.get('DB_OUTPUT') == "influx":
    influx_client = InfluxDBClient('influxdb', 8086, database='balena-sense')
    influx_client.create_database('balena-sense')

loop_count = 0

# In order to calculate CPM we need to store a rolling count of events in the last 60 seconds
# This loop runs every second to update the Nixie display and removes elements from the queue
# that are older than 60 seconds
while True:
    loop_count = loop_count + 1

    try:
        while counts[0] < datetime.datetime.now() - datetime.timedelta(seconds=60):
            counts.popleft()
    except IndexError:
        pass # there are no records in the queue.

    if loop_count == 10:
        # Every 10th iteration (10 seconds), store a measurement in Influx or make it available to Prometheus
        if os.environ.get('DB_OUTPUT') == "influx":
            measurements = [
                {
                    'measurement': 'balena-sense',
                    'fields': {
                        'cpm': int(len(counts)),
                        'usvh': "{:.2f}".format(len(counts)*usvh_ratio)
                    }
                }
            ]
            influx_client.write_points(measurements)
            print(measurements,"\n");
        elif os.environ.get('DB_OUTPUT') == "prometheus":
            with open("/run/prometheus.prom", 'w') as f:
                print(f'geiger_cpm {int(len(counts))}', file=f)
                print(f'geiger_usvh {"{:.2f}".format(len(counts)*usvh_ratio)}', file=f)
                f.close()
        else:
            print("ERROR: $DB_OUTPUT is not \'influx\ or \'prometheus\'", flush=True)
        if os.environ.get('GEIGER_VERBOSE') == "true":
            print(f'count={int(len(counts))} cpm', flush=True)
            print(f'exposure={"{:.2f}".format(len(counts)*usvh_ratio)} uSv/h', flush=True)

        loop_count = 0

    # Update the displays with a zero-padded string
    text_count = f"{len(counts):0>3}"
    my_tube.set_digit(int(text_count[0]))
    my_tube_m.set_digit(int(text_count[1]))
    my_tube_r.set_digit(int(text_count[2]))

    time.sleep(1)
