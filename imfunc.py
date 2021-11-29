from PIL import Image
from imagehash import average_hash, phash
import numpy as np
import os


def supported(format: list, path: str):
    for i in format:
        if path.endswith(i):
            return True
    return False

def assemble(name, path, length):
    path = "| " + path
    nl = len(name)
    pl = len(path)
    return name + ' '*(length-nl-pl) + path


def greyscale_PAL(c: list) -> int:
    '''
    RGB в оттенок серого.
    '''
    return int(0.299*c[0] + 0.587*c[1] + 0.114*c[2])


def greyscale_HDTV(c: list) -> int:
    '''
    RGB в оттенок серого.
    '''
    return int(0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2])


def scan(path: str, format: list):
    res = {}
    for name in os.listdir(path):
        if supported(format, name):
            p = os.path.join(path, name)
            res[name] = [p]
    return res.copy()


def scan_rec(path: str, format: list):
    res = {}
    for folder in list(os.walk(path)):
        for name in folder[2]:
            if supported(format, name):
                p = os.path.join(folder[0], name)
                res[name] = [p]
    return res.copy()


def sko(image, size=64, func=greyscale_PAL, prec=3) -> float:
    img = image.resize((size, size))
    values = [func(i) for i in img.getdata()]
    n = len(values)
    res = np.sqrt(n/(n-1)*np.std(values)**2)
    return round(res, prec)


def cmp_sko(target: float, other: float) -> float:
    return np.abs(1 - other/target)*100


class scanner:
    def __init__(self, target_path: str, folder_path: str, formats: list):
        self.folder = folder_path
        self.image = target_path
        self.format = formats.copy()
        self.info = {}
    
    def scan(self, rec: bool):
        if rec:
            self.info = scan_rec(self.folder, self.format)
        else:
            self.info = scan(self.folder, self.format)
        for i in self.info.keys():
            print(i)
    
    def calc(self, func):
        for name, info in self.info.items():
            img = Image.open(info[0])
            self.info[name].append(func(img))
    
    def find(self, func, dist=5, rec=False):
        self.scan(rec)
        self.calc(func)
        target = func(Image.open(self.image))
        res = []
        for name, info in self.info.items():
            if func==sko:
                if cmp_sko(target, info[1]) < dist:
                    res.append([name, info[0]])
            else:
                if target - info[1] < dist:
                    res.append([name, info[0]])
        return res.copy()
