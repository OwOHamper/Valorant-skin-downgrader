import json
import os
import time

import requests
from colr import color
import ctypes
from threading import Thread

from src import fileUtils
from src import api
from src import systray


def main():
    FileUtils = fileUtils.FileUtils()
    lockfile = FileUtils.waitForLockfile()

    version = FileUtils.getVersion()
    region = FileUtils.getRegion()
    val = api.Api(lockfile, region, version)


    handle = ctypes.windll.kernel32.GetConsoleWindow()
    tray = systray.Systray(handle)

    tray = Thread(target=tray.loop)
    tray.start()
    # tray.loop()

    try:
        with open("config.json", "r") as file:
            config = json.load(file)
            inv = val.get_inventory()
            valskins = requests.get("https://valorant-api.com/v1/weapons/skins").json()
            print("Currently downgrading skins:")
            for gun in config[inv.json()["Subject"]]:
                for valgun in valskins["data"]:
                    if gun["skinID"] == valgun["uuid"]:
                        for level in valgun["levels"]:
                            if level["uuid"] == gun["levelID"]:
                                rgb_color = val.tierDict[valgun["contentTierUuid"]]
                                print("   " + color(level["displayName"], fore=rgb_color))
    except FileNotFoundError:
        print("Customize downgrader with config.py!")
        print("This program will close in 5 seconds!")
        time.sleep(5)
        os._exit(1)

    while True:
        FileUtils.InventoryLoop()
        inv = val.get_inventory()
        with open("config.json", "r") as file:
            config = json.load(file)
        modifiedInv = FileUtils.modifyInventory(inv.json(), config)
        val.put_inventory(modifiedInv)





if __name__ == '__main__':
    main()
