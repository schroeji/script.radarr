#!/usr/bin/env python3

def LoadSettings(addon):
    settings = {}
    settings["port"] = addon.getSettingInt("port")
    settings["api-key"] = addon.getSettingString("api-key")
    settings["ipaddress"] = addon.getSettingString("ipaddress")
    return settings
