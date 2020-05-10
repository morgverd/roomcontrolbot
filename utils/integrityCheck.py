import hashlib, os
print("[INTEGRITY] Integrity Check function imported")
def getIntegrityKey(dirpath):
    def getListOfFiles(dirName):
        listOfFile = os.listdir(dirName)
        allFiles = list()
        for entry in listOfFile:
            fullPath = os.path.join(dirName, entry)
            if os.path.isdir(fullPath):
                allFiles = allFiles + getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)
        return allFiles
    listOfFilesArr = getListOfFiles(dirpath)
    filesString = "||=||".join(listOfFilesArr)
    bannnedStrings = [".txt", ".mp4", ".git", ".png", ".jpeg", ".jpg", ".json", ".example", "gitFixIntegrity.py"]
    for bStr in bannnedStrings:
        filesString = filesString.replace(str(bStr), ".errfile")
    listOfFiles = filesString.split("||=||")
    validFiles = list()
    for filepath in listOfFiles:
        if os.path.isfile(filepath):
            validFiles.append(str(filepath))
    allDataString = ""
    for filepath in validFiles:
        try:
            f = open(filepath, "r")
            allDataString += ((f.read()).replace("\n", ""))
        except UnicodeDecodeError:
            pass
    keyObj = hashlib.md5(allDataString.encode())
    return (keyObj.hexdigest())