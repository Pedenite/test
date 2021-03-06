import os
import sys
import math
from classes.ppm import PPM

def get_file(file_name):
    os.system("if [ ! -d .tempICFMS ]; then mkdir .tempICFMS; fi")              # creates .tempICFMS folder if not exists (only on linux) 
    os.system("convert " + file_name + " -compress none .tempICFMS/temp.ppm")   # uses image-magik convert to .ppm P3

def prepare_PPM():
    file = open(".tempICFMS/temp.ppm", "r")
    a = file.readline()
    b = file.readline()
    abc = [int(n) for n in b.split()]
    c = file.readline()

    test = PPM(abc[0], abc[1], int(c))
    test.pixels = []
    d = ""
    while True:
        d = file.readline()
        if d == '':
            break
        bcd = [int(n) for n in d.split()]
        test.pixels.extend(bcd)

    file.close()
    test.show()

    return test

def crop_PPM(ppm):
    i = j = 0
    m_x = m_y = 0
    crop_x = crop_y = 0
    limit = 10
    precision = 250

    while i < ppm.size2:
        j = 0
        while j < ppm.size1*3:
            if ppm.pixels[j + ppm.size1*3*i] > precision:
                crop_x += 1
            else:
                crop_x = 0
            
            if crop_x >= limit*3:
                m_x += j - limit*3
                break
            j += 1

        if j-limit*3 <= 5:
            crop_y += 1
        else:
            crop_y = 0

        if crop_y >= limit:
            m_y = i-limit
            break
        i += 1
    
    m_x = m_x/(i*3)

    
    return m_x, m_y

def resize_PPM(ppm, x, y):
    x = math.ceil(x)
    y = math.ceil(y)
    new_set = []
    for line in range(y):
        for color in range(x*3):
            new_set.append(ppm.pixels[color + ppm.size1*3*line])

    ppm.size1 = x
    ppm.size2 = y
    ppm.pixels = new_set
    print(len(ppm.pixels))

def get_dir(file_name):
    dirs = file_name.split('/')
    dirs.pop()
    direc = ''
    if len(dirs) > 0:
        direc = str(dirs).replace('[', '').replace(']', '').replace(',', '/').replace('\'', '').replace(" ", "") # get directory from file_name

    return direc

def save(file_name, ppm):
    new_file = open(".tempICFMS/result.ppm", "w")
    new_file.write(ppm.id+'\n')
    new_file.write(str(ppm.size1)+' '+str(ppm.size2)+'\n')
    new_file.write(str(ppm.comp)+'\n')
    new_file.write(str(ppm.pixels).replace('[', '').replace(']', '').replace(',', '')+'\n')
    new_file.close()

    temp = file_name.split(".")
    if len(temp) == 1:
        file_name = temp[0] + ".ppm"
        print(file_name)

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    if temp[len(temp)-1] == "jpg" or temp[len(temp)-1] == "png" or temp[len(temp)-1] == "jpeg":
        os.system("convert .tempICFMS/result.ppm " + file_name)
    else:
        os.system("mv .tempICFMS/result.ppm " + file_name)

def image_processing():
    fileList = sys.argv
    fileList.pop(0)
    template = False
    dim_x = dim_y = 0

    if fileList[0] == "-t":
        template = True
        fileList.pop(0)

    if len(fileList) == 0:
        print("fatal error: no input files\nPlease insert all input files separated by a blank space after program name\nFor a workaround of the recent problems, it's possible to use the -t flag to resize all images to the dimensions of the first")
        return

    for i,file_name in enumerate(fileList):
        print(file_name)
        get_file(file_name)
        ppm = prepare_PPM()
        if not(template and i > 0):
            dim_x, dim_y = crop_PPM(ppm)

        resize_PPM(ppm, dim_x, dim_y)

        direc = get_dir(file_name)
        save(direc + "/result/out" + str(i) + "." + str(file_name.split('.').pop()), ppm)  

if(__name__ == "__main__"):
    image_processing()
