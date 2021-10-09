import requests
from InquirerPy import prompt
import json


class ConfigUtils():
    def __init__(self, val):
        self.inv = val.get_inventory()
        self.puuid = self.inv.json()["Subject"]
        self.valskins = requests.get("https://valorant-api.com/v1/weapons/skins").json()


    def addToConfig(self, skin_uuid, level_uuid, chroma_uuid):
        try:
            with open("config.json", "r") as file:
                currentConfig = json.load(file)
                newConfig = currentConfig
            if self.puuid in currentConfig.keys():
                #check if skin is already in config.json
                skinAlreadyIn = False
                for i in currentConfig[self.puuid]:
                    if i["skinID"] == skin_uuid:
                        skinAlreadyIn = True

                if not skinAlreadyIn:
                    newConfig[self.puuid].append({"skinID": skin_uuid, "levelID": level_uuid, "chromaID": chroma_uuid})
                else:
                    for i in range(len(currentConfig[self.puuid])):
                        if currentConfig[self.puuid][i]["skinID"] == skin_uuid:
                            newConfig[self.puuid][i]["levelID"] = level_uuid
                            newConfig[self.puuid][i]["chromaID"] = chroma_uuid
            else:
                newConfig.update({self.puuid: []})
                newConfig[self.puuid].append({"skinID": skin_uuid, "levelID": level_uuid, "chromaID": chroma_uuid})



        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("config.json", "w") as file:
                newConfig = {}
                newConfig.update({self.puuid: []})
                newConfig[self.puuid].append({"skinID": skin_uuid, "levelID": level_uuid, "chromaID": chroma_uuid})

        with open("config.json", "w") as file:
            json.dump(newConfig, file)

    def promptSkinName(self):
        q_skin_name = {
            "type": "list",
            "message": "Select skin to downgrade:",
            "choices": [],
        }

        for gun in self.inv.json()["Guns"]:
            for valgun in self.valskins["data"]:
                if gun["SkinID"] == valgun["uuid"]:
                    q_skin_name["choices"].append(valgun["displayName"])

        result = prompt(q_skin_name)
        return result[0]

    def promptSkinLevel(self, choosen_skin):
        q_level_name = {
            "type": "list",
            "message": "Select level to downgrade to:",
            "choices": [],
        }

        for valgun in self.valskins["data"]:
            if valgun["displayName"] == choosen_skin:
                for level in valgun["levels"]:
                    q_level_name["choices"].append(level["displayName"])

        result = prompt(q_level_name)
        return result[0]

    def promptSkinChroma(self, choosen_skin):
        q_chroma_name = {
            "type": "list",
            "message": "Select chroma to set:",
            "choices": [],
        }

        for valgun in self.valskins["data"]:
            if valgun["displayName"] == choosen_skin:
                for chroma in valgun["chromas"]:
                    if "\n" in chroma["displayName"]:
                        chroma_modified = chroma["displayName"].split("\n")[1][1:-1]
                    else:
                        chroma_modified = chroma["displayName"]
                    q_chroma_name["choices"].append(chroma_modified)

        result = prompt(q_chroma_name)
        return result[0]

    def convertNamesToUuids(self, skin_name, level_name, chroma_name):
        for gun in self.valskins["data"]:
            if gun["displayName"] == skin_name:
                skin_uuid = gun["uuid"]
                for chroma in gun["chromas"]:

                    if "\n" in chroma["displayName"]:
                        chroma_modified = chroma["displayName"].split("\n")[1][1:-1]
                    else:
                        chroma_modified = chroma["displayName"]

                    if chroma_name == chroma_modified:
                        chroma_uuid = chroma["uuid"]

                for level in gun["levels"]:
                    if level["displayName"] == level_name:
                        level_uuid = level["uuid"]
                return skin_uuid, level_uuid, chroma_uuid
