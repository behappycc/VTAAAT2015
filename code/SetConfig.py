import os
import json

class SetConfig:
    def __init__(self):
       os.system("echo setConfig")

    #read info from a json files
    def readJson(self):
        with open("Config.json", "r") as f:
            config = json.load(f)
        return config

if __name__ == '__main__':
    x = SetConfig()
    config = x.readJson()
    print config["sleepTime"]