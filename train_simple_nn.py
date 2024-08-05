import matplotlib
matplotlib.use("Agg")

# import the necessary packages
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras import Sequential
from tensorflow.keras.activations import sigmoid
from pathutils import list_images
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import os
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True)
ap.add_argument("-m", "--model", required=True)
ap.add_argument("-l", "--label-bin", required=True)
ap.add_argument("-p", "--plot", required=True)


args = ap.parse_args()

print("[INFO] loading images...")

data = []
labels = []


imagesPaths = sorted(list(list_images(args.dataset)))
random.seed(42)
random.shuffle(imagesPaths)

for imagePath in imagesPaths:
    try:
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (32, 32)).flatten()
        data.append(image)

        label = imagePath.split(os.path.sep)[-2]
        labels.append(label)

        print("Resize success✅")
    except Exception as e:
        print(str(e))


data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)


(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=42)



lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.fit_transform(testY)



model = Sequential()

model.add(Dense(1024, input_shape=(3072,), activation="sigmoid"))
model.add(Dense(512, activation="sigmoid"))
model.add(Dense(len(lb.classes_), activation="softmax"))


INIT_LR = 0.01
EPOCHS = 160


print("[INFO] training network...")
# opt = SGD(learning_rate=INIT_LR)
#  ????
model.compile(loss="categorical_crossentropy", metrics=["accuracy"])


H = model.fit(x=trainX, y=trainY, validation_data=(testX, testY), epochs=EPOCHS, batch_size=32)



print("[INFO] evaluating network...")
predictions = model.predict(x=testX, batch_size=32)

print(classification_report(testY.argmax(axis=1), predictions.argmax(axis=1), target_names=lb.classes_))
# plot the training loss and accuracy
N = np.arange(0, EPOCHS)
plt.style.use("ggplot")
plt.figure()
plt.plot(N, H.history["loss"], label="train_loss")
plt.plot(N, H.history["val_loss"], label="val_loss")
plt.plot(N, H.history["accuracy"], label="train_acc")
plt.plot(N, H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy (Simple NN)")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.savefig(args.plot)



print("[INFO] serializing network and label binarizer...")
model.save(args.model)
f = open(args.label_bin, "wb")
f.write(pickle.dumps(lb))
f.close()
