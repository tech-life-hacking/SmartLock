import face_recognition
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Create arrays of known face encodings and their names
my_face_encodings = []
my_face_names = []
for i in range(5):
    picture_of_me = face_recognition.load_image_file("picture_of_me/"+str(i)+".jpg")
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
    my_face_encodings.append(my_face_encoding)
    my_face_names.append("my_face_"+str(i))

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

# initialize Jetson.GPIO
output_pin = 33

# Pin Setup:
# Board pin-numbering scheme
GPIO.setmode(GPIO.BOARD)
# set pin as an output pin with optional initial state of HIGH
GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
servo = GPIO.PWM(output_pin, 50)
servo.start(0)

class FaceDetection():
    def run(self,process_this_frame):
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=1, model="cnn")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(my_face_encodings, face_encoding, tolerance=0.4)
                name = "Unknown"
                capturedname = "Unknown"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(my_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = my_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for name in face_names:
            if name in my_face_names:
                return True

