import pymem
import pymem.process
import keyboard
import win32gui
from art import *
import time
import os
import PySimpleGUI as sg
import threading
from threading import *
import ctypes
import json


###OFFSETST###
m_szCustomName = (0x304C)
dwEntityList = (0x4DDB92C)
dwClientState = (0x58CFDC)
dwLocalPlayer = (0xDBF4CC)
m_iTeamNum = (0xF4)
dwGlowObjectManager = (0x5324588)
m_iGlowIndex = (0x10488)
m_clrRender = (0x70)
model_ambient_min = (0x590054)
dwForceJump = (0x52858A8)
m_fFlags = (0x104)
m_iDefaultFOV = (0x333C)
m_bSpotted = (0x93D)
dwForceAttack = (0x320BE10)
m_iCrosshairId = (0x11838)
m_iObserverMode = (0x3388)
m_flFlashMaxAlpha = (0x1046C)
m_iItemIDHigh = (0x2FD0)
m_hMyWeapons = (0x2E08)
m_iItemDefinitionIndex = (0x2FBA)
m_OriginalOwnerXuidLow = (0x31D0)
m_nFallbackPaintKit = (0x31D8)
m_iAccountID = (0x2FD8)
m_nFallbackStatTrak = (0x31E4)
m_nFallbackSeed = (0x31DC)
m_flFallbackWear = (0x31E0)


layout = [sg.Text("Anaconda Mod Menu")], [sg.Button('ESP')], [sg.Button('CHAMS')], [sg.Button('Bunny Hop')], [sg.Button('FOV')], [sg.Button('Radar Hack')], [sg.Button('Triggerbot')], [sg.Button('Skin Changer')], [sg.Button('3RD Person'), [sg.Button('No Flash')]], [sg.Button("exit")]
window = sg.Window("Buck3ts41", layout)

def esp():
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


def chams():
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

def bhop():
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


            
def fov():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        player = pm.read_int(client + dwEntityList)
        iFOV = pm.read_int(player + m_iDefaultFOV)

        pm.write_int(player + m_iDefaultFOV, 140)

def r5():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        for i in range(1, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)
            if entity:
                pm.write_uchar(entity + m_bSpotted, 1)

def trigger():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    if keyboard.is_pressed("shift"):
        player = pm.read_int(client + dwLocalPlayer)
        entity_id = pm.read_int(player + m_iCrosshairId)
        entity = pm.read_int(client + dwEntityList + (entity_id - 1) * 0x10)

        entity_team = pm.read_int(entity + m_iTeamNum)
        player_team = pm.read_int(player + m_iTeamNum)

        if entity_id > 0 and entity_id <= 64 and player_team != entity_team:
            time.sleep(0.08)
            pm.write_int(client + dwForceAttack, 6)

        else:
            pass
    else:
        pass


def person():
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

def noflash():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    player = pm.read_int(client + dwLocalPlayer)
    if player:
        flash_value = player + m_flFlashMaxAlpha
        if flash_value:
            pm.write_float(flash_value, float(0))

    else:
        pass

def skinchanger():
    handle = pymem.Pymem("csgo.exe")
    client_dll = pymem.process.module_from_name(handle.process_handle, "client.dll").lpBaseOfDll
    engine_dll = pymem.process.module_from_name(handle.process_handle, "engine.dll").lpBaseOfDll

    def force_full_update():
        engine_state = handle.read_int(engine_dll + dwClientState)
        handle.write_int(engine_state + 0x174, -1)

    def statTrak(value):
        handle.write_int(currentWeapon + m_nFallbackStatTrak, value)

    while True:
        f = open('config.json', "r")
        config = json.load(f)

        localPlayer = handle.read_int(client_dll + dwLocalPlayer)
        for i in range(8):
            currentWeapon = handle.read_int(localPlayer + m_hMyWeapons + i * 0x4) & 0xfff
            currentWeapon = handle.read_int(client_dll + dwEntityList + (currentWeapon - 1) * 0x10)
            if currentWeapon == 0:
                continue

            weaponID = handle.read_short(currentWeapon + m_iItemDefinitionIndex)
            fallbackPaint = 0
            fallbackWear = 0.01
            itemIDHigh = -1

            for (k, v) in config.items():
                if weaponID == config[k]["id"]:
                    fallbackPaint = config[k]["skinID"]
                    fallbackWear = config[k]["float"]
                    if "statTrak" in config[k]:
                        statTrak(config[k]["statTrak"])
                    if "name" in config[k]:
                        handle.write_string(currentWeapon + m_szCustomName, config[k]["name"])
            handle.write_int(currentWeapon + m_iItemIDHigh, itemIDHigh)
            handle.write_int(currentWeapon + m_nFallbackPaintKit, fallbackPaint)
            handle.write_float(currentWeapon + m_flFallbackWear, fallbackWear)
    force_full_update()

###THREAD###
t1 = Thread(target=esp)
t2 = Thread(target=chams)
t3 = Thread(target=bhop)
t4 = Thread(target=fov)
t5 = Thread(target=r5)
t6 = Thread(target=trigger)
t7 = Thread(target=person)
t8 = Thread(target=noflash)
t9 = Thread(target=skinchanger)

while True:
    event, values = window.read()


    if event == "exit" or event == sg.WIN_CLOSED:
        break
    if event == "ESP":

        t1.start()
    if event == "CHAMS":

        t2.start()
    if event == "Bunny Hop":

        t3.start()
    if event == "FOV":

        t4.start()
    if event == "Radar Hack":

        t5.start()
    if event == "Triggerbot":

        t6.start()
    if event == "3RD Person":

        t7.start()
    if event == "No Flash":

        t8.start()
    if event == "Skin Changer":

        t9.start()

window.close()





