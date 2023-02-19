#!/usr/bin/env python3
import xbmc
import xbmcaddon
import xbmcgui
import asyncio
import time
import traceback
from kodi_sonarr.sonarr import Sonarr
from resources.lib.settings import LoadSettings
from resources.lib.task_queue import TaskQueue


def connection_established_callback(sonarr):
    xbmcgui.Dialog().notification(
        "Connection Established",
        "Successfully connected to {}:{}".format(
            settings["ipaddress"], settings["port"]
        ),
        icon=xbmcgui.NOTIFICATION_INFO,
    )
    task_queue = TaskQueue()
    while sonarr.is_connected():
        task = task_queue.pop()
        if task is not None:
            try:
                sonarr.execute_task(task)
            except Exception as ex:
                xbmc.log("Exception while executing task: ")
                traceback.print_exception(type(ex), ex, ex.__traceback__)
                xbmcgui.Dialog().notification(
                    "Connection lost", "Lost connection to Sonarr server"
                )
        time.sleep(5)
    xbmcgui.Dialog().notification("Connection lost", "Lost connection to Sonarr server")


if __name__ == "__main__":
    monitor = xbmc.Monitor()
    addon = xbmcaddon.Addon()
    xbmc.log("Started Sonarr addon", level=xbmc.LOGDEBUG)
    settings = LoadSettings(addon)
    first_try = True
    sonarr = Sonarr(settings)
    while not monitor.abortRequested():
        connected = sonarr.is_connected()
        if connected:
            connection_established_callback(sonarr)
            first_try = True
        else:
            if first_try:
                xbmcgui.Dialog().notification(
                    "Connection error",
                    "Could not connect to Sonarr server",
                    icon=xbmcgui.NOTIFICATION_ERROR,
                )
            first_try = False
        if monitor.waitForAbort(10):
            break
