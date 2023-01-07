#!/usr/bin/env python3
import sys
import asyncio
import xbmcgui
import xbmcaddon
from resources.lib.settings import LoadSettings
from resources.lib.task_queue import TaskQueue, create_task

if __name__ == "__main__":
    try:
        tmdb_id = sys.listitem.getUniqueID('tmdb')
    except Exception as e:
        xbmcgui.Dialog().notification('Error', 'Could not retrieve TMDB id for {}'.format(sys.listitem.getLabel()), icon=xbmcgui.NOTIFICATION_ERROR)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    settings = LoadSettings(xbmcaddon.Addon())
    task_queue = TaskQueue()
    task_queue.push(create_task("add_movie", tmdb_id=tmdb_id))
