data_path = "./imgs/"

import os
import cv2
import numpy as np

def preprocessing():
    mean_color = []

    for filename in os.listdir(data_path):
        img = cv2.imread(data_path + filename)
        N = int(512/128)
        img = cv2.resize(img, (N, N), interpolation=cv2.INTER_AREA)
        mean_color.append([img[:,:,0].mean(), img[:,:,1].mean(), img[:,:,2].mean()])

    return mean_color

def min(array):
    min = 100000
    min_index = 0

    k = 0
    for element in array:
        if abs(np.sum(element)) < min:
            min = abs(np.sum(element))
            min_index = k
        k = k + 1
    return min, min_index

def mosaic_photo(image_path):

    mean_color = preprocessing()  # bgr

    target = cv2.imread(image_path)
    r, c, ch = target.shape

    filenames = [filename for filename in os.listdir(data_path)]

    N = int(512/128)
    for i in range(round(r/N)):
        for j in range(round(c/N)):
            block = target[i * N : i*N + N, j * N : j*N + N, :]
            bgr_mean = [block[:,:,0].mean(), block[:,:,1].mean(), block[:,:,2].mean()] # colore medio bgr in una porzione di N x N
            
            diff = np.subtract(mean_color, bgr_mean)
            best, best_index = min(diff)

            img = cv2.imread(data_path + filenames[best_index])
            img = cv2.resize(img, (N, N), interpolation=cv2.INTER_AREA)
            target[i * N : i*N + N, j * N : j*N + N, :] = img[:,:,:]

    return target


res = mosaic_photo("./imgs/0060.jpg")
cv2.imwrite('./res.jpg', res)

