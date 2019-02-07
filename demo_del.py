import os
import re
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
def del_pic():
    s = os.listdir('./images')
    for i in s:
        if (re.findall('(^\d+\.jpg)|(^\d+\.gif)',i)):
            file_path = os.path.join(BASE_DIR, 'images',i)
            os.remove(file_path)
            # print(file_path)

del_pic()