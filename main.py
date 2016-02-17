#/usr/bin/python3

'''
This process monitors /queue for new files and sends them to the bot without
confirmation unless there's an issue.
'''

import os, serial, time
try:
    import innernet
except:
    os.subprocess('wget https://raw.githubusercontent.com/pumpkinpai/innernet/master/innernet.py')
    # todo: restart script

# CONFIGURATION- MAIN
# todo: firstRun and update functions
firstRun    = True  # True if this hasn't been run before (downloads deps)
autoUpdate  = False # True or False, to check github for updates and do 'em

# CONFIGURATION- PRINTER
devName = '/dev/tty0'
devBaud = 115200    # 9600, something something
devScan = True      # True to scan other tty's if tty0 isn't found
devScanMax = 5      # give up after ttyx

# CONFIGURATION- INNERNET
'''
innernet.port       = 65656
innernet.name       = 'Red Baron'   # Name of this machine
innernet.password   = 'password'    # shared password by innernet devices
innernet.friendlist = ['all']       # list of devices to listen to, ['all'] for all
innernet.ignorelist = []            # list of devices to ignore
'''


def sendJob(grblFilename):
    # Make serial connection
    try:
        s = serial.Serial(devName, devBaud)
    except:
        return 'no connection'

    grblFile = open(grblFilename, 'r')

    # Grbl init
    s.write('\r\n\r\n')
    # Give it time to init
    time.sleep(3.0)
    # Flush startup text from serial input
    s.flushInput()

    # Stream gcode!
    for line in grblFile:
        # prep each line for clean serial injection
        line = line.strip() + '\n'
        s.write(line)
        # Wait for grbl response with '\n'
        grbl_out = s.readline()

    grblFile.close()
    s.close()
    return True

if __name__ == "__main__":

    # todo: check firstRun and autoUpdate & run if True

    while True:
        # Give the fella a break
        time.sleep(5.0)

        # todo: check for innernet messages (jobs)
        if innernet.connected() == True:
            innernet.post('msgCheck')
        else:
            innernet.connect()

        # todo: check for file in queue folder, choose oldest
        queueFilename = 'test.gcode'
        success = sendJob(queueFilename)
        if success == True:
            # todo: report success to job sender
            # todo: move file to done folder
            pass
        else:
            print(success)

