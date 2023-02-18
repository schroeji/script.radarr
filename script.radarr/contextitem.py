#!/usr/bin/env python3
import sys
import xbmc
import xbmcgui
import xbmcaddon
from kodi_radarr.radarr import Radarr
from resources.lib.settings import LoadSettings
from resources.lib.task_queue import TaskQueue, create_task

if __name__ == "__main__":
    info_tag_video = sys.listitem.getVideoInfoTag()
    tmdb_id = info_tag_video.getUniqueID('tmdb')
    task_queue = TaskQueue()
    if tmdb_id is not None and tmdb_id is not "":
        task_queue.push(create_task("add_movie", tmdb_id=tmdb_id))
    else:
        settings = LoadSettings(xbmcaddon.Addon())
        radarr = Radarr(settings)
        title = info_tag_video.getTitle()
        year = info_tag_video.getYear()
        xbmc.log("title {} year {}".format(title, year), level=xbmc.LOGDEBUG)
        if year is not None:
            movie = radarr.SearchMovieTmdb("{} {}".format(title, year))
        else:
            movie = radarr.SearchMovieTmdb(title)
        tmdb_id = movie["tmdbId"]
    task_queue.push(create_task("add_movie", tmdb_id=tmdb_id))
    xbmc.log("Added add_movie task for tmdb_id: {}".format(tmdb_id), level=xbmc.LOGDEBUG)
