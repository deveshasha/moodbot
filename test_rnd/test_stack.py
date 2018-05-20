import sys
import subprocess
from threading import Thread
from queue import Queue, Empty  # python 3.x


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


def getOutput(outQueue):
    outStr = ''
    try:
        while True: #Adds output from the Queue until it is empty
            outStr+=outQueue.get_nowait()
    except Empty:
        return outStr

p = subprocess.Popen('python test_3.py', 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    shell=False, 
                    universal_newlines=True,
                    )

outQueue = Queue()

outThread = Thread(target=enqueue_output, args=(p.stdout, outQueue))

outThread.daemon = True

outThread.start()

someInput = ""

while someInput != "stop":
    someInput = input("Input: ") # to take input from user
    p.stdin.write(someInput) # passing input to be processed by the rasa command
    p.stdin.flush()
    output = getOutput(outQueue)
    print("Output: " + output + "\n")
    p.stdout.flush()