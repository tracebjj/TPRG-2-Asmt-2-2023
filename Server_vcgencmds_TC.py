# This server runs on Pi, sends Pi's your 4 arguments from the vcgencmds, sent as Json object.

# details of the Pi's vcgencmds - https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd
# more vcgens on Pi 4, https://forums.raspberrypi.com/viewtopic.php?t=245733
# more of these at https://www.nicm.dev/vcgencmd/

import socket
import os, time
import json

s = socket.socket()
host = '0.0.0.0' # Localhost
port = 5000
s.bind((host, port))
s.listen(5)


#gets the Core Temperature from Pi, ref https://github.com/nicmcd/vcgencmd/blob/master/README.md
t = os.popen('vcgencmd measure_volts ain1').readline() #gets from the os, using vcgencmd - the core-temperature
#gets the GPU core speed
spd = os.popen('vcgencmd measure_clock core').readline() #gets from the os, using vcgencmd - the GPU core speed
#gets the HDMI clock
HDMIclk = os.popen('vcgencmd measure_clock hdmi').readline()
#measures RAM I/O Voltage
RAMIOV = os.popen('vcgencmd measure_volts sdram_i').readline()
#measures SD card interface speed
SDCLKSPD = os.popen('vcgencmd measure_clock emmc').readline()

# initialising json object string
ini_string = """{"Temperature": t,
"GPU Core Speed": spd,
"HDMI Speed": HDMIclk,
"RAM I/O Voltage": RAMIOV,
"SD Card Interface Speed": SDCLKSPD}"""
# converting string to json
f_dict = eval(ini_string) # The eval() function evaluates JavaScript code represented as a string and returns its completion value.



while True:
    c, addr = s.accept()
    print ('Got connection from',addr)
    res = bytes(str(f_dict), 'utf-8') # needs to be a byte
    c.send(res) # sends data as a byte type
    c.close()