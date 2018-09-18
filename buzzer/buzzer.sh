#!/bin/sh

echo 0 > /sys/class/pwm/pwmchip0/export

echo 200000 >  /sys/class/pwm/pwmchip0/pwm0/period
echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable

echo 50000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
sleep 1
echo 100000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
sleep 1
echo 150000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
sleep 1
echo 30000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
sleep 1
echo 0 > /sys/class/pwm/pwmchip0/pwm0/enable

echo 0 > /sys/class/pwm/pwmchip0/unexport
