# -*- coding: utf-8 -*-
import tensorflow as tf
from tensorflow import keras

inception_v3 = keras.applications.InceptionV3(weights='imagenet', include_top=True)

import cv2
import json
import math
import os
import numpy as np
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing import image
from keras.models import Model
from keras.applications.inception_v3 import InceptionV3
import matplotlib.image as mpimg

from tensorflow.keras.applications.inception_v3 import InceptionV3

def load_image(image_path):
  image = cv2.imread(image_path)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  image = cv2.resize(image, (299, 299))
  image = tf.keras.preprocessing.image.img_to_array(image)
  image = tf.keras.applications.inception_v3.preprocess_input(image)
  return np.expand_dims(image, axis=0)
  model.predict(image)

base_model = InceptionV3(include_top=False, weights='imagenet', input_shape=(299, 299, 3))

def detect_objects(img):
    # img = cv2.resize(img, (299, 299,3))
    img = image.image_utils.load_img(img, target_size=(299, 299,3))
    x = image.image_utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    # x = x/255
    x = preprocess_input(x)
    # y = []
    # y.append(x)
    # final = np.array(y)
    # print(x.shape)
    features = model.predict(x)
    # print(features.shape)
    # X.append(features)
    return x

for layer in base_model.layers:
    layer.trainable = False
x = base_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dense(1024, activation='relu')(x)
x = tf.keras.layers.Dropout(0.5)(x)
x = tf.keras.layers.Dense(512, activation='relu')(x)
x = tf.keras.layers.Dropout(0.5)(x)
predictions = tf.keras.layers.Dense(2, activation='softmax')(x)

from google.colab import files

uploaded = files.upload()

#Capture video
def detect_objects_in_video(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        features = detect_objects(frame)
        for i in range(features.shape[1]):
            feature = features[0, i, :]
            img_path = output_dir + '/frame_{}_object_{}.jpg'.format(frame_count, i)
            cv2.imwrite(img_path, frame)
            print('Object detected in frame {}: {}'.format(frame_count, get_object_name(feature)))
        frame_count += 1
    cap.release()

video_file = 'path_to_video_file.mp4'
#Define the output path of the video
output_folder = 'path_to_output_folder/'

cap = cv2.VideoCapture(video_file)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

def process_frame(frame):
    # Resize the frame to 299x299 pixels (the required input size for Inception v3)
    resized_frame = cv2.resize(frame, (299, 299))
    normalized_frame = preprocess_input(resized_frame)
    batched_frame = np.expand_dims(normalized_frame, axis=0)
    predictions = model.predict(batched_frame)
    decoded_predictions = decode_predictions(predictions, top=5)[0]
    for prediction in decoded_predictions:
        print("Object: {}, Probability: {}".format(prediction[1], prediction[2]))

    return
    
for i in range(frame_count):
    # Set the current frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)

    # Read the current frame
    ret, frame = cap.read()

    if ret:
        # Save the current frame as an image file
        frame_file = output_folder + 'frame' + str(i) + '.jpg'
        cv2.imwrite(frame_file, frame)

        # Process the current frame and detect objects
        process_frame(frame)
        cap.release()

query = input("Enter a search query: ")

#Search for objects in the video that match the query
def search(query):
     search_video(query)

#Release the video file and close the window
cap.release()
cv2.destroyAllWindows()

def search(query):
    results = []

!pip install Flask

import tempfile
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

@app.route('/', methods=['GET', 'POST'])
def upload_and_classify():
    if request.method == 'POST':
        # Process input data
        video_file = request.files['video']
        video_data = video_file.read()

        # Preprocess input
        # Convert the video data to a NumPy array
        video_array = np.frombuffer(video_data, dtype=np.uint8)
        # Reshape the video array to (num_frames, height, width, channels)
        video_shape = (num_frames, height, width, channels)
        video_array = np.reshape(video_array, video_shape)
        # Normalize the pixel values
        video_array = video_array / 255.0
        predictions = model.predict(np.array([video_array]))

     # Postprocess output
        class_index = np.argmax(predictions)
        output = {'class': classes[class_index], 'probability': float(predictions[0][class_index])}

        return render_template('result.html', output=output)
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run()
