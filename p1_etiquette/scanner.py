# from pdf2image import convert_from_path
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import threading

# def pdf_to_jpgs():
#     pages = convert_from_path('./Etiquette_Book.pdf')
#
#     # Save each page as a JPEG file using Pillow
#     for i, page in enumerate(pages):
#         page.save(f'./pages/page_{i}.jpg', 'JPEG')

def calculate_fold_line(i,padding):
    is_left =  i % 2
    image =  Image.open(f'./pages/page_{i}.jpg')

    img_arr = np.array(image, dtype=np.uint8)
    img_arr = img_arr
    
    p_range = []
    avg_page_color = 0
    slice_w = 1
    padding_x = padding
    color_range = 16

    x_len = len(img_arr[0])
    x_start = padding_x if is_left else x_len-slice_w-padding_x
    x_end = padding_x+ slice_w if is_left else x_len-padding_x

    for img_i in range(len(img_arr)):
        for img_j in range(x_start, x_end):
            avg = 0
            for px in img_arr[img_i][img_j]:
                avg += px/3

            avg_page_color = (avg_page_color + avg)/2

    for img_i in range(len(img_arr)):
        for img_j in range(x_start, x_end):
            avg = 0
            for px in img_arr[img_i][img_j]:
                avg += px/3

            if (avg <= avg_page_color - color_range):
                if (len(p_range) > 0 and img_i -1 == p_range[-1]):
                    p_range[-1] = img_i
                else:
                    p_range.append(img_i)

            if(len(p_range) == 2): break

    if(len(p_range) == 2):
        img_arr[p_range[0]] = 255
        img_arr[p_range[1]] = 255

    img = Image.fromarray(img_arr)
    img.save(f'./transformed/transformed_page_{i}.jpg')
    return p_range

def plot_folds(i, page_start,page_end, y_space, x1_space, x2_space):
    for j in range(page_start,page_end):

        p_range = calculate_fold_line(j, 1)
        if(len(p_range) != 2): continue

        y_space.append(j)

        x1_space.append(p_range[0])
        x2_space.append(p_range[1])
        print(f'page {j} transformed')

    
# pdf_to_jpgs()
thread_count = 6
page_fraction   = int(len(os.listdir("./pages/"))/thread_count)
y_space=[]
x1_space =[]
x2_space=[]
threads = []

for i in range(thread_count):
    threads.append(threading.Thread(target=plot_folds, args=(i,page_fraction*i,page_fraction*(i+1),y_space,x1_space,x2_space)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()


plt.figure(dpi=1200)
plt.hlines(y=y_space,xmin=x1_space,xmax=x2_space, color='r')
plt.savefig(f'plot.png')
plt.clf()
