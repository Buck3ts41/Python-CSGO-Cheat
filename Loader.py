import psutil
from art import *
import time
import os
import colorama
from colorama import Fore


tprint("Anaconda Loader v1.2")
print("By Buck3ts41", '\n')
time.sleep(1)

input("Start cs:go, when in lobby press ENTER")
processName = 'csgo.exe'

def checkProcessRunning(processName):

    for proc in psutil.process_iter():
        try:

            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

if checkProcessRunning('csgo'):
    print(Fore.GREEN + "Cheat started, have fun!")
    import csgo_mod_menu
    csgo_mod_menu
else:
    print(Fore.RED + "Process not found or need to Update Offsets")
    time.sleep(3)
    exit(0)
