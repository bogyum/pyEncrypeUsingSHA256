#-*-coding: utf-8
import logging, sys, os
import pyUtils

utils = pyUtils.Utils()
config = utils.readJsonFile('/../config/config.json')


def loadKeySet(keyFileName) :

    keySet = set()
    fileName = "%s/..%s/%s" % (utils.root, config['join']['key_list_path'], keyFileName)
    try:
        with open(fileName, 'r', encoding='UTF8') as keyFile:
            while True:
                line = keyFile.readline().rstrip('\n').rstrip('\t')

                if not line: break
                if line.startswith('#'): continue

                keySet.add(line)
        keyFile.close()
    except IOError:
        logging.error("File load error : " + keyFileName)

    return keySet

def getDataList(keySet, headerFileName, encryptedFileName):

    result = []
    header = "%s/..%s/%s" % (utils.root, config['join']['header_path'], headerFileName)
    try:
        with open(header, 'r', encoding='UTF8') as hFile:
            while True:
                line = hFile.readline().rstrip('\n')

                if not line: break
                if line.startswith('#'): continue

                result.append(line)
        hFile.close()
    except IOError:
        logging.error("File load error : " + headerFileName)

    encrypted = "%s/..%s/%s" % (utils.root, config['join']['data_path'], encryptedFileName)
    try:
        with open(encrypted, 'r', encoding='UTF8') as eFile:
            while True:
                line = eFile.readline().rstrip('\n')

                if not line: break
                if line.startswith('#'): continue

                if keySet.__contains__( line.split('\t')[0] ) :
                    result.append(line)
        eFile.close()
    except IOError:
        logging.error("File load error : " + encryptedFileName)
        exit()

    return result

if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    if len(sys.argv) != 5:
        logging.error("Argument error")
        logging.error("  Allowed argument :: (Target keys file) (Header file) (Target data file) (Final result file")
        exit()

    logging.info("main() - Loading key list")
    keySet = loadKeySet(sys.argv[1])

    logging.info("main() - Join table by key list")
    result4JoinedData = getDataList(keySet, sys.argv[2], sys.argv[3])

    logging.info("main() - File output")
    writeFileName = "%s/..%s/%s" % (utils.root, config['join']['target_path'], sys.argv[4])
    utils.writeFiles(writeFileName, result4JoinedData, "ALL")
