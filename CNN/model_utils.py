from numpy import load
import os
import numpy as np
import cv2

SIZE = (96, 96)
directories = [r'dataset/youtube_faces_with_keypoints_full_1']
directories.append(r'dataset/youtube_faces_with_keypoints_full_2')
directories.append(r'dataset/youtube_faces_with_keypoints_full_3')
directories.append(r'dataset/youtube_faces_with_keypoints_full_4')

def gray_scale(images):
    # rgb2gray converts RGB values to grayscale values by forming a weighted sum of the R, G, and B components:
    # 0.2989 * R + 0.5870 * G + 0.1140 * B
    # source: https://www.mathworks.com/help/matlab/ref/rgb2gray.html

    images = 0.2989 * images[:, :, :, 0] + 0.5870 * images[:, :, :, 1] + 0.1140 * images[:, :, :, 2]
    return images
from progress.bar import IncrementalBar



def load_data():
    X = []
    y = []
    for i in range(len(directories)):
        to_load = os.listdir(directories[i])
        to_load = to_load[:len(to_load)]
        bar = IncrementalBar('Loading training data', max=len(to_load))
        for filename in to_load:
            if filename.endswith(".npz"):
                data = load(directories[i] + "/" + filename)
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

                        width = bound[3][0] - bound[0][0]
                        height = bound[3][1] - bound[0][1]
                        result[:, 0] -= bound[0][0]
                        result[:, 1] -= bound[0][1]
                        result[:, 0] *= SIZE[0] / width
                        result[:, 1] *= SIZE[1] / height
                        result = (result - 48) / 48
                        y.append(result)
                    except cv2.error:
                        continue

            bar.next()
        bar.finish()
    X = np.array(X[:len(X)])
    print(X.shape)
    # X = gray_scale(X)
    # X = X.reshape(X.shape[0], X.shape[1], X.shape[2], 1)
    print('X after reshaping: ', X.shape)
    y = np.array(y[:len(y)])
    print(y.shape)
    # print(y.shape[0], y.shape[1]*y.shape[2])
    y = y.reshape(y.shape[0], y.shape[1] * y.shape[2])
    print('y after reshaping: ', y.shape)

    return X, y
# TODO: transpose V
# TODO: crop V
# TODO: resize V
# TODO: gray scale V
# TODO: put everything in one array V

