#-*-coding: utf-8
import logging, sys, os, json, hashlib

root = str(os.path.dirname(os.path.realpath(__file__)))

def getEncrypeUsingSHA256(sourceFileName, saltFileName, keyColumes):

    salt = ''
    result = []
    try:
        logging.info("getEncrypeUsingSHA256() - Load salt")
        with open(saltFileName, 'r') as saltFile:
            salt = saltFile.read().replace('\n', '')
        saltFile.close()

        logging.info("getEncrypeUsingSHA256() - Do encryption")
        with open(sourceFileName, 'r', encoding='UTF8') as sourceFile:
            while True:
                line = sourceFile.readline()
                if not line: break
                data = line.split("\t")

                keyString = data[keyColumes[0]] + data[keyColumes[1]] + data[keyColumes[2]]
                result.append(hashlib.sha256( salt.encode() + keyString.encode()).hexdigest())
        sourceFile.close()

    except OSError:
        logging.error("File open error")
        exit()

    return result;

def readJsonFile(fileName):
    try:
        with open( fileName, 'r') as jsonFile:
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

    if len(sys.argv) != 4:
        logging.error("argument error")
        logging.error("  allowd argument :: (Encrype Source File) (Salt File) (Encrype Target File)")
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
    encrypeResult = getEncrypeUsingSHA256(sourceFileName, saltFileName, keyColumes)

    # result print out
    logging.info("main() - Result output")
    targetFileName = root + '/..' + config['encrype_target']['file_path'] + '/' + sys.argv[3]
    try:
        with open(targetFileName, 'w') as outputFile:
            for keys in encrypeResult:
                outputFile.write(keys)
                outputFile.write("\n")
        outputFile.close()
    except OSError:
        logging.error("File write error :: " + targetFileName)

