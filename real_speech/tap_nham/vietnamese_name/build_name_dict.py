# https://gist.github.com/thuandt/3421905

import re


def no_accent_vietnamese(s):
    # s = s.decode('utf-8')
    s=s.lower()
    s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(u'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(u'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(u'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(u'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(u'[ìíịỉĩ]', 'i', s)
    s = re.sub(u'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(u'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(u'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(u'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(u'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(u'Đ', 'D', s)
    s = re.sub(u'đ', 'd', s)
    return s #s.encode('utf-8').lower()


from collections import defaultdict
import os


def load_name_dict() -> dict:
    newdict = defaultdict(list)
    list_name=[]
    with open(f"{os.path.dirname(__file__)}/female.txt", 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            list_name.append(line)

    with open(f"{os.path.dirname(__file__)}/male.txt", 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            list_name.append(line)
    list_name=set(list_name)
    for name in list_name:
        newdict[no_accent_vietnamese(name)].append(name)
    return newdict


