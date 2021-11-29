from imfunc import *

# RGB гистограмма
def hist_arr(img):
    clrs = img.getcolors(img.size[0]*img.size[1])
    r_ch = [0 for i in range(256)]
    g_ch = r_ch.copy()
    b_ch = r_ch.copy()
    for n, c in clrs:
        r_ch[r(c)] += n
        g_ch[g(c)] += n
        b_ch[b(c)] += n
    arr = [round((r_ch[i] + g_ch[i] + b_ch[i])/3, 3) for i in range(256)]
    return arr.copy()

img = Image.open("hk.png")
harr = hist_arr(img)
print(harr)
hist(harr, 256, "TestHist")