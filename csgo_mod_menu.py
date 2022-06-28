import pymem
import pymem.process
import keyboard
import win32gui
from art import *
import time
import os
import PySimpleGUI as sg


os.system("cls")
tprint("CS:GO Mod Menu")
print("By Buck3ts41", '\n')

time.sleep(1)


layout = [sg.Text("Anaconda Mod Menu")], [sg.Button('ESP')], [sg.Button('CHAMS')], [sg.Button('Bunny Hop')], [sg.Button('FOV')], [sg.Button('Radar Hack')], [sg.Button('Triggerbot')], [sg.Button('3RD Person')], [sg.Button("exit")]


window = sg.Window("Buck3ts41", layout)


while True:
    event, values = window.read()

    if event == "exit" or event == sg.WIN_CLOSED:
        break
    if event == "ESP":
        ###OFFSETS###
        dwEntityList = (0x4DDB92C)
        dwLocalPlayer = (0xDBF4CC)
        m_iTeamNum = (0xF4)
        dwGlowObjectManager = (0x5324588)
        m_iGlowIndex = (0x10488)


        ###MAIN###

        def main():
            pm = pymem.Pymem("csgo.exe")
            client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

            while True:

                glow_manager = pm.read_int(client + dwGlowObjectManager)
                for i in range(1, 32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)

                    if entity:
                        entity_team_id = pm.read_int(entity + m_iTeamNum)
                        entity_glow = pm.read_int(entity + m_iGlowIndex)

                    if entity_team_id == 2:  ###TERRORIST###
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))  # R
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))  # G
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))  # B
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # A
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # START

                    elif entity_team_id == 3:  ###COUNTER###
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))  # R
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))  # G
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # B
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # A
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # START


        if __name__ == "__main__":
            main()

    if event == "CHAMS":
        ###OFFSETS###
        dwEntityList = (0x4DDB92C)
        dwLocalPlayer = (0xDBF4CC)
        m_iTeamNum = (0xF4)
        m_clrRender = (0x70)
        model_ambient_min = (0x590054)


        ###MAIN###

        def main():
            pm = pymem.Pymem("csgo.exe")
            client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
            engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll

            rgbt = [255, 51, 0]
            rgbc = [0, 51, 255]

            while True:

                time.sleep(0.001)
                for i in range(32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)

                    if entity:
                        entity_team_id = pm.read_int(entity + m_iTeamNum)
                        if entity_team_id == 2:  # terrorist
                            pm.write_int(entity + m_clrRender, (rgbt[0]))  # R
                            pm.write_int(entity + m_clrRender + 0x1, (rgbt[1]))  # G
                            pm.write_int(entity + m_clrRender + 0x2, (rgbt[2]))  # B

                        elif entity_team_id == 3:  # counter
                            pm.write_int(entity + m_clrRender, (rgbc[0]))  # R
                            pm.write_int(entity + m_clrRender + 0x1, (rgbc[1]))  # G
                            pm.write_int(entity + m_clrRender + 0x2, (rgbc[2]))  # B

                    else:
                        pass


            
        if __name__ == "__main__":
            main()

    if event == "Bunny Hop":
        ###OFFSETS###
        dwForceJump = (0x52858A8)
        dwLocalPlayer = (0xDBF4CC)
        m_fFlags = (0x104)


        ###MAIN###
        def main():
            pm = pymem.Pymem("csgo.exe")
            client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

            while True:

                if keyboard.is_pressed("space"):
                    force_jump = client + dwForceJump
                    player = pm.read_int(client + dwLocalPlayer)
                    on_ground = pm.read_int(player + m_fFlags)
                    if player and on_ground and on_ground == 257:
                        pm.write_int(force_jump, 5)
                        time.sleep(0.08)
                        pm.write_int(force_jump, 4)


            
        if __name__ == "__main__":
            main()

    if event == "FOV":
        ###OFFSETS###
        dwEntityList = (0x4DDB92C)
        m_iDefaultFOV = (0x333C)


        ###MAIN###
        def main():
            pm = pymem.Pymem("csgo.exe")
            client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

            while True:
                player = pm.read_int(client + dwEntityList)
                iFOV = pm.read_int(player + m_iDefaultFOV)

                pm.write_int(player + m_iDefaultFOV, 140)



        if __name__ == "__main__":
            main()

    if event == "Radar Hack":
        ###OFFSETS###
        dwEntityList = (0x4DDB92C)
        m_bSpotted = (0x93D)


        ###MAIN###
        def main():
            pm = pymem.Pymem("csgo.exe")
            client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

            while True:
                for i in range(1, 32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    if entity:
                        pm.write_uchar(entity + m_bSpotted, 1)


        if __name__ == "__main__":
            main()

    if event == "Triggerbot":
        ###OFFSETS###
        dwEntityList = (0x4DDB92C)
        dwForceAttack = (0x320BE10)
        dwLocalPlayer = (0xDBF4CC)
        m_iCrosshairId = (0x11838)
        m_iTeamNum = (0xF4)
        m_fFlags = (0x104)


        ###MAIN###
        def main():
            pm = pymem.Pymem("csgo.exe")
            client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

            while True:
                localPlayer = pm.read_int(client + dwLocalPlayer)
                crosshairID = 0
                crosshairID = pm.read_int(localPlayer + crosshairID)
                getTeam = pm.read_int(client + dwEntityList + (crosshairID - 1) * 0x10)
                localTeam = pm.read_int(localPlayer + m_iTeamNum)
                crosshairTeam = pm.read_int(getTeam + m_iTeamNum)

                if crosshairID > 0 and crosshairID < 32 and localTeam != crosshairTeam:
                    pm.write_int(client + dwForceAttack, 6)

        if __name__ == "__main__":
            main()

    if event == "3RD Person":
        ###OFFSETS###
        m_iObserverMode = (0x3388)
        dwLocalPlayer = (0xDBF4CC)

        ###MAIN###
        switch = 0
        print("enable\disable with z")
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

        while True:
            localplayer = pm.read_int(client + dwLocalPlayer)

            if keyboard.is_pressed("z") and switch == 0:
                pm.write_int(localplayer + m_iObserverMode, 1)
                switch = 1
                time.sleep(0.5)
            if keyboard.is_pressed("z") and switch == 1:
                pm.write_int(localplayer + m_iObserverMode, 0)
                switch = 0
                time.sleep(0.5)


window.close()





