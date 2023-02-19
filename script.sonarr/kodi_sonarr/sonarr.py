import xbmcgui
import xbmc
from pyarr import SonarrAPI


class Sonarr:
    def __init__(self, settings):
        url = "http://{}:{}".format(settings["ipaddress"], settings["port"])
        self.client = SonarrAPI(url, settings["api-key"])

    def GetStatus(self):
        """Example usage of aiopyarr."""
        return self.client.get_system_status()

    def SearchShowTvdb(self, search_string):
        """Lookup information about movie."""
        return self.client.lookup_series(search_string)[0]

    def FindRelease(self, radarr_id):
        params = {"movieId": radarr_id}
        result = self.client.request_get("release", self.client.ver_uri, params)
        return result

    def GetShow(self, tvdb_id):
        return self.client.get_series(tvdb_id)

    def GetAllShows(self):
        return self.client.get_series()

    def DownloadRelease(self, indexer_id, release_guid):
        params = {"indexerId": indexer_id, "guid": release_guid}
        return self.client.request_post("release", self.client.ver_uri, data=params)

    def GetIndexers(self):
        return self.client.get_indexer()

    def DeleteShow(self, sonarr_id):
        self.client.del_series(sonarr_id)

    def AddShowByTvdbId(self, tvdb_id):
        root_folder = self.client.get_root_folder()[0]["path"]
        quality_profile_id = 1
        added_show = self.client.add_series(
            tvdb_id,
            quality_profile_id,
            root_folder,
            season_folder=True,
            monitored=False,
            search_for_missing_episodes=False,
        )
        if added_show:
            xbmcgui.Dialog().notification(
                "Sonarr", "Successfully added show: {}".format(added_show["title"])
            )

        return added_show

    def is_connected(self):
        try:
            status = self.GetStatus()
            connected = True
        except Exception as e:
            connected = False
        return connected

    def add_show_by_title(self, title, year=None):
        if year:
            show = self.SearchShowTvdb("{} {}".format(title, year))
        else:
            show = self.SearchShowTvdb(title)
        if show:
            return self.AddShowByTvdbId(show["tvdbId"])

    def execute_task(self, task):
        if task["action"] == "download_release":
            self.DownloadRelease(task["indexer_id"], task["release_guid"])
        elif task["action"] == "add_show":
            self.AddShowByTvdbId(task["tvdb_id"])
        elif task["action"] == "add_show_by_title":
            self.add_show_by_title(task["title"], task["year"])
        else:
            xbmc.log("Unknown action {}".format(task["action"]), level=xbmc.LOGDEBUG)


if __name__ == "__main__":
    settings = {
        "ipaddress": "127.0.0.1",
        "port": "7878",
        "api-key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    }
    sonarr = Sonarr(settings)
    shows = sonarr.GetAllShows()
    # print(movies[0].keys())
    # print(list(map(lambda movie: (movie["title"], movie["hasFile"]), movies)))
    # search_string = "the good, the bad"
    # movie = radarr.SearchMovieTmdb(search_string)
    # print("Found movie with id: {}".format(movie["tmdbId"]))
    # added_movie = radarr.AddMovieByTmdbId(movie["tmdbId"])
    # print("Added movie with id: {}".format(added_movie["id"]))
    # print(movies)
    releases = sonarr.FindRelease(26)
    print(releases)
    indexer = sonarr.GetIndexers()[0]["id"]
    print(indexer)
    # print("Added release {}".format(release.url))
