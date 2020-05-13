import json


class ConfigHandler:
    config = None
    def __init__(self, configFile):
        # Load config file into config object
        with open (configFile) as cf:
            self.config = json.load(cf)
            # TODO: validate config file

    def getChunkSizes(self):
        l = []
        for f in self.config['fields']:
            l.append(f['width'])
        return l
