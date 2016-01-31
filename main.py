#/usr/bin/python3

'''
This process monitors /queue for new files and sends them to the bot without
confirmation unless there's an issue.
'''
# CONFIGURATION
devName = '/dev/tty_000?'
devBaud = 115200    # 9600, something something

import os, serial, time


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

    while True:
        queueFilename = 'test.gcode'
        success = sendJob(queueFilename)
        if success == True:
            # todo: report success to job sender
            # todo: move file to done folder
            pass
        else:
            print(success)

        # Give the fella a break
        time.sleep(5.0)
