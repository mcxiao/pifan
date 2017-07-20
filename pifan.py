#!/usr/bin/env python

from RPi import GPIO as gpio
import time

#max = 55
#upper_limit = 45
#lower_limit = 40
#min = 38

#sleeping = 6
#long_sleeping = 6
#max_work_time = 2 * 6

max = 55
upper_limit = 50
lower_limit = 41
min = 36

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


starttime = -1


def start():
    gpio.output(port, gpio.HIGH)
    global starttime
    starttime = time.time()


def stop():
    gpio.output(port, gpio.LOW)
    global starttime
    starttime = -1


def main():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(port, gpio.OUT)

    log('Program start and cpu temp {0}'.format(cpu_temp()))
    while run:
        cputemp = cpu_temp()
        # if RPi not too 'hot' and fan run so long, then let fan take five.O_o
        runtime = time.time() - starttime
        if starttime > 0 and cpu_temp < max and runtime > max_work_time:
            log('Tips: cpu temp {0} and run so long {1}s, take fiiiiive.'.format(cputemp, runtime), timestamp=True)
            stop()
        # too hot to start fan
        elif cputemp > upper_limit:
            log('Alert: cpu temp {0}, rolling fan!'.format(cputemp), timestamp=True)
            start()
            time.sleep(long_sleeping)
        # temp down and stop fan
        elif cputemp < lower_limit and starttime > 0:
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
