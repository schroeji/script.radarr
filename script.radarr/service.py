#!/usr/bin/env python3
import xbmc
import xbmcaddon
import xbmcgui
import asyncio
import time
import traceback
from kodi_radarr.radarr import Radarr
from resources.lib.settings import LoadSettings
from resources.lib.task_queue import TaskQueue

def connection_established_callback(radarr):
    xbmcgui.Dialog().notification("Connection Established", "Successfully connected to {}:{}".format(settings["ipaddress"], settings["port"]), icon=xbmcgui.NOTIFICATION_INFO)
    task_queue = TaskQueue()
    while radarr.is_connected():
        task = task_queue.pop()
        if task is not None:
            try:
                radarr.execute_task(task)
            except Exception as ex:
                xbmc.log("Exception while executing task: ")
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                xbmcgui.Dialog().notification("Connection lost", "Lost connection to Radarr server")
        time.sleep(5)
    xbmcgui.Dialog().notification("Connection lost", "Lost connection to Radarr server")


if __name__ == '__main__':
    monitor = xbmc.Monitor()
    addon = xbmcaddon.Addon()
    xbmc.log("Started Radarr addon", level=xbmc.LOGDEBUG)
    settings = LoadSettings(addon)
    first_try = True
    radarr = Radarr(settings)
    while not monitor.abortRequested():
        connected = radarr.is_connected()
        if connected:
            connection_established_callback(radarr)
            first_try = True
        else:
            if first_try:
                xbmcgui.Dialog().notification("Connection error", "Could not connect to Radarr server", icon=xbmcgui.NOTIFICATION_ERROR)
            first_try = False
        if monitor.waitForAbort(10):
            break
