#-*-coding: utf-8
import logging, sys, os, json, hashlib, datetime

root = str(os.path.dirname(os.path.realpath(__file__)))

def getEncrypeUsingSHA256(sourceFileName, saltFileName, keyColumes, ASK_ID, RSHP_ID):

    saltList = {}
    result = []
    try:
        logging.info("getEncrypeUsingSHA256() - Load salt")
        with open(saltFileName, 'r', encoding='UTF8') as saltFile:
            while True:
                saltLine = saltFile.readline().rstrip('\n')

                if not saltLine: break
                if '#' in saltLine: continue

                values = saltLine.split('\t')

                id = "%s_%s" % (values[0], values[1])
                rand = values[3]

                saltList[id] = rand
                #salt = saltFile.read().replace('\n', '')

        saltFile.close()

        salt = saltList.get("%s_%s" % (ASK_ID, RSHP_ID))
        logging.info("getEncrypeUsingSHA256() - Do encryption(UTF-8)")

        outputFileName = sourceFileName + ".rst"
        outputFile = open(outputFileName, 'w', encoding='UTF8')

        with open(sourceFileName, 'r', encoding='UTF8') as sourceFile:
            while True:
                line = sourceFile.readline().rstrip('\n')
                if not line: break
                data = line.split("\t")

                keyString = ''
                for i in keyColumes:
                    if '-' in data[i]:
                        keyString += str(data[i])[:6] + str(data[i])[7]
                    else:
                        keyString += data[i]

                hexHashValue = hashlib.sha256(salt.encode() + keyString.encode()).hexdigest()
                result.append(hexHashValue)

                outputLine = ''
                for index in range(0, len(data)):
                    if (index not in keyColumes) :
                        outputLine += data[index] + '\t'
                outputLine.rstrip('\t')
                outputFile.write("%s\t%s\n" % (hexHashValue, outputLine))

        sourceFile.close()
        outputFile.close()

    except OSError:
        logging.error("File open error")
        exit()

    return result;

def readJsonFile(fileName):
    try:
        with open( fileName, 'r', encoding='UTF8') as jsonFile:
            jsonData = json.load(jsonFile)
        jsonFile.close()
        return jsonData
    except OSError:
        logging.error("File read error :: " + fileName)
        return None

if __name__ == "__main__":
    # Program argument setting
    #   argument :: dev environment, crawling - date
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    if len(sys.argv) != 5:
        logging.error("argument error")
        logging.error("  allowd argument :: (Encrype Source File) (Salt File) (ASK_ID) (RSHP_ID)")
        logging.error("                     (Source.txt) (Encryped.txt) (Salt.txt) ")
        exit()

    # 환경 설정 파일 로딩
    logging.info("main() - Load config file")
    config = readJsonFile(root + '/../config/config.json')

    # 파라미터 로딩
    logging.info("main() - Load arguments")
    sourceFileName = root + '/..' + config['encrype_source']['file_path'] + '/' + sys.argv[1]
    saltFileName = root + '/..' + config['encrype_source']['salt_path'] + '/' + sys.argv[2]
    keyColumes = config['encrype_source']['key_columes']

    # encrype using SHA256
    logging.info("main() - Do encrype using sha256 with salt")
    encrypeResult = getEncrypeUsingSHA256(sourceFileName, saltFileName, keyColumes, sys.argv[3], sys.argv[4])

    # result print out
    logging.info("main() - Result output")

    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    targetFileName = "%s/..%s/IF_DL_304_%s_%s_TBPKV%s_1_1_%s.txt" % (root, config['encrype_target']['file_path'], sys.argv[3], sys.argv[4], sys.argv[3], date)

    # targetFileName = root + '/..' + config['encrype_target']['file_path'] + '/IF_DL_304_' + sys.argv[3] + "_"
    try:
        with open(targetFileName, 'w', encoding='UTF8') as outputFile:
            for keys in encrypeResult:
                outputFile.write(keys)
                outputFile.write("\n")
        outputFile.close()
    except OSError:
        logging.error("File write error :: " + targetFileName)

