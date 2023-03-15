from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from picamera2 import Picamera2 
import cv2 as cv 
import numpy as np
from libcamera import controls
import time


def tensortest():
    # picam2 = Picamera2()
    # picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #sets auto focus mode


    # picam2.start() #must start the camera before taking any images
    # time.sleep(1)

    # picam2.capture_file('/home/tuftsrobot/ME35PROJECT/imagetensor.jpg')

    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)


    # Load the model

    # Load the labels
    class_names = open("/home/tuftsrobot/ME35PROJECT/labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open('/home/tuftsrobot/ME35PROJECT/imagetensor.jpg').convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)

    # picam2.stop()

    return confidence_score