#-*-coding: utf-8
import logging, sys, hashlib
import pyUtils

utils = pyUtils.Utils()
# 환경 설정 파일 로딩
config = utils.readJsonFile('/../config/config.json')

def getSaltList(argv):
    saltList = {}
    saltFileName = "%s/..%s/%s" % (utils.root, config['encrypt']['salt_path'], argv[2])

    try:
        logging.info("getEncrypeUsingSHA256() - Load salt")
        with open(saltFileName, 'r', encoding='UTF8') as saltFile:
            while True:
                saltLine = saltFile.readline().rstrip('\n')
                if not saltLine: break
                if saltLine.startswith('#'): continue
                values = saltLine.split('\t')
                id = "%s_%s" % (values[0], values[1])
                rand = values[3]
                saltList[id] = rand
        saltFile.close()
    except OSError:
        logging.error("getSaltList() - File load error")
        exit()

    return saltList

def getEncryptedData(argv, salt):

    logging.info("getEncryptedData() - Do encryption(UTF-8)")

    resultList = []
    sourceFileName = "%s/..%s/%s" % (utils.root, config['encrypt']['source_path'], argv[1])
    keyColumns = config['encrypt']['key_columns']

    try:
        with open(sourceFileName, 'r', encoding='UTF8') as sourceFile:
            while True:
                line = sourceFile.readline().rstrip('\n')
                if not line: break
                if line.startswith('#'):
                    resultList.append( "%s\t%s\n" % ("hashkeys", utils.getDataWithoutTarget(line.split('\t'), keyColumns)) )
                    continue

                data = line.split("\t")

                keyString = ''
                for i in keyColumns:
                    if '-' in data[i]:
                        keyString += str(data[i])[:6] + str(data[i])[7]
                    else:
                        keyString += data[i]

                hexHashValue = hashlib.sha256(salt.encode() + keyString.encode()).hexdigest()
                output = utils.getDataWithoutTarget(data, keyColumns)

                resultList.append("%s\t%s\n" % (hexHashValue, output))

        sourceFile.close()
        return resultList

    except OSError:
        logging.error("File open error")
        exit()

def getEncryptUsingSHA256(argv):

    logging.info("getEncryptUsingSHA256() - Load salt")
    salt = getSaltList(argv).get("%s_%s" % (argv[3], argv[4]))

    logging.info("getEncryptUsingSHA256() - Load data and key generation")
    result = getEncryptedData(argv, salt)

    return result

if __name__ == "__main__" :
    # Program argument setting
    #   argument :: dev environment, crawling - date
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    if len(sys.argv) != 5:
        logging.error("Argument error")
        logging.error("  Allowed argument :: (Encrype Source File) (Salt File) (ASK_ID) (RSHP_ID)")
        logging.error("                          (Source.txt) (Encryped.txt) (Salt.txt) ")
        exit()

    # encrype using SHA256
    logging.info("main() - Do encrype using sha256 with salt")
    encryptedResult = getEncryptUsingSHA256(sys.argv)

    # result print out
    logging.info("main() - File output(key result)")
    targetKeyFileName = "%s/..%s/IF_DL_304_%s_%s_TBPKV%s_1_1_%s.txt" % (utils.root, config['encrypt']['target_key_path'], sys.argv[3], sys.argv[4], sys.argv[3], utils.date)
    utils.writeFiles(targetKeyFileName, encryptedResult, "0")

    logging.info("main() - File output(data result)")
    targetEncryptedFileName = "%s/..%s/%s" % (utils.root, config['encrypt']['target_encrypt_path'], sys.argv[1].replace(".txt", ".ept"))
    utils.writeFiles(targetEncryptedFileName, encryptedResult, "ALL")
