import requests
import time
import os


from src import fileUtils
from src import api
from src import configUtils



def main():
    os.system("cls")
    FileUtils = fileUtils.FileUtils()
    lockfile = FileUtils.waitForLockfile()

    version = FileUtils.getVersion()
    region = FileUtils.getRegion()
    val = api.Api(lockfile, region, version)


    cfg = configUtils.ConfigUtils(val)

    while True:
        skin_name = cfg.promptSkinName()
        level_name = cfg.promptSkinLevel(skin_name)
        chroma_name = cfg.promptSkinChroma(skin_name)
        skin_uuid, level_uuid, chroma_uuid = cfg.convertNamesToUuids(skin_name, level_name, chroma_name)
        cfg.addToConfig(skin_uuid, level_uuid, chroma_uuid)
        print("Downgrade saved into config.json!")















if __name__ == '__main__':
    main()
