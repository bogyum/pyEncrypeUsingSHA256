import json, logging, os, datetime

class Utils:

    def __init__(self):
        self.root = str(os.path.dirname(os.path.realpath(__file__)))
        self.date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def readJsonFile(self, fileName):
        try:
            with open( self.root + fileName, 'r', encoding='UTF8') as jsonFile:
                jsonData = json.load(jsonFile)
            jsonFile.close()
            return jsonData
        except OSError:
            logging.error("File read error :: " + fileName)
            return None

    def getDataWithoutTarget(self, data, keyColumns):
        output = ""
        for index in range(0, len(data)):
            if (index not in keyColumns) :
                output += data[index] + '\t'
        output.rstrip('\t')
        return output

    def getDataWithTarget(self, data, keyColumns):
        output = ''
        for index in range(0, len(data)):
            if ( index in map(int, keyColumns)) :
                output += data[index] + '\t'
        output.rstrip('\t')
        return output

    def writeFiles(self, fileName, data, target):
        try:
            with open(fileName, 'w', encoding='UTF8') as outputFile:
                for line in data:
                    dataList = line.split('\t')

                    if ( target == 'ALL' ):
                        outputFile.write(line.rstrip('\t') + '\n')
                    else:
                        outputFile.write( self.getDataWithTarget(dataList, target.split('\t')) + '\n' )
            outputFile.close()
        except OSError:
            logging.error("File write error :: " + fileName)