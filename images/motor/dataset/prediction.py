import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf
IMG_HEIGHT = 150
IMG_WIDTH = 150
def predict_image(img_path):
    # Load the model for inference
    model = tf.keras.models.load_model('images/motor/dataset/motor_classifier.h5')
    img = image.load_img(img_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array)
    if prediction[0] > 0.5:
        return "motor"
    else:
        return "not motor"

# Example usage
print(predict_image('sscjgzzneo.jpeg'))
