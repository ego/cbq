# -*- coding: utf-8 -*-
"""prototype.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G3J-xn2r7XlrEIV4tgtyOjqC3GmikkUe

________
# I: Librairies

### pip install
"""

!pip install visualkeras

!pip install tensorflow

"""### Import Librairies """

# to deal with maths
import pandas as pd
import numpy as np
import random

# to deal with graphs
from keras.utils import load_img
import matplotlib.pyplot as plt
from collections import defaultdict # we use it to create color map
import visualkeras

# to deal with folders
import os
import glob as gb
import shutil # automating process of copying and removal of files and directories
from sklearn.utils import shuffle

# DL
import tensorflow as tf
import cv2
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras import Input
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, BatchNormalization, Activation

# Check versions
!python --version
print('TensorFlow ', tf.__version__)
print('Keras ', tf.keras.__version__)

"""### Random Seed"""

# fix random seed for reproducibility
np.random.seed(5)

# random_state
RANDOM_STATE = 44

# # to avoid GPU errors
# physical_devices = tf.config.list_physical_devices("GPU")
# tf.config.experimental.set_memory_growth(physical_devices[0], True)

"""________
# II: Data Preparation

### 1: Download the dataset from kaggle
"""

# One time for runtime
# Download and use kaggle data within Google Colab:
# 1. Click on kaggel profile icon
# 2. Click Account
# 3. Scroll to the API section
# 4. Click Expire API Token
# 5. Then click Create New API Token
# 6. You will then have new API credentials in the file kaggle.json
# 7. install kaggle in colab
! pip install -q kaggle

# 8: Choose the "kaggle.json" file that you downloaded
from google.colab import files
files.upload()
# 9: Make directory named kaggle
! mkdir ~/.kaggle

# 10: copy kaggle.json file there
! cp kaggle.json ~/.kaggle/

# 11: Change the permissions of the file
! chmod 600 ~/.kaggle/kaggle.json

# 12: Now you can check if everything's okay by running this command
! kaggle datasets list

# 13: to download a dataset that are NOT part of a competition (regular dataset)
! kaggle datasets download -d grassknoted/asl-alphabet -p /content/sample_data/dataset/ --unzip

"""### 2: Checking Dimention and Images size (check the data before choosing img_size)

##### 1: Training dataset
"""

# We can check the training data by looking at one image of each of the alphabets to make sure that none of them are missing from our data.
train_alphabet_filenames = os.listdir("/content/sample_data/dataset/asl_alphabet_train/asl_alphabet_train/A/")
sample = random.choice(train_alphabet_filenames)
image = load_img("/content/sample_data/dataset/asl_alphabet_train/asl_alphabet_train/A/"+sample)
plt.imshow(image)

# delete useless variables
del train_alphabet_filenames, sample, image

# We can check the training data by looking at one image of each of the alphabets to make sure that none of them are missing from our data.
train_path = '/content/sample_data/dataset/asl_alphabet_train/asl_alphabet_train/'

folders = os.listdir(train_path) 
for folder in folders:
  plt.figure(figsize=(20, 20))
  plt.subplot(6, 5, 30)
  files = os.listdir(train_path + folder)
  sample = random.choice(files)
  image = load_img(train_path + folder + '/' + sample)
  plt.imshow(image, cmap=plt.cm.binary)
  plt.title(folder)

# delete useless variables
del folders, folder, files, sample, image

# 1: Images sizes and shape of training dataset
total_samples = 0
train_samples_classes = {}
size = []

print('For training dataset:\n')
for folder in os.listdir(train_path): 
    files = gb.glob(pathname= str(train_path + folder + '/*.jpg'))

    # get number of samples for each class and dataset
    print(f'Class {folder} : {len(files)} samples')
    total_samples += len(files)
    train_samples_classes[folder] = len(files)

    # get the size of dataset
    for file in files: 
        image = plt.imread(file)
        size.append(image.shape)

# 2: print the results
print("\nTotal number of train samples is: ", total_samples)

# 3: Data to plot
plt.pie([float(train_samples_classes[v]) for v in train_samples_classes], labels=[str(k) for k in train_samples_classes], autopct='%1.1f%%')
plt.show()

# 4: all of them are with size of (200,200,3)
print("\nThe number of traning samples that has the same size are as: ")
pd.Series(size).value_counts()

"""##### 2: Testing dataset"""

# check all testing dataset
test_path = '/content/sample_data/dataset/asl_alphabet_test/asl_alphabet_test/'

files = os.listdir(test_path) 
for file in files:
  plt.figure(figsize=(20, 20))
  plt.subplot(6, 5, 30)
  image = load_img(test_path + file)
  plt.imshow(image, cmap=plt.cm.binary)
  plt.title(file)

# delete useless variables
del files, file, image

# 1: Images sizes and shape of test dataset
size = []
files = gb.glob(pathname= str(test_path + '*.jpg'))

# get the size of dataset
for file in files: 
    image = plt.imread(file)
    size.append(image.shape)

# 2: get number of samples for the dataset
print(f'For test data, found {len(files)} samples')

# 3: all of them are with a size of (200,200,3)
print("\nThe testing dataset sizes are as: ")
pd.Series(size).value_counts()

# delete all useless variables
del total_samples, train_samples_classes, size, folder, files, file, image

"""**OK**, since all of jpgs are with size (200,200,3) we can feel comfort in using all images in our model, after resizing it in a specific amount.

### **3: Define Input Size Constants (you can edit it)**
"""

# Input Image
IMAGE_WIDTH=100
IMAGE_HEIGHT=100
IMAGE_CHANNELS=3
IMAGE_SIZE=(IMAGE_WIDTH, IMAGE_HEIGHT)
INPUT_SHAPE=(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)

"""### 4:
### -Getting X and y from Train and Test Datasets
### -Check Random Images
### -Remove Useless Folders

##### 1: Training dataset
"""

# create a dictionary with their names & indices for 29 classes
folders = os.listdir(train_path) 
classes = {}

for index, folder in enumerate(folders, start=0):
    classes[folder] = index
print (classes)

# create a function to get the the dictionary back
def get_classes(n) : 
    for x , y in classes.items() : 
        if n == y :
            return x

# get X_train and y_train that used to fit the parameters (e.g., weights) 
X_train = []
y_train = []

# read all images of 29 categories in training folder
for folder in os.listdir(train_path): 
    files = gb.glob(pathname= str(train_path + folder + '/*.jpg'))

    for file in files: 
        # use OpenCV to resize them and convert them into arrays
        image = cv2.imread(file)
        image_array = cv2.resize(image , IMAGE_SIZE)

        X_train.append(list(image_array))
        y_train.append(classes[folder])

# how many items in X_train 
print(f'we have {len(X_train)} items in X_train')

# check random pictures in X_train, and adjust their titles using the get_classes function
plt.figure(figsize=(20,20))

# n = [0, .., 28 images], i = [random_indice_1, .., random_indice_29]
for n , i in enumerate(list(np.random.randint(0, len(X_train), 29))): 
    plt.subplot(6, 6, n+1)
    plt.imshow(X_train[i])   
    plt.axis('off')
    plt.title(get_classes(y_train[i]))

# deletes the training directory and all its contents
shutil.rmtree('/content/sample_data/dataset/asl_alphabet_train')

"""##### 2: Testing dataset"""

# create a function to get the id back
def get_id(n) : 
    for x , y in classes.items() : 
        if n == x :
            return y

# get X_test and y_test that used to tune the hyperparameters (i.e. the architecture, ..) 
X_test = []
y_test = []

# read all images of 29 categories in testing folder
files = gb.glob(pathname= str(test_path + '/*.jpg'))

for file in files: 
  # use OpenCV to resize them and convert them into arrays
  image = cv2.imread(file)
  image_array = cv2.resize(image , IMAGE_SIZE)
  file = file.replace('/content/sample_data/dataset/asl_alphabet_test/asl_alphabet_test/', '')
  file = file.replace('_test.jpg', '')

  X_test.append(list(image_array))
  y_test.append(get_id(file))

# how many items in X_test 
print(f'we have {len(X_test)} items in X_test')

# check random pictures in X_test, and adjust their titles using the get_classes function
plt.figure(figsize=(20,20))

# n = [0, .., 28 images], i = [random_indice_0, .., random_indice_28
for n , i in enumerate(list(np.random.randint(0, len(X_test), 29))) : 
    plt.subplot(6, 6, n+1)
    plt.imshow(X_test[i])    
    plt.axis('off')
    plt.title(get_classes(y_test[i]))

# deletes the testing directory and all its contents
shutil.rmtree('/content/sample_data/dataset/asl_alphabet_test')

# delete useless variables
del test_path, train_path, folders, folder, index, files, file, image, image_array, n , i

# removes an empty directory.
os.rmdir('/content/sample_data/dataset/')

"""### 5: Shuffle Data"""

X_train, y_train = shuffle(X_train, y_train, random_state = RANDOM_STATE)
X_test, y_test = shuffle(X_test, y_test, random_state = RANDOM_STATE)

"""### 6: Train and Test Datasets"""

# shape of datasets
print("X train shape: ", len(X_train), " samples")
print("y train shape: ", len(np.unique(y_train)), " classes")
print("-------------------------------")
print("X test shape: ",  len(X_test), " samples")
print("y test shape: ", len(np.unique(y_test)), " classes")

"""________
# III: Data Preprocessing

### 1: One-Hot Encoding  for Train and Test Datasets
"""

# Encode labels to one hot vectors (ex : 2 -> [0,1,0,0,0,0,0,..,0,0])
y_train = to_categorical(y_train, num_classes = 29)
y_test = to_categorical(y_test, num_classes = 29)

"""### 2: Make the 2D Image Arrays Into 1D (flatten them) for CNN

you can use one of these methods:

1: np.array(X)

2: X.reshape(m,n)

3: keras.layers.Flatten(X)
"""

# Convert the Data from list to Arrays for cnn
X_train = np.array(X_train)
X_test = np.array(X_test)

y_train = np.array(y_train)
y_test = np.array(y_test)

print(f'X_train shape  is {X_train.shape}')
print(f'y_train shape  is {y_train.shape}')
print('--------------------------------')
print(f'X_test shape  is {X_test.shape}')
print(f'y_test shape  is {y_test.shape}')

"""### 3: Normalization"""

# The same Normalisation applyied on Training and testing Datasets
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

y_train = y_train.astype("float32")
y_test = y_test.astype("float32")

X_train /= 255
X_test /= 255

"""### 4: Save Datasets

There are 4 ways to save our dataset for later use:

**1.**   For **Small** or **Medium** Sized Datasets

      1. CSV file
      -> save
           for split, dataset in raw_datasets.items():
              dataset.to_csv(f"my-dataset-{split}.csv", index=None)
      -> load
           data_files = {
              "train": "my-dataset-train.csv",
              "validation": "my-dataset-validation.csv",
              "test": "my-dataset-test.csv",
           }
           re_data = load_dataset("csv", data_files= data_files)

           
      2. JSON file
      -> save
           for split, dataset in raw_datasets.items():
              dataset.to_json(f"my-dataset-{split}.jsonl")
      -> load
           data_files = {
              "train": "my-dataset-train.json",
              "validation": "my-dataset-validation.json",
              "test": "my-dataset-test.json",
           }
           re_data = load_dataset("json", data_files= data_files)

**2.**   For **Huge** Sized Datasets

      1. ARROW file
      Great for reload or process the data in the near future
      from datasets import load_dataset, load_from_disk
      raw_datasets.save_to_disk("path")
      re_data = load_from_disk("path")

      2. PARQUET file
      Designed for long term storage and very space efficency 
      -> save
      for split, dataset in raw_datasets.items():
        dataset.to_parquet(f"my-dataset-{split}.parquet")
      -> load
      data_files = {
        "train": "my-dataset-train.parquet",
        "validation": "my-dataset-validation.parquet",
        "test": "my-dataset-test.parquet",
      }
      re_data = load_dataset("parquet", data_files= data_files)

________
# IIII: CNN

### 1: Build the Model
"""

# build a CNN model
prototype = Sequential([
                        Input(INPUT_SHAPE),
                         
                        Conv2D(256,kernel_size=(1,1),strides=(1, 1), padding='valid'), # apply bottleneck method to reduce the num of para
                        BatchNormalization(),
                        Activation('relu'), 
                         
                        Conv2D(512,kernel_size=(3,3)),
                        BatchNormalization(),
                        Activation('relu'), 
                         
                        MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='valid'),   # if stride none, then take the same pool size
                                                  
                        Conv2D(128,kernel_size=(1,1)),
                        BatchNormalization(),
                        Activation('relu'), 
                         
                        Conv2D(256,kernel_size=(3,3)),
                        BatchNormalization(),
                        Activation('relu'), 
                         
                        MaxPool2D(2,2),
                         
                        Conv2D(64,kernel_size=(1,1)),
                        BatchNormalization(),
                        Activation('relu'), 
                         
                        Conv2D(128,kernel_size=(3,3)),
                        BatchNormalization(),
                        Activation('relu'), 
                         
                        MaxPool2D(2,2),
                         
                        Conv2D(32,kernel_size=(1,1)),
                        BatchNormalization(),
                        Activation('relu'), 
                         
                        Conv2D(64,kernel_size=(3,3)),
                        BatchNormalization(),
                        Activation('relu'), 
                         
                        MaxPool2D(2,2),
                         
                        Conv2D(32,kernel_size=(3,3)),
                        BatchNormalization(),
                        Activation('relu'), 

                        Flatten(),    
                            
                        Dense(64), 
                        BatchNormalization(),
                        Activation('relu'), 
                         
                        Dense(29), 
                        BatchNormalization(),  
                        Activation('softmax'), 
                        ])

print('Model Details are : ')
print(prototype.summary())

"""### 2: Visualise the Model"""

# create color map
color_map = defaultdict(dict)

color_map[Conv2D]['fill'] = 'yellow'
color_map[BatchNormalization]['fill'] = 'red'
color_map[Activation]['fill'] = 'red'
color_map[MaxPool2D]['fill'] = 'pink'
color_map[Flatten]['fill'] = 'blue'
color_map[Dense]['fill'] = 'green'

visualkeras.layered_view(prototype, 
                         to_file='Model_Architecture.png', 
                         color_map=None, # color map or none
                         type_ignore=[], # ignoring layers by their type
                         index_ignore=[], # ignoring layers by their index
                         background_fill='white', # background color
                         draw_volume=True, # Flat Style or not
                         padding=100, # padding between left to center of image
                         spacing=0, # global distance between two layers
                         legend=True, # legend or not
                         #font=text_font, # font type
                         font_color='black' # font color
                         )

"""### 3: Tuning hyperparameters"""



"""### 4: Train the model"""



"""### 5: save the model"""

import gradio as gr


title = """
# Project title
"""
description = """
## Project description
"""
article = """
### Some article here.
Hi!
"""


# def snap(image=None, video=None):
#     return "Hi, it is outputs!"


# demo = gr.Interface(
#     fn=snap,
#     inputs=[
#         gr.Image(info="Image"),
#         # gr.Image(source="webcam", tool=None),
#         # gr.Video(source="webcam"),
#      ],
#     outputs="text",
#     title=title,
#     description=description,
#     article=article,
#     # theme=gr.themes.Monochrome(),
# )

# demo.launch(debug=True, share=True)



#############################################

import gradio as gr


def image_process(image):
    print(image)
    return f"image outputs {len(image)}"


def webcam_process(video):
    print(video)
    return f"video outputs {len(video)}"


demo = gr.Blocks()
with demo:
    # Descriptive content
    with gr.Row():
        gr.Markdown(title)
    with gr.Row():
        gr.Markdown(description)
    with gr.Row():
        gr.Markdown(article)

    # Tabs: image | webcam.
    with gr.Tabs():

        # Process image.
        with gr.TabItem("Process Image"):
            with gr.Row():
                image_input = gr.Image()
                image_output = gr.Textbox()
            image_button = gr.Button("Submit")

        # Process webcam.
        with gr.TabItem("Flip Video"):
            with gr.Row():
                webcam_input = gr.Image(source="webcam", streaming=True)
                webcam_output = gr.Textbox()
            webcam_button = gr.Button("Submit")

    image_button.click(fn=image_process, inputs=image_input, outputs=image_output)
    # webcam_button.click(fn=webcam_process, inputs=webcam_input, outputs=webcam_output)
    webcam_input.change(fn=webcam_process, inputs=webcam_input, outputs=webcam_output, show_progress=True, status_tracker=None)


# Demo entry point.
demo.launch(debug=True, share=True)





#################################################################

import gradio as gr


title = """
# Project title
"""
description = """
## Project description
"""
article = """
### Some article here.
Hi!
"""


# def snap(image=None, video=None):
#     return "Hi, it is outputs!"


# demo = gr.Interface(
#     fn=snap,
#     inputs=[
#         gr.Image(info="Image"),
#         # gr.Image(source="webcam", tool=None),
#         # gr.Video(source="webcam"),
#      ],
#     outputs="text",
#     title=title,
#     description=description,
#     article=article,
#     # theme=gr.themes.Monochrome(),
# )

# demo.launch(debug=True, share=True)



#############################################

import gradio as gr


def image_process(image):
    print(image)
    return f"image outputs {id(image)}"


def webcam_process(video):
    print(video)
    return f"video outputs {id(video)}"


image_page = gr.Blocks()
with image_page:
    # Process image.
    with gr.Row():
        image_input = gr.Image()
        image_output = gr.Textbox()
    image_button = gr.Button("Submit")
    image_button.click(fn=image_process, inputs=image_input, outputs=image_output)


# webcam_page = gr.Blocks()
# with webcam_page:
#     # Descriptive content
#     with gr.Row():
#         gr.Markdown(title)
#     with gr.Row():
#         gr.Markdown(description)
#     with gr.Row():
#         with gr.Accordion("More ..."):
#             gr.Markdown(article)

#     # Process webcam.
#     with gr.Row():
#         webcam_input = gr.Image(source="webcam", streaming=True)
#         webcam_output = gr.Textbox()
#     webcam_button = gr.Button("Submit")
#     webcam_input.change(fn=webcam_process, inputs=webcam_input, outputs=webcam_output, show_progress=True, status_tracker=None)
#     # webcam_button.click(fn=webcam_process, inputs=webcam_input, outputs=webcam_output)


# Demo entry point.
demo = gr.Blocks()
with demo:
    # Descriptive content
    with gr.Row():
        gr.Markdown(title)
    with gr.Row():
        gr.Markdown(description)
    with gr.Row():
        with gr.Accordion("More ..."):
            gr.Markdown(article)

    gr.TabbedInterface([image_page,], [
        "Process image page", 
        # "Process webcam video page"
    ])
demo.launch(debug=True, share=True)
