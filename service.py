#!/usr/bin/env python3
import xbmc
import xbmcaddon
import xbmcgui
import asyncio
from kodi_radarr.radarr import Radarr
from resources.lib.settings import LoadSettings

async def push_cached_commands(queue, radarr):
    pass


if __name__ == '__main__':
    monitor = xbmc.Monitor()
    addon = xbmcaddon.Addon()
    xbmc.log("Started Radarr addon", level=xbmc.LOGDEBUG)
    settings = LoadSettings(addon)
    connected = None
    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break
        try:
            radarr = Radarr(settings)
            status = radarr.GetStatus()
            if connected != True:
                xbmcgui.Dialog().notification("Connection Established", "Successfully connected to {}:{}".format(settings["ipaddress"], settings["port"]), icon=xbmcgui.NOTIFICATION_INFO)
            connected = True
        except Exception as e:
            if connected != False:
                xbmcgui.Dialog().notification("Connection error", "Could not connect to Radarr server", icon=xbmcgui.NOTIFICATION_ERROR)
            connected = False
