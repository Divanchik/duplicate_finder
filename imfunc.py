from PIL import Image, ImageTk
from imagehash import average_hash, phash
import numpy as np
import os
from tqdm import tqdm


def r(c: list) -> int:
    '''
    Значение R.
    '''
    return c[0]


def g(c: list) -> int:
    '''
    Значение G.
    '''
    return c[1]


def b(c: list) -> int:
    '''
    Значение B.
    '''
    return c[2]


def supported(format: list, path: str):
    '''
    Проверка, принадлежит ли формат изображения `path` списку `list`.
    '''
    for i in format:
        if path.endswith(i):
            return True
    return False


def greyscale_PAL(c: list) -> int:
    '''
    RGB в оттенок серого.
    '''
    return int(0.299*c[0] + 0.587*c[1] + 0.114*c[2])


def scan(path: str, format: list):
    '''
    Сканирование папки(не рекурсивно).
    Возвращает словарь вида { name: path, ... }.
    '''
    res = {}
    for name in tqdm(os.listdir(path), desc="Сканируем", ncols=100):
        if supported(format, name):
            p = os.path.join(path, name)
            res[name] = []
            res[name].append(p)
    return res.copy()


def scan_rec(path: str, format: list):
    '''
    Сканирование папки(рекурсивно).
    Возвращает словарь вида { name: path, ... }.
    '''
    res = {}
    for folder in tqdm(list(os.walk(path)), desc="Сканируем", ncols=100):
        for name in folder[2]:
            if supported(format, name):
                p = os.path.join(folder[0], name)
                res[name] = []
                res[name].append(p)
    return res.copy()


def hist(image):
    try:
        clrs = image.getcolors(image.size[0]*image.size[1])
        r_c = [0 for i in range(256)]
        g_c = r_c.copy()
        b_c = r_c.copy()
        for n, c in clrs:
            r_c[r(c)] += n
            g_c[g(c)] += n
            b_c[b(c)] += n
        arr = [round((r_c[i] + g_c[i] + b_c[i])/3, 3) for i in range(256)]
        return arr.copy()
    except TypeError:
        return -1
    except IndexError:
        return -2


def cmp_hist(base, other):
    tmp = np.abs(np.subtract(base, other))
    return np.std(tmp)


def sko(image, size=64, prec=3) -> float:
    '''
    Принимает изображение `image` и вычисляет среднее квадратичное отклонение.
    '''
    try:
        img = image.resize((size, size))
        values = [greyscale_PAL(i) for i in img.getdata()]
        n = len(values)
        res = np.sqrt(n/(n-1)*np.std(values)**2)
    except TypeError:
        res = -1
    except IndexError:
        res = -2
    return round(res, prec)


def cmp_sko(target: float, other: float) -> float:
    '''
    Сравнение двух СКО.
    Возвращает, на сколько процентов `other` отличается от `target`.
    '''
    return np.abs(1 - other/target)*100


class scanner:
    def __init__(self, target_path: str, folder_path: str, formats: list):
        self.folder = folder_path
        self.target = target_path
        self.format = formats.copy()
        self.info = {}
    
    def scan(self, rec: bool):
        '''
        Сканирование папки и сохранение списка найденных изображений.
        '''
        if rec:
            self.info = scan_rec(self.folder, self.format)
        else:
            self.info = scan(self.folder, self.format)
    
    def calc(self, func):
        '''
        Вычисление хэшей изображений и их сохранение.
        '''
        e = []
        for name, info in tqdm(self.info.items(), desc="Вычисление цифровых отпечатков", ncols=100):
            img = Image.open(info[0])
            tmp_val = func(img)
            if tmp_val == -1:
                e.append(info[0] + " >> неверные данные!")
            elif tmp_val == -2:
                e.append(info[0] + " >> проблемы с индексацией!")
            else:
                self.info[name].append(func(img))
        for i in e:
            print(i)
        for n in self.info.keys():
            print(n, self.info[n])
    
    def find(self, func, dist=5, rec=False):
        '''
        Сканирование, вычисление хэшей и отбор изображений по тому, как сильно они отличаются от образца.
        Возвращает список типа [ [ `name`, `path` ], ... ].
        '''
        self.scan(rec)
        self.calc(func)
        target = func(Image.open(self.target))
        res = []
        for name, info in self.info.items():
            if len(info) == 2:
                if func==sko:
                    if cmp_sko(target, info[1]) < dist:
                        res.append({'name': name, 'path': info[0], 'rate': str(round(cmp_sko(target, info[1]), 3))})
                elif func==hist:
                    if cmp_hist(target, info[1]) < dist*500:
                        res.append({'name': name, 'path': info[0], 'rate': str(round(cmp_hist(target, info[1]), 3))})
                else:
                    if target - info[1] < dist:
                        res.append({'name': name, 'path': info[0], 'rate': str(target-info[1])})
        return res.copy()
