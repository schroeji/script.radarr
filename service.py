#!/usr/bin/env python3
import xbmc
import xbmcaddon
import xbmcgui
from kodi_radarr.radarr import Radarr
from resources.lib.settings import LoadSettings

if __name__ == '__main__':
    monitor = xbmc.Monitor()
    addon = xbmcaddon.Addon()
    xbmc.log("Started Radarr addon", level=xbmc.LOGDEBUG)
    settings = LoadSettings(addon)
    connected = False
    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break
        try:
            radarr = Radarr(settings)
            status = radarr.GetStatus()
        except Exception as e:
            xbmcgui.Dialog().notification("Connection error", "Could not connect to Radarr server", icon=xbmcgui.NOTIFICATION_ERROR)
