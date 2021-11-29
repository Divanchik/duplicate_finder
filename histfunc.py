from PIL import Image, ImageDraw
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

def hist(arr: list, height: int, name: str) -> None:
    '''
    Отрисовка гистограммы и сохранение в файл с именем `name.png`.
    '''
    width = len(arr)
    img = Image.new('RGB', (width, height), 'white')
    drw = ImageDraw.Draw(img)
    maxv = float(max(arr))
    for i in range(width):
        if arr[i] > 0:
            drw.line(((i, height), (i, height-arr[i]/maxv*height)), 'black')
    del drw
    img.save(name+'.png', 'PNG')