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
    handle = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(handle, 0)
    tray = systray.Systray(handle)
    tray.closed = True

    tray = Thread(target=tray.loop)
    tray.start()

    FileUtils = fileUtils.FileUtils()
    lockfile = FileUtils.waitForLockfile()

    version = FileUtils.getVersion()
    region = FileUtils.getRegion()
    val = api.Api(lockfile, region, version)






    try:
        with open("config.json", "r") as file:
            config = json.load(file)
            inv = val.get_inventory()
            valskins = requests.get("https://valorant-api.com/v1/weapons/skins").json()
            message_printed = False

            for gun in config[inv.json()["Subject"]]:
                for valgun in valskins["data"]:
                    if gun["skinID"] == valgun["uuid"]:
                        for level in valgun["levels"]:
                            if level["uuid"] == gun["levelID"]:
                                rgb_color = val.tierDict[valgun["contentTierUuid"]]
                                if not message_printed:
                                    print("Currently downgrading skins:")
                                    message_printed = True
                                print("   " + color(level["displayName"], fore=rgb_color))

    except (FileNotFoundError, KeyError):
        print("Customize downgrader with config.py!")
        print("This program will close in 5 seconds!")
        time.sleep(5)
        os._exit(1)

    inv = val.get_inventory()
    with open("config.json", "r") as file:
        config = json.load(file)
    modifiedInv = FileUtils.modifyInventory(inv.json(), config)
    val.put_inventory(modifiedInv)

    while True:
        FileUtils.InventoryLoop()
        inv = val.get_inventory()
        with open("config.json", "r") as file:
            config = json.load(file)
        modifiedInv = FileUtils.modifyInventory(inv.json(), config)
        val.put_inventory(modifiedInv)





if __name__ == '__main__':
    main()
