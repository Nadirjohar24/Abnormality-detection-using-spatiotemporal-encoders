import cv2
import numpy as np
from keras.models import load_model
import imutils

model = load_model("saved_model.h5")

def mean_squared_loss(x1, x2):
    difference = x1 - x2
    a, b, c, d, e = difference.shape
    n_samples = a * b * c * d * e
    sq_difference = difference**2
    Sum = sq_difference.sum()
    distance = np.sqrt(Sum)
    mean_distance = distance / n_samples

    return mean_distance

def process_video(video_file):
    cap = cv2.VideoCapture(video_file)
    print(cap.isOpened())

    abnormal_events = []

    while cap.isOpened():
        imagedump = []
        ret, frame = cap.read()

        for i in range(10):
            ret, frame = cap.read()
            if not ret:
                break

            image = imutils.resize(frame, width=1000, height=1200)
            frame = cv2.resize(frame, (227, 227), interpolation=cv2.INTER_AREA)
            gray = 0.2989 * frame[:, :, 0] + 0.5870 * frame[:, :, 1] + 0.1140 * frame[:, :, 2]
            gray = (gray - gray.mean()) / gray.std()
            gray = np.clip(gray, 0, 1)
            imagedump.append(gray)

        imagedump = np.array(imagedump)
        imagedump.resize(227, 227, 10)
        imagedump = np.expand_dims(imagedump, axis=0)
        imagedump = np.expand_dims(imagedump, axis=4)

        output = model.predict(imagedump)

        loss = mean_squared_loss(imagedump, output)

         #if frame.any()==None:
     #   print("none")
        if frame is None:
            print("Frame is None")
            break 
        

        if loss > 0.00038:
            print('Abnormal Event Detected')
            # Add the timestamp or frame number to the list of abnormal events
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
            abnormal_events.append(timestamp)

    cap.release()
    return abnormal_events