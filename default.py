import xbmc
import xbmcgui
import xbmcaddon
from kodi_radarr.radarr import Radarr

# create a class for your addon, we need this to get info about your addon
ADDON = xbmcaddon.Addon()
# get the full path to your addon, decode it to unicode to handle special (non-ascii) characters in the path
CWD = ADDON.getAddonInfo('path') # for kodi 19 and up..

def LoadSettings(addon):
    settings = {}
    settings["port"] = addon.getSettingInt("port")
    settings["api-key"] = addon.getSettingString("api-key")
    settings["ipaddress"] = addon.getSettingString("ipaddress")
    return settings

# add a class to create your xml based window
class GUI(xbmcgui.WindowXML):
    # until now we have a blank window, the onInit function will parse your xml file
    def onInit(self):
        # select a view mode, '50' in our case, as defined in the skin file
        xbmc.executebuiltin('Container.SetViewMode(50)')
        # define a temporary list where we are going to add all the listitems to
        # radarr = Radarr()
        # movies = radarr.GetAllMovies()
        # listitems = list(map(lambda movie: movie.title, movies))
        listitem1 = xbmcgui.ListItem('Item')
        listitem2 = xbmcgui.ListItem(str(ADDON.))
        # by default the built-in container already contains one item, the 'up' (..) item, let's remove that one
        self.clearList()
        # now we are going to add all the items we have defined to the (built-in) container
        self.addItem(listitem1)
        self.addItem(listitem2)
        # give kodi a bit of (processing) time to add all items to the container
        xbmc.sleep(100)
        # this puts the focus on the top item of the container
        self.setFocusId(self.getCurrentContainerId())

# this is the entry point of your addon, execution of your script will start here
if (__name__ == '__main__'):
    # define your xml window and pass these five arguments (more optional items can be passed as well):
    # 1 'the name of the xml file for this window', 
    # 2 'the path to your addon',
    # 3 'the name of the folder that contains the skin',
    # 4 'the name of the folder that contains the skin xml files'
    # 5 set to True for a media window (a single list window that will list music / videos / pictures), set to False otherwise
    # 6 [optional] if you need to pass additional data to your window, simply add them to the list
    # you'll have to add them as key=value pairs: key1=value1, key2=value2, etc...
    ui = GUI('script-radarr.xml', CWD, 'default', '1080i', True)
    # now open your window. the window will be shown until you close your addon
    ui.doModal()
    # window closed, now cleanup a bit: delete your window before the script fully exits
    del ui
