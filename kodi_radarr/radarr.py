import asyncio
from aiopyarr.models.host_configuration import PyArrHostConfiguration
from aiopyarr.radarr_client import RadarrClient
from aiopyarr.models.radarr import RadarrMovie
from aiopyarr.models.base import toraw
from aiohttp.client import ClientError, ClientSession, ClientTimeout


class Radarr():
    def __init__(self, settings):
        self.host_configuration = PyArrHostConfiguration(ipaddress=settings["ipaddress"], api_token=settings["api-key"])
        self.client = RadarrClient(host_configuration=self.host_configuration)

    def GetStatus(self):
        """Example usage of aiopyarr."""
        return asyncio.get_event_loop().run_until_complete(self.client.async_get_system_status())

    async def SearchMovieTmdb(self, search_string):
        """Lookup information about movie.
        tmdb: Use TMDB IDs. Set to False to use IMDB.
        """
        result = await self.client._async_request(
            "movie/lookup",
            params={"term": search_string},
            datatype=RadarrMovie,
        )
        print(result[0].tmdbId)
        return result[0]

    def FindRelease(self, radarr_id):
        result = asyncio.get_event_loop().run_until_complete(self.client.async_get_release(radarr_id))
        print("Found {} releases".format(len(result)))
        return result

    async def GetMovieId(self, tmdb_id):
        result = await self.client.async_get_movies(tmdb_id, True)
        print(result[0].tmdbId)
        print(result[0].id)

    def GetAllMovies(self):
        return asyncio.get_event_loop().run_until_complete(self.client.async_get_movies())

    def DownloadRelease(self, indexer_id, release_guid):
        return asyncio.get_event_loop().run_until_complete(self.client.async_download_release(release_guid, indexer_id))


    async def AddMovieByTmdbId(self, tmdb_id):
        root_folders = self.client.async_get_root_folders()
        movie_list = await self.client.async_lookup_movie(tmdb_id, True)
        movie = movie_list[0]
        movie.qualityProfileId = 1
        root_folders = await root_folders
        movie.rootFolderPath = root_folders[0].path
        added_movie = await self.client.async_add_movies(movie)
        return added_movie

    async def AsyncGetStatus(self):
        print(await self.client.async_get_system_status())

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    radarr = Radarr()
    movies = radarr.GetAllMovies()
    print(movies[0].__dict__.keys())
    print(list(map(lambda movie: (movie.title, movie.hasFile), movies)))
    search_string = "Tenet"
    movie = loop.run_until_complete(radarr.SearchMovieTmdb(search_string))
    print("Found movie with id: {}".format(movie.tmdbId))
    added_movie = loop.run_until_complete(radarr.AddMovieByTmdbId(movie.tmdbId))
    print("Added movie with id: {}".format(added_movie.id))
    for release in releases:
        print("Titles: {} Size: {} Seeders: {}". format(release.title, release.size, release.seeders))
