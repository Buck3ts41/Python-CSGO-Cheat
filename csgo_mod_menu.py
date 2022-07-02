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
import offsets
from offsets import *

tkey = input("triggerbot key: ")
persons = input("3rd person key: ")

layout = [sg.Text("Anaconda Mod Menu")], [sg.Button('ESP')], [sg.Button('CHAMS')], [sg.Button('Bunny Hop')], [sg.Button('FOV')], [sg.Button('Radar Hack')], [sg.Button('Triggerbot')], [sg.Button('Skin Changer')], [sg.Button('Show Rank')], [sg.Button('3RD Person'), [sg.Button('No Flash')]], [sg.Button("exit")]
window = sg.Window("Buck3ts41", layout)

def esp():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        player = pm.read_uint(client + dwLocalPlayer)
        localTeam = pm.read_uint(player + m_iTeamNum)
        glow_manager = pm.read_int(client + dwGlowObjectManager)
        for i in range(1, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_hp = pm.read_uint(entity + m_iHealth)
                entity_team_id = pm.read_uint(entity + m_iTeamNum)
                entity_dormant = pm.read_uint(entity + m_bDormant)
                entity_glow = pm.read_uint(entity + m_iGlowIndex)
                if entity_hp > 50 and not entity_hp == 100:
                    r, g, b = 255, 165, 0
                elif entity_hp < 50:
                    r, g, b = 255, 144, 0
                elif entity_hp == 100 and entity_team_id == 2:
                    r, g, b = 0, 255, 0
                elif entity_hp > 25:
                    r, g, b = 255, 0, 0
                else:
                    r, g, b = 0, 255, 0

                if entity_team_id == 2 and localTeam != 2 and not entity_dormant:  ###TERRORIST###
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(r))  # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(g))  # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(b))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(255))  # A
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # START

                elif entity_team_id == 3 and localTeam != 3 and not entity_dormant:  ###COUNTER###
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(r))  # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(g))  # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(b))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(255))  # A
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # START


def chams():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    rgbt = [255, 3, 3]
    rgbc = [3, 255, 20]

    while True:

        time.sleep(0.001)
        for i in range(1, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)


            if entity:
                entity_team_id = pm.read_uint(entity + m_iTeamNum)

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
    player = pm.read_uint(client + dwLocalPlayer)
    crosshairID = pm.read_uint(player + m_iCrosshairId)
    getcrosshairTarget = pm.read_uint(client + dwEntityList + (crosshairID - 1) * 0x10)
    localTeam = pm.read_uint(player + m_iTeamNum)
    crosshairTeam = pm.read_uint(getcrosshairTarget + m_iTeamNum)

    if keyboard.is_pressed(tkey) and 0 < crosshairID <= 64 and localTeam != crosshairTeam:
        pm.write_int(client + dwForceAttack, 6)

    else:
        pass

def person():
    switch = 0

    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        localplayer = pm.read_int(client + dwLocalPlayer)

        if keyboard.is_pressed(persons) and switch == 0:
            pm.write_int(localplayer + m_iObserverMode, 1)
            switch = 1
            time.sleep(0.5)
        if keyboard.is_pressed(persons) and switch == 1:
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
def rank():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll")
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll")
    ranks = ["Unranked",
             "Silver I",
             "Silver II",
             "Silver III",
             "Silver IV",
             "Silver Elite",
             "Silver Elite Master",
             "Gold Nova I",
             "Gold Nova II",
             "Gold Nova III",
             "Gold Nova Master",
             "Master Guardian I",
             "Master Guardian II",
             "Master Guardian Elite",
             "Distinguished Master Guardian",
             "Legendary Eagle",
             "Legendary Eagle Master",
             "Supreme Master First Class",
             "The Global Elite"]
    for i in range(0, 32):
        entity = pm.read_uint(client.lpBaseOfDll + dwEntityList + i * 0x10)

        if entity:
            entity_team_id = pm.read_uint(entity + m_iTeamNum)
            if entity_team_id:
                player_info = pm.read_uint(
                    (pm.read_uint(engine.lpBaseOfDll + dwClientState)) + dwClientState_PlayerInfo)
                player_info_items = pm.read_uint(pm.read_uint(player_info + 0x40) + 0xC)
                info = pm.read_uint(player_info_items + 0x28 + (i * 0x34))
                playerres = pm.read_uint(client.lpBaseOfDll + dwPlayerResource)
                rank = pm.read_uint(playerres + m_iCompetitiveRanking + (i * 4))
                wins = pm.read_uint(playerres + m_iCompetitiveWins + i * 4)
                if pm.read_string(info + 0x10) != 'GOTV':
                    print(rank)
                    print(pm.read_string(info + 0x10) + "   -->   " + ranks[rank])
                    print(wins)

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
t10 = Thread(target=rank)

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
    if event == "Show Rank":

        t10.start()

window.close()





