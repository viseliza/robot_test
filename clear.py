import os
from datetime import datetime

def clearDir():
    dn = datetime.now()

    for file in os.listdir("src"):
        if (int(file.split(".")[2]) < dn.year \
            or int(file.split(".")[1]) < dn.month \
            or int(file.split(".")[0]) < dn.day):
            os.remove(f"src/{file}")
