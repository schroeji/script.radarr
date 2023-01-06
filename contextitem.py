#!/usr/bin/env python3
import sys
import asyncio
import xbmcgui
import xbmcaddon
from kodi_radarr.radarr import Radarr
from resources.lib.settings import LoadSettings

if __name__ == "__main__":
    try:
        tmdb_id = sys.listitem.getUniqueID('tmdb')
    except Exception as e:
        xbmcgui.Dialog().notification('Error', 'Could not retrieve TMDB id for {}'.format(sys.listitem.getLabel()), icon=xbmcgui.NOTIFICATION_ERROR)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        settings = LoadSettings(xbmcaddon.Addon())
        radarr = Radarr(settings)
        movie = radarr.AddMovieByTmdbId(tmdb_id)
        movie = asyncio.get_event_loop().run_until_complete(movie)
        xbmcgui.Dialog().notification('Radarr', 'Successfully added movie: {}'.format(movie.title))
    except Exception as e:
        xbmcgui.Dialog().notification('Radarr error', 'Could not add movie.', icon=xbmcgui.NOTIFICATION_ERROR)
        print(e)
