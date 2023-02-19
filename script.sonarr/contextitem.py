#!/usr/bin/env python3
import sys
import xbmc
import xbmcgui
import xbmcaddon
from resources.lib.task_queue import TaskQueue, create_task

if __name__ == "__main__":
    info_tag_video = sys.listitem.getVideoInfoTag()
    tvdb_id = info_tag_video.getUniqueID("tvdb")
    task_queue = TaskQueue()
    if tvdb_id:
        task_queue.push(create_task("add_show", tvdb_id=tvdb_id))
        xbmc.log(
            "Added add_show task for tvdb_id: {}".format(tvdb_id), level=xbmc.LOGDEBUG
        )
    else:
        title = info_tag_video.getTVShowTitle()
        year = info_tag_video.getYear()
        task_queue.push(create_task("add_show_by_title", title=title, year=year))
        xbmc.log(
            "Added add_show_by_title task for title: {} year: {}".format(title, year),
            level=xbmc.LOGDEBUG,
        )
