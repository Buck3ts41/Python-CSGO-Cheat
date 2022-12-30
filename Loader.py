import psutil
import time
from colorama import Fore, Style
import os
os.system("cls")
print(Fore.CYAN + """
___________        ___________     __________            _____   .__              ________            ________   
\_   _____/___  ___\__    ___/____ \______   \  ____    /  _  \  |  |      ___  __\_____  \           \_____  \  
 |    __)_ \  \/  /  |    | _/ __ \ |       _/ /    \  /  /_\  \ |  |      \  \/ / /  ____/             _(__  <  
 |        \ >    <   |    | \  ___/ |    |   \|   |  \/    |    \|  |__     \   / /       \            /       \ 
/_______  //__/\_ \  |____|  \___  >|____|_  /|___|  /\____|__  /|____/      \_/  \_______ \    /\    /______  / 
        \/       \/              \/        \/      \/         \/                          \/    \/           \/  
                                                                                                                 
""" + Style.RESET_ALL, '\n')


print(Fore.CYAN + "[*] By Buck3ts41", '\n', Style.RESET_ALL)
time.sleep(2)
os.system("cls")
input(Fore.YELLOW + "---> Press ENTER in game <---")

def checkProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

if checkProcessRunning('csgo'):
    import csgo_mod_menu
    csgo_mod_menu
else:
    print(Fore.RED + "[!] Process not found or need to Update Offsets")
    time.sleep(3)
    exit(0)