import requests
from colorama import Fore
import time
import os
os.system("cls")
print(Fore.LIGHTGREEN_EX + "[!] Getting latest offsets from Hazedumper")
time.sleep(1)
###OFFSETST###
offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get( offsets ).json()
m_clrRender = int(response["netvars"]["m_clrRender"] )
m_iObserverMode = int(response["netvars"]["m_iObserverMode"] )
m_nFallbackStatTrak = int(response["netvars"]["m_nFallbackStatTrak"] )
m_hMyWeapons = int(response["netvars"]["m_hMyWeapons"] )
m_szCustomName = (0x304C)
m_iCompetitiveWins = int(response["netvars"]["m_iCompetitiveWins"] )
m_iItemIDHigh = int(response["netvars"]["m_iItemIDHigh"] )
m_nFallbackPaintKit = int(response["netvars"]["m_nFallbackPaintKit"] )
m_iItemDefinitionIndex = int(response["netvars"]["m_iItemDefinitionIndex"] )
m_flFallbackWear = int(response["netvars"]["m_flFallbackWear"] )
dwEntityList = int( response["signatures"]["dwEntityList"] )
dwGlowObjectManager = int( response["signatures"]["dwGlowObjectManager"] )
m_iGlowIndex = int( response["netvars"]["m_iGlowIndex"] )
m_iTeamNum = int( response["netvars"]["m_iTeamNum"] )
dwForceJump = int( response["signatures"]["dwForceJump"] )
dwLocalPlayer = int( response["signatures"]["dwLocalPlayer"] )
m_fFlags = int( response["netvars"]["m_fFlags"] )
dwForceAttack = int( response["signatures"]["dwForceAttack"] )
m_iCrosshairId = int( response["netvars"]["m_iCrosshairId"] )
m_flFlashMaxAlpha = int( response["netvars"]["m_flFlashMaxAlpha"] )
m_iDefaultFOV = (0x333C)
dwClientState = int( response["signatures"]["dwClientState"] )
m_iHealth = int( response["netvars"]["m_iHealth"] )
dwViewMatrix = int( response["signatures"]["dwViewMatrix"] )
m_dwBoneMatrix = int( response["netvars"]["m_dwBoneMatrix"] )
dwClientState_ViewAngles = int( response["signatures"]["dwClientState_ViewAngles"] )
m_vecOrigin = int( response["netvars"]["m_vecOrigin"] )
m_vecViewOffset = int( response["netvars"]["m_vecViewOffset"] )
dwbSendPackets = int( response["signatures"]["dwbSendPackets"] )
dwInput = int( response["signatures"]["dwInput"] )
clientstate_net_channel = int( response["signatures"]["clientstate_net_channel"] )
clientstate_last_outgoing_command = int( response["signatures"]["clientstate_last_outgoing_command"] )
m_bSpotted = int( response["netvars"]["m_bSpotted"] )
m_iShotsFired = int( response["netvars"]["m_iShotsFired"] )
m_aimPunchAngle = int( response["netvars"]["m_aimPunchAngle"] )
m_bGunGameImmunity = int( response["netvars"]["m_bGunGameImmunity"] )
m_bIsDefusing = int( response["netvars"]["m_bIsDefusing"] )
m_bDormant = int( response["signatures"]["m_bDormant"] )
dwClientState_PlayerInfo = int( response["signatures"]["dwClientState_PlayerInfo"] )
dwPlayerResource = int( response["signatures"]["dwPlayerResource"] )
m_iCompetitiveRanking = int( response["netvars"]["m_iCompetitiveRanking"] )
m_iAccountID = int( response["netvars"]["m_iAccountID"] )
m_ArmorValue = int( response["netvars"]["m_ArmorValue"] )



print(Fore.LIGHTGREEN_EX + "[!] Done, starting cheat")
time.sleep(0.5)
os.system("cls")
import pymem.process

pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
player = pm.read_uint(client + dwLocalPlayer)
localTeam = pm.read_uint(player + m_iTeamNum)
glow_manager = pm.read_int(client + dwGlowObjectManager)
crosshairID = pm.read_int(player + m_iCrosshairId)
getTeam = pm.read_int(client + dwEntityList + (crosshairID - 1) * 0x10)
localTeam = pm.read_int(player + m_iTeamNum)
crosshairTeam = pm.read_int(getTeam + m_iTeamNum)