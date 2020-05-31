from numpy import load
import os
import numpy as np
import cv2

SIZE = (96, 96)
directory = r'dataset/youtube_faces_with_keypoints_full_4'

def gray_scale(images):
    # rgb2gray converts RGB values to grayscale values by forming a weighted sum of the R, G, and B components:
    # 0.2989 * R + 0.5870 * G + 0.1140 * B
    # source: https://www.mathworks.com/help/matlab/ref/rgb2gray.html

    images = [0.2989 * images[:, :, :, 0] + 0.5870 * images[:, :, :, 1] + 0.1140 * images[:, :, :, 2]]
    return images


def load_data():
    X = []
    y = []

    for filename in os.listdir(directory):
        if filename.endswith(".npz"):
            data = load(directory + "/" + filename)
            images = np.array(data['colorImages'])
            images = images.transpose(3, 0, 1, 2)

            bounds = np.array(data['boundingBox'])
            bounds = bounds.transpose(2, 0, 1)

            results = np.array(data['landmarks2D'])
            results = results.transpose(2, 0, 1)

            for image, bound, result in zip(images, bounds, results):
                bound = np.array(bound)
                bound = bound.astype(int)
                # print('\n\nbound', bound)
                top_left, down_left, top_right, down_right = bound

                # crop
                cropped = image[top_left[0]:down_right[0], top_left[1]:down_right[1]]
                try:
                    resized = cv2.resize(cropped, dsize=SIZE, interpolation=cv2.INTER_CUBIC)
                    # print(cropped.shape)
                    # print(resized.shape)
                    X.append(resized)
                    y.append(result)
                except cv2.error:
                    continue

    X = np.array(X)
    print(X.shape)
    X = gray_scale(X)
    print('after gray_scale: ', X.shape)
    y = np.array(y)
    print(y.shape)

    return X, y
# TODO: transpose V
# TODO: crop V
# TODO: resize V
# TODO: gray scale V
# TODO: put everything in one array V

