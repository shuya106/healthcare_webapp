import numpy as np
import cv2

def process_img(img_list):

    image_array = np.empty((0, 224,224,3))
    for img_path in img_list:
        img = cv2.imread(img_path)
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.reshape(1, 224, 224, 3)

        image_array = np.concatenate([image_array, img], axis=0)

    image_array /= 255
    return image_array

def get_labels(num_0, num_1, num_2):
    t = np.concatenate([np.zeros(num_0), np.ones(num_1), np.ones(num_2) * 2]).astype(int)
    t = np.identity(3)[t].astype(int)
    return t
