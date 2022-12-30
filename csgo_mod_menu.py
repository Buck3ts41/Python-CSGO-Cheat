import keyboard
import PySimpleGUI as sg
from threading import *
from globals import *
import numpy as np

r = 255
g = 3
b = 3

layout = [
    # Use a modern font and color scheme
    [sg.Text("External 2.3", font="Helvetica 20", text_color="#d80fc6")],
    # Use tabs to organize the buttons into different categories
    [sg.TabGroup([
        # Tab for aim-related buttons
        [sg.Tab("Aim", [[
            sg.Column(
                # Define the grid layout for the buttons
                [
                    [sg.Button("No Recoil", button_color=("magenta", "#a9a9a9"))],
                    [sg.Button("Triggerbot", button_color=("magenta", "#a9a9a9"))]
                ],
                # Set the number of rows and columns in the grid
            )
        ]]),
        # Tab for visual-related buttons
        sg.Tab("Visuals", [[
            sg.Column(
                # Define the grid layout for the buttons
                [
                    [sg.Button("ESP", button_color=("magenta", "#a9a9a9"))],
                    [sg.Button("CHAMS", button_color=("magenta", "#a9a9a9"))],
                    [sg.Button("FOV", button_color=("magenta", "#a9a9a9"))],
                ],
                # Set the number of rows and columns in the grid
            )
        ]]),
        sg.Tab("Misc", [[
            sg.Column(
                [
                    [sg.Button("Bunny Hop", button_color=("magenta", "#a9a9a9"))],
                    [sg.Button("Radar Hack", button_color=("magenta", "#a9a9a9"))],
                    [sg.Button("Show Rank", button_color=("magenta", "#a9a9a9"))],
                    [sg.Button("3RD Person", button_color=("magenta", "#a9a9a9"))],
                    [sg.Button("No Flash", button_color=("magenta", "#a9a9a9"))]
                ],
            )
        ]]),
        sg.Tab("LocalPlayer", [[
            sg.Column(
                [
                    [sg.Text("Player Health:")],
                    [sg.Text(key="Health")],
                    [sg.Text("Armor:")],
                    [sg.Text(key="Armor")],
                    [sg.Text("Enter a new value:")],
                    [sg.InputText(key="NewArmor")],
                    [sg.Button("Update Armor")],
                    [sg.Text("Enter a new money value:")],
                    [sg.InputText(key="Money")],
                    [sg.Button("Update Money")]


                ],
            )
        ]]),
        # Tab for color-related buttons
        sg.Tab("Color and Debug", [[
            sg.Column(
                # Define the grid layout for the sliders
                [
                    [sg.Button("Debug", button_color=("magenta", "#a9a9a9"))],
                    [sg.Text("Enter the glow color values:")],
                    [sg.Text("Red:"), sg.InputText(key="Red")],
                    [sg.Text("Green:"), sg.InputText(key="Green")],
                    [sg.Text("Blue:"), sg.InputText(key="Blue")],
                    [sg.Button("Set Glow Color")]
                ],
                # Set the number of rows and columns in the grid
            )
        ]])
    ]])]
]

window = sg.Window("Buck3ts41", layout, element_justification="center")
def debug():
    while True:
        print("crossID ", crosshairID)
        print("corssTeam ", crosshairTeam)
        print("LocalPlayer ", player)
        print("LocalTeam ", localTeam)
        print("GlowManager ", glow_manager)
        print("GetTeam ", getTeam)
        time.sleep(2)
def esp():
    while True:
        for i in range(1, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)
            if entity:
                entity_hp = pm.read_uint(entity + m_iHealth)
                entity_team_id = pm.read_uint(entity + m_iTeamNum)
                entity_dormant = pm.read_uint(entity + m_bDormant)
                entity_glow = pm.read_uint(entity + m_iGlowIndex)

                if entity_team_id == 2 and localTeam != 2 and not entity_dormant:  ###TERRORIST###
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(r))  # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(g))  # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(b))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(255))  # A
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # START
                elif entity_team_id == 3 and localTeam != 3 and not entity_dormant:  ###COUNTER###
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(r))  # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(g))  # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(b)) # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(255))  # A
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)  # START

def chams():
    rgbt = [255, 0, 0]
    rgbc = [0, 0, 255]
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
def norcs():
    view_angles = np.array(pm.read_struct(client + dwClientState_ViewAngles, '2f'))
    punch_angles = np.array(pm.read_struct(client + m_aimPunchAngle, '2f'))
    recoil_compensation = -punch_angles * 2.0
    view_angles += recoil_compensation
    pm.write_struct(client + dwClientState_ViewAngles, view_angles)
def bhop():
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
    while True:
        player = pm.read_int(client + dwEntityList)
        pm.write_int(player + m_iDefaultFOV, 140)

def r5():
    while True:
        for i in range(1, 32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)
            if entity:
                pm.write_uchar(entity + m_bSpotted, 1)

def trigger():
    while True:

        # If the crosshair is on an enemy, shoot
        if crosshairID > 0 and crosshairID < 64 and crosshairTeam != localTeam:
            keyboard.press("attack")
            time.sleep(0.1)
            keyboard.release("attack")
        time.sleep(0.1)
def person():
    switch = 0
    while True:
        localplayer = pm.read_int(client + dwLocalPlayer)

        if keyboard.is_pressed('z') and switch == 0:
            pm.write_int(localplayer + m_iObserverMode, 1)
            switch = 1
            time.sleep(0.5)
        if keyboard.is_pressed('z') and switch == 1:
            pm.write_int(localplayer + m_iObserverMode, 0)
            switch = 0
            time.sleep(0.5)

def noflash():
    if player:
        flash_value = player + m_flFlashMaxAlpha
        if flash_value:
            pm.write_float(flash_value, float(0))
    else:
        pass

def rank():
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

###THREAD###
t1 = Thread(target=esp)
t2 = Thread(target=chams)
t3 = Thread(target=bhop)
t4 = Thread(target=fov)
t5 = Thread(target=r5)
t6 = Thread(target=trigger)
t7 = Thread(target=person)
t8 = Thread(target=noflash)
t9 = Thread(target=rank)
t10 = Thread(target=debug)
t11 = Thread(target=norcs)
while True:
    event, values = window.read(timeout=100)
    if event == "exit" or event == sg.WIN_CLOSED:
        break
    if event == "__TIMEOUT__":
        # Read the health value of the player
        health = pm.read_uint(player + m_iHealth)

        # Update the displayed health value
        window["Health"].update(str(health))
    if event == "Set Glow Color":
        # Split the input string into a list of strings representing the red, green, and blue values
        r = values["Red"]
        g = values["Green"]
        b = values["Blue"]

        # Convert the strings to integers
        r = int(r)
        g = int(g)
        b = int(b)
    if event == "Update Money":
        # Read the new money value from the textbox
        new_money = values["Money"]

        # Convert the new money value to an integer
        new_money = int(new_money)

        # Write the new money value to the game's memory
        pm.write_int(player + m_iAccountID, new_money)
    if event == "Update Armor":
        # Read the new armor value from the textbox
        new_armor = values["NewArmor"]

        # Convert the new armor value to an integer
        new_armor = int(new_armor)

        # Update the armor value
        pm.write_int(player + m_ArmorValue, new_armor)

        # Update the displayed armor value
        window["Armor"].update(str(new_armor))
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
    if event == "Show Rank":
        t9.start()
    if event == "Debug":
        t10.start()
    if event == "No Recoil":
        t11.start()

window.close()




