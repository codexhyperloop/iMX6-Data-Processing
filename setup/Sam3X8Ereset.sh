#!/bin/sh

# enable erase signal
echo out > /sys/class/gpio/gpio117/direction
echo 1 > /sys/class/gpio/gpio117/value

# reset
echo 0 >/gpio/gpio0/value
sleep 0.2
echo 1 >/gpio/gpio0/value

sleep 0.2

# disable erase signal
echo 1 > /sys/class/gpio/gpio117/value
echo in > /sys/class/gpio/gpio117/direction