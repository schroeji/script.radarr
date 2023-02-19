#!/usr/bin/env python3
import sys
import xbmc
import xbmcgui
import xbmcaddon
from resources.lib.task_queue import TaskQueue, create_task

if __name__ == "__main__":
    info_tag_video = sys.listitem.getVideoInfoTag()
    tmdb_id = info_tag_video.getUniqueID("tmdb")
    task_queue = TaskQueue()
    if tmdb_id:
        task_queue.push(create_task("add_movie", tmdb_id=tmdb_id))
        xbmc.log(
            "Added add_movie task for tmdb_id: {}".format(tmdb_id), level=xbmc.LOGDEBUG
        )
    else:
        title = info_tag_video.getTitle()
        year = info_tag_video.getYear()
        task_queue.push(create_task("add_movie_by_title", title=title, year=year))
        xbmc.log(
            "Added add_movie_by_title task for title: {} year: {}".format(title, year),
            level=xbmc.LOGDEBUG,
        )
