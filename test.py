from imfunc import scanner, sko, average_hash, phash

path = "C:\\Users\\Lenovo\\Desktop"
target = "C:\\Users\\Lenovo\\Desktop\\OS_L2_1.png"

a = scanner(target, path, ['.png'])
b = a.find(sko)
for i in b:
    print(i)