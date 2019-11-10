import numpy as np
import os
from keras.utils import to_categorical
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras import layers
from keras import models


directory = '/Users/retwet/Downloads/leapGestRecog/'

lookup = dict()
reverselookup = dict()
count = 0
for j in os.listdir(directory + '00/'):
    if not j.startswith('.'):
        lookup[j] = count
        reverselookup[count] = j
        count = count + 1

print(lookup)


x_data = []
y_data = []
datacount = 0
for i in range(0, 10):
    for j in os.listdir(directory + '/0' + str(i) + '/'):
        if not j.startswith('.'):
            count = 0
            for k in os.listdir(directory + '/0' + str(i) + '/' + j + '/'):
                img = Image.open(directory + '/0' + str(i) + '/' + j + '/' + k).convert('L')
                img = img.resize((320, 120))
                arr = np.array(img)
                x_data.append(arr)
                count = count + 1
            y_values = np.full((count, 1), lookup[j])
            y_data.append(y_values)
            datacount = datacount + count
x_data = np.array(x_data, dtype='float32')
y_data = np.array(y_data)
y_data = y_data.reshape(datacount, 1)


# for i in range(0, 10):
#    plt.imshow(x_data[i*200 , :, :])
#    plt.title(reverselookup[y_data[i*200 ,0]])
#    plt.show()


y_data = to_categorical(y_data)
x_data = x_data.reshape((datacount, 120, 320, 1))
x_data /= 255

x_train,x_further,y_train,y_further = train_test_split(x_data,y_data,test_size = 0.2)
x_validate,x_test,y_validate,y_test = train_test_split(x_further,y_further,test_size = 0.5)


model=models.Sequential()
model.add(layers.Conv2D(32, (5, 5), strides=(2, 2), activation='relu', input_shape=(120, 320,1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))


model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.fit(x_train, y_train, epochs=10, batch_size=64, verbose=1, validation_data=(x_validate, y_validate))


model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)


model.save_weights("model.h5")
print("Saved model to disk")


[loss, acc] = model.evaluate(x_test,y_test,verbose=1)
print("Accuracy:" + str(acc))
