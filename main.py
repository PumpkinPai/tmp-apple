#/usr/bin/python3

'''
This process monitors /queue for new files and sends them to the bot without
confirmation unless there's an issue.
'''

import os, serial, time

'''
try:
    import innernet
except:
    os.subprocess('wget https://raw.githubusercontent.com/pumpkinpai/innernet/master/innernet.py')
    # todo: restart script
'''

# CONFIGURATION- MAIN
# todo: firstRun and update functions
firstRun    = True  # True if this hasn't been run before (downloads deps)
autoUpdate  = False # True or False, to check github for updates and do 'em

# CONFIGURATION- PRINTER
devName = '/dev/ttyUSB0'
devBaud = 38400     # 9600, 19200, 38400, 57600, 115200, 230400, 250000
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
        #todo: if devScan == True check other ports and/or bauds
        return 'no connection'

    # debug
    print('Connection established')

    resp = input('Enter gcode command: ')

    while resp != 'exit':
        resp += '\n'
        s.write(resp.encode())
        soutput = s.readline()
        print(soutput)
        resp = input('Enter gcode command: ')

    grblFile = open(grblFilename, 'r')

    # Grbl init
    s.write('\r\n\r\n'.encode())
    # Give it time to init
    time.sleep(3.0)
    # Flush startup text from serial input
    s.flushInput()

    # Stream gcode!
    for line in grblFile:
        if line[0] == ';' or line[0] == ' ': continue
        print(line)
        # prep each line for clean serial injection
        line = line.strip() + '\n'
        s.write(line.encode())
        # Wait for grbl response with '\n'
        grbl_out = s.readline()
        print(grbl_out)

    grblFile.close()
    # debug
    print('gcode file complete')
    s.close()
    return True

if __name__ == "__main__":

    # todo: check firstRun and autoUpdate & run if True

    running = True

    while running:
        # Give the fella a break
        time.sleep(5.0)


        # todo: check for innernet messages (jobs)
        if True: # Todo: innernet.connected() == True:
            pass
            #innernet.post('msgCheck')
        else:
            innernet.connect()


        # todo: check for file in queue folder, choose oldest
        queueFilename = 'test.gcode'
        success = sendJob(queueFilename)
        if success == True:
            #debug
            print('successfully printed')
            running = False #debug
            # todo: report success to job sender
            # todo: move file to done folder
            pass
        else:
            print(success)

