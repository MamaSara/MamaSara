import matplotlib.pyplot as plt
import numpy as np
import time 
import os
import subprocess


# Next two functions from https://www.raspberrypi.org/forums/viewtopic.php?t=22180
# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string
def getCPUuse():
    #return 0
    d = dict(os.environ)
    d['TERM'] = 'xterm-256color'
    cmd = "top n1 b | awk '/Cpu\(s\):/ {print $2}'"#[ 'echo', 'arg1', 'arg2' ]
    #cmd = ['top', '-n1']
    output = subprocess.Popen(cmd, env =d, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    return float(output)



old_t = time.time()

cpu = [0]
mem = [0]
x = [0]
t = 0
x_step = 1.0
plt.legend()
plt.title('CPU and Memory Usage')
plt.xlabel('Time (s)')
plt.ylabel('Usage (%)')
while 1:
    if(time.time() - old_t >= 1):
        old_t = time.time()
        t += 1
        x.append(t)
        # Get from top

        ram_info = getRAMinfo()
        ram_perc_used = float(ram_info[1])/float(ram_info[0]) * 100

        mem.append(ram_perc_used)
        use = getCPUuse()

        cpu.append(use)
        
        plt.draw()
        plt.plot(x, cpu, 'r-')
        plt.plot(x, mem, 'b-')

        plt.legend()
        plt.title('CPU and Memory Usage')
        plt.xlabel('Time (s)')
        plt.ylabel('Usage (%)')

        plt.show(block=False)
        print("showing")

        
