import logging, json, glob

class Utils:

    def getDictionary(self, key, value ):
        jsonDict = {}
        jsonDict[key] = value
        return jsonDict

    def getDirFileList(self, path):
        fileList = glob.glob(path + "/*")
        jsonFileList = [file for file in fileList]
        return jsonFileList

    def readJsonFile(self, fileName):
        try:
            with open( fileName, 'r') as jsonFile:
                jsonData = json.load(jsonFile)
            jsonFile.close()
            return jsonData
        except OSError:
            logging.error("File read error :: " + fileName)
            return None

    def writeJsonFile(self, result, fileName):
        try:
            with open( fileName, 'w') as jsonFile:
                jsonFile.write( json.dumps(result, sort_keys=True, indent=4))
            jsonFile.close()
        except OSError:
            logging.error("File write error :: " + fileName)