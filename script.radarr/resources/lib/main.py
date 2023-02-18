#!/usr/bin/env python3

import asyncio
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import sys
import traceback
import threading
from kodi_radarr.radarr import Radarr
from urllib.parse import urlencode, parse_qsl
from resources.lib.settings import LoadSettings
from resources.lib.task_queue import TaskQueue, create_task

__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.
    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(__url__, urlencode(kwargs))



class RadarrMenu():
    def __init__(self):
        self.addon = xbmcaddon.Addon()
        self.settings = LoadSettings(self.addon)
        self.task_queue = TaskQueue()
        self.radarr = Radarr(self.settings)
        if not self.radarr.is_connected():
            self.radarr = None
            xbmcgui.Dialog().notification("Connection error", "Could not connect to Radarr server")


    def Router(self, paramstring):
        """
        Router function that calls other functions
        depending on the provided paramstring
        :param paramstring: URL encoded plugin paramstring
        :type paramstring: str
        """
        # Parse a URL-encoded paramstring to the dictionary of
        # {<parameter>: <value>} elements
        print(paramstring)
        params = dict(parse_qsl(paramstring))
        # Check the parameters passed to the plugin
        if params:
            if params['action'] == 'movie_details':
                self.MovieDetails(params['radarr_id'])
            elif params['action'] == 'list_releases':
                self.ListReleases(params['radarr_id'])
            elif params['action'] == 'download_release':
                xbmc.log("Download release {}".format(params['release_guid']), level=xbmc.LOGDEBUG)
                self.DownloadRelease(params['indexer_id'], params['release_guid'])
            else:
                # If the provided paramstring does not contain a supported action
                # we raise an exception. This helps to catch coding errors,
                # e.g. typos in action names.
                raise ValueError('Invalid paramstring: {}'.format(paramstring))
        else:
            # If the plugin is called from Kodi UI without any parameters,
            # display the list of video categories
            self.ListMovies()

    def MovieDetails(self, radarr_id):
        print("Movie Details")
        self.ListReleases(radarr_id)

    def CreateMovieDetailUrl(self, radarr_movie):
        url = get_url(action='movie_details', radarr_id=radarr_movie["id"])
        return url

    def CreateMovieContextMenu(self, radarr_movie):
        items = [("Details", "RunPlugin({})".format(self.CreateMovieDetailUrl(radarr_movie)))]
        print(items)
        return items

    def CreateDownloadReleaselUrl(self, release):
        url = get_url(action='download_release', indexer_id=release["indexerId"], release_guid=release["guid"])
        return url

    def ListMovies(self):
        if self.radarr:
            movies = self.radarr.GetAllMovies()
            listitems = []
            for movie in movies:
                listitem = xbmcgui.ListItem(movie["title"])
                listitem.addContextMenuItems(self.CreateMovieContextMenu(movie))
                listitems.append((self.CreateMovieDetailUrl(movie), listitem, True))
                print(listitems[-1][0])
            xbmcplugin.addDirectoryItems(__handle__, listitems, len(listitems))
            # Add a sort method for the virtual folder items (alphabetically, ignore articles)
            xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
            # Finish creating a virtual folder.
            xbmcplugin.endOfDirectory(__handle__)

    def ListReleases(self, radarr_id):
        releases = self.radarr.FindRelease(radarr_id)
        listitems = [(self.CreateDownloadReleaselUrl(release), xbmcgui.ListItem(release["title"]), True) for release in releases]
        xbmcplugin.addDirectoryItems(__handle__, listitems, len(listitems))
        # Add a sort method for the virtual folder items (alphabetically, ignore articles)
        xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(__handle__)

    def DownloadRelease(self, indexer_id, release_guid):
        self.task_queue.push(create_task("download_release", indexer_id=indexer_id, release_guid=release_guid))



def CreateRadarrMenu(argv):
    menu = RadarrMenu()
    menu.Router(argv[2][1:])
