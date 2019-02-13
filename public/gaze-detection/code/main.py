import numpy as np

from pathlib import Path
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv2D, Input,MaxPool2D, Reshape,Activation,Flatten, Permute,MaxPooling2D,Dropout
from keras.models import Model
import tensorflow as tf
from keras.layers.advanced_activations import PReLU

# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
import cv2
import sys
import numpy as np

import gradients

from Xlib import display

X = []
Y = []
data = Path('MASK-1011-1249.txt').read_text().splitlines()
for line in data:
	tmp = line.split(',')
	x = [float(i) for i in tmp[:24]]
	y = [float(i) for i in tmp[24:]]
	z = []
	for i in range(12):
		z.append([x[i * 2], x[i * 2 + 1]])
	X.append(z)
	Y.append(y)

eye_width = 25
eye_height = 20

model = Sequential()
model.add(Dense(256, input_shape=(12,2)))
model.add(Dense(128))
model.add(Dense(64))
model.add(Flatten())
model.add(Dense(256, activation='sigmoid'))
model.add(Dense(2, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['mean_squared_error'])
model.fit(np.array(X), np.array(Y), epochs=200, verbose=1)


# initialize dlib's face detector (HOG-based) and then create the
# facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# initialize the video stream and sleep for a bit, allowing the
# camera sensor to warm up
print("[INFO] camera sensor warming up...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

qx = 0
qy = 0

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream, resize it to
	# have a maximum width of 400 pixels, and convert it to
	# grayscale
	frame = vs.read()
	frame = imutils.resize(frame, width=720)
 
	# detect faces in the grayscale frame
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rects = detector(frame_gray, 0)

	# check to see if a face was detected, and if so, draw the total
	# number of faces on the frame
	if len(rects) > 0:
		text = "{} face(s) found".format(len(rects))
		cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 0, 255), 2)

	# loop over the face detections
	for rect in rects:
		# compute the bounding box of the face and draw it on the
		# frame
		(bX, bY, bW, bH) = face_utils.rect_to_bb(rect)
		cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),
			(0, 255, 0), 1)

		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(frame_gray, rect)
		shape = face_utils.shape_to_np(shape)

		ex = shape[36][0] + 2
		ew = shape[39][0] - ex - 2
		ey = min(shape[37][1], shape[38][1]) - 5
		eh = max(shape[40][1], shape[41][1]) - ey + 5
		eye = frame[ey: ey + eh, ex: ex + ew]
		cv2.imshow("Right Eye", eye)

		px, py = gradients.find_pupil(eye)
		eye = cv2.fastNlMeansDenoisingColored(eye,None,10,10,3,21)
		eye = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)

		keras = [
			# right eye
			shape[36].tolist(),
			shape[37].tolist(),
			shape[38].tolist(),
			shape[39].tolist(),
			shape[40].tolist(),
			shape[41].tolist(),
			# right eye pupil
			[px + ex, py + ey],
			# nose
			shape[31].tolist(),
			shape[33].tolist(),
			shape[35].tolist(),
			shape[29].tolist(),
			# chin
			shape[8].tolist(),
		]

		keras_min_x = min([i[0] for i in keras])
		keras_max_x = max([i[0] for i in keras])
		keras_min_y = min([i[1] for i in keras])
		keras_max_y = max([i[1] for i in keras])
		keras_max_w = keras_max_x - keras_min_x
		keras_max_h = keras_max_y - keras_min_y
		print(keras)
		# normalize
		for i in keras:
			i[0] = (i[0] - keras_min_x) / keras_max_w
			i[1] = (i[1] - keras_min_y) / keras_max_h

		k = model.predict(np.array([keras]))[0]
		m = np.zeros((1080, 1920,1), np.uint8)

		if qx == 0:
			qx = int(k[0] * 1920)
			qy = int(k[1] * 1080)
		else:
			qx = int(qx * 0.7 + k[0] * 1920 * 0.3)
			qy = int(qy * 0.7 + k[1] * 1080 * 0.3)


		cv2.circle(m, (qx, qy), 2, (255), thickness=1, lineType=8, shift=0)
		cv2.namedWindow("Predict", cv2.WND_PROP_FULLSCREEN)
		cv2.setWindowProperty("Predict",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
		cv2.imshow("Predict", m)
		cv2.circle(eye, (px, py), 2, (255), thickness=1, lineType=8, shift=0)
		cv2.imshow("Right Eye Processed", eye)

	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	elif key == ord("p"):
		time.sleep(2.0)

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
