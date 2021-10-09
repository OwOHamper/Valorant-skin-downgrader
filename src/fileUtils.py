import os
import time


class FileUtils():
    def __init__(self):
        self.logs_path = os.path.join(os.getenv('LOCALAPPDATA'), R'VALORANT\Saved\Logs\ShooterGame.log')

    def getLockfile(self):
        try:
            with open(os.path.join(os.getenv('LOCALAPPDATA'), R'Riot Games\Riot Client\Config\lockfile')) as lockfile:
                data = lockfile.read().split(':')
                keys = ['name', 'PID', 'port', 'password', 'protocol']
                return dict(zip(keys, data))
        except FileNotFoundError:
            return None

    def waitForLockfile(self):
        lockfile = None
        while lockfile is None:
            lockfile = self.getLockfile()
            time.sleep(1)
        return lockfile

    def getVersion(self):
        path = self.logs_path
        with open(path, "r", encoding="utf8") as file:
            while True:
                line = file.readline()
                if 'CI server version:' in line:
                    version_without_shipping = line.split('CI server version: ')[1].strip()
                    version = version_without_shipping.split("-")
                    version.insert(2, "shipping")
                    version = "-".join(version)
                    return version


    def getRegion(self):
        path = self.logs_path
        with open(path, "r", encoding="utf8") as file:
            while True:
                line = file.readline()
                if '.a.pvp.net/account-xp/v1/' in line:
                    pd_url = line.split('.a.pvp.net/account-xp/v1/')[0].split('.')[-1]
                elif 'https://glz' in line:
                    glz_url = [(line.split('https://glz-')[1].split(".")[0]),
                               (line.split('https://glz-')[1].split(".")[1])]
                if "pd_url" in locals().keys() and "glz_url" in locals().keys():
                    return [pd_url, glz_url]

    def searchForFlush(self):
        path = self.logs_path
        with open(path, "r", encoding="utf8") as file:
            lines = file.readlines()
            for line in lines:
                if 'Flush completed successfully.' in line:
                    return True
            return False

    def InventoryLoop(self):
        path = self.logs_path
        with open(path, "r") as file:
            first_line = file.readline()
            file.seek(0, os.SEEK_END)
            exit = False
            while True:
                line = ""
                while len(line) == 0 or line[-1] != '\n':
                    tail = file.readline()
                    if tail == "":
                        time.sleep(0.5)
                        continue
                    line += tail
                if "Flush completed successfully." in line:
                    while not exit:
                        file.seek(0, 0)
                        if first_line == file.readline():
                            time.sleep(3)
                        else:
                            file.seek(0, os.SEEK_END)
                            exit = True
                if "[playerLoadoutUpdate]" in line:
                    print("Inventory update!")
                    return True

    def modifyInventory(self, inventory, config):
        newInventory = inventory
        for gunConfig in config[inventory["Subject"]]:
            for gun in range(len(inventory["Guns"])):
                if gunConfig["skinID"] == inventory["Guns"][gun]["SkinID"]:
                    newInventory["Guns"][gun]["SkinLevelID"] = gunConfig["levelID"]
                    newInventory["Guns"][gun]["ChromaID"] = gunConfig["chromaID"]
        return newInventory


