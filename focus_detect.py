import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import matplotlib.pyplot as plt


class_names = ['e', 'hd', 'se', 'straight', 'sw', 'w']

filepath = 'Keras-Model'
loaded_model = load_model(filepath)

def focus(filename):
    img_data = Image.open(filename).resize((100, 100))
    img_arr = np.array(img_data)
    img_arr = img_arr[:, :, :3] / 255
    print(img_arr.shape)

    test_image = img_arr.reshape(1, 100, 100, 3)
    print(test_image.shape)

    predictions = loaded_model.predict(test_image)
    prediction = np.argmax(predictions[0])
    print(f'Prediction: {class_names[int(prediction)]}')

    return str(prediction)