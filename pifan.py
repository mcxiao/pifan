#!/usr/bin/env python

from RPi import GPIO as gpio
import time

# max = 55
# upper_limit = 45
# lower_limit = 40
# min = 38

# sleeping = 6
# long_sleeping = 6
# max_work_time = 2 * 6

warn_max = 55
upper_limit = 50
lower_limit = 41
warn_min = 36

sleeping = 60
long_sleeping = 120
max_work_time = 60 * 60

debug = True
port = 40
run = False


def log(string, timestamp=False):
    if not debug:
        return
    if timestamp:
        print "{0} --- {1}".format(time.ctime(), string)
    else:
        print string


def cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = float(f.read()) / 1000
        f.close()
        return temp


stime = -1


def start():
    gpio.output(port, gpio.HIGH)
    global stime
    stime = time.time()


def stop():
    gpio.output(port, gpio.LOW)
    global stime
    stime = -1


def main():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(port, gpio.OUT)

    log('Program start and cpu temp {0}'.format(cpu_temp()))
    while run:
        cputemp = cpu_temp()
        # too hot to start fan
        if cputemp > upper_limit:
            log('Alert: cpu temp {0}, rolling fan!'.format(cputemp), timestamp=True)
            start()
            time.sleep(long_sleeping)
        # temp down and stop fan
        elif cputemp < lower_limit and stime > 0:
            log('Tips: cpu temp {0}, fan stop.'.format(cputemp), timestamp=True)
            stop()
        else:
            # just roll
            pass
        # print "starttime: {0}\ncputemp: {1}\ncurtime: {2}".format(starttime, cputemp, time.time())
        time.sleep(sleeping)

    gpio.cleanup(port)


if __name__ == '__main__':
    run = True
    main()
