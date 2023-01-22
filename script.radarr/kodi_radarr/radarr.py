import xbmcgui
from pyarr import RadarrAPI

class Radarr():
    def __init__(self, settings):
        url = "http://{}:{}".format(settings["ipaddress"], settings["port"])
        self.client = RadarrAPI(url, settings['api-key'])

    def GetStatus(self):
        """Example usage of aiopyarr."""
        return self.client.get_system_status()

    def SearchMovieTmdb(self, search_string):
        """Lookup information about movie.
        tmdb: Use TMDB IDs. Set to False to use IMDB.
        """
        return self.client.lookup_movie(search_string)[0]

    def FindRelease(self, radarr_id):
        params = {"movieId" : radarr_id}
        result = self.client.request_get("release", self.client.ver_uri, params)
        return result

    def GetMovieId(self, tmdb_id):
        return self.client.get_movie(tmdb_id)

    def GetAllMovies(self):
        return self.client.get_movie()

    def DownloadRelease(self, indexer_id, release_guid):
        params = {"indexerId" : indexer_id,
                  "guid" : release_guid}
        return self.client.request_post("release", self.client.ver_uri, data=params)

    def GetIndexers(self):
        return self.client.get_indexer()

    def DeleteMovie(self, id):
        self.client.del_movie(id)

    def AddMovieByTmdbId(self, tmdb_id):
        root_folder = self.client.get_root_folder()[0]["path"]
        quality_profile_id = 1
        added_movie = self.client.add_movie(tmdb_id, quality_profile_id, root_folder, monitored=False, search_for_movie=False)
        if added_movie != None:
            xbmcgui.Dialog().notification('Radarr', 'Successfully added movie: {}'.format(added_movie["title"]))
        return added_movie


    def is_connected(self):
        try:
            status = self.GetStatus()
            connected = True
        except Exception as e:
            connected = False
        return connected

    def execute_task(self, task):
        if task["action"] == "download_release":
            self.DownloadRelease(task["indexer_id"], task["release_guid"])
        elif task["action"] == "add_movie":
            self.AddMovieByTmdbId(task["tmdb_id"])


if __name__ == "__main__":
    settings = {
        "ipaddress" : "127.0.0.1",
        "port"  : "7878",
        "api-key" : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
    radarr = Radarr(settings)
    movies = radarr.GetAllMovies()
    # print(movies[0].keys())
    # print(list(map(lambda movie: (movie["title"], movie["hasFile"]), movies)))
    # search_string = "the good, the bad"
    # movie = radarr.SearchMovieTmdb(search_string)
    # print("Found movie with id: {}".format(movie["tmdbId"]))
    # added_movie = radarr.AddMovieByTmdbId(movie["tmdbId"])
    # print("Added movie with id: {}".format(added_movie["id"]))
    movies = radarr.GetAllMovies()
    # print(movies)
    releases = radarr.FindRelease(26)
    print(releases)
    indexer = radarr.GetIndexers()[0]["id"]
    release = radarr.DownloadRelease(indexer, releases[0]["guid"])
    print(release)
    # print("Added release {}".format(release.url))
