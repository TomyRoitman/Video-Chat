from keras.models import Sequential
from keras.models import load_model
from keras.layers import Convolution2D, MaxPooling2D, Dropout
from keras.layers import Flatten, Dense
from keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam

def get_my_CNN_model_architecture():
    '''
    The network should accept a 96x96 grayscale image as input, and it should output a vector with 30 entries,
    corresponding to the predicted (horizontal and vertical) locations of 15 facial keypoints.
    '''
    model = Sequential()
    model.add(Convolution2D(68, (5, 5), input_shape=(96, 96, 1), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Convolution2D(68, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.1))

    model.add(Convolution2D(136, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Convolution2D(34, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))

    model.add(Flatten())

    model.add(Dense(68, activation='relu'))
    model.add(Dense(136, activation='relu'))
    model.add(Dense(272, activation='relu'))
    # model.add(Dense(68, activation='relu'))
    model.add(Dense(136))

    return model;

def compile_my_CNN_model(model, optimizer, loss, metrics):
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

def train_my_CNN_model(model, X_train, y_train):
    return model.fit(X_train, y_train, epochs=30, batch_size=200, verbose=1, validation_split=0.2)

def save_my_CNN_model(model, fileName):
    model.save(fileName + '.h5')

def load_my_CNN_model(fileName):
    return load_model(fileName + '.h5')
