import hashlib
import os

def get_md5_value(string):
    if string:
        m = hashlib.md5(bytes('GgsDdu', encoding='utf-8'))
        m.update(bytes(string, encoding='utf-8'))
        return m.hexdigest()


def rmdir_all(dirPath):
    if not os.path.isdir(dirPath):
        return

    for file in os.listdir(dirPath):
        filePath = os.path.join(dirPath, file)
        if os.path.isfile(filePath):
            os.remove(filePath)
        elif os.path.isdir(filePath):
            rmdir_all(filePath)

    for folder in os.listdir(dirPath):
        os.rmdir(os.path.join(dirPath, folder))
