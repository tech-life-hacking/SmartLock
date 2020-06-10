import timeit

TEST_IMAGES = [
    "0.jpg",
    "1.jpg",
    "2.jpg",
    "3.jpg",
    "4.jpg"
]


def run_test(setup, test, iterations_per_test=5, tests_to_run=10):
    fastest_execution = min(timeit.Timer(test, setup=setup).repeat(tests_to_run, iterations_per_test))
    execution_time = fastest_execution / iterations_per_test
    fps = 1.0 / execution_time
    return execution_time, fps

setup = """
import face_recognition
import cv2

image = face_recognition.load_image_file("picture_of_me/{}")
small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
"""

test_from_face_locate_to_face_encording = """
face_location = face_recognition.face_locations(small_image, number_of_times_to_upsample=0, model="cnn")
face_encoding = face_recognition.face_encodings(small_image, known_face_locations=face_location)[0]
"""

for image in TEST_IMAGES:
    samples = image.split(".")[0]
    print("Timings at {}:".format(samples))
    print(" - End-to-end: {:.4f}s ({:.2f} fps)".format(*run_test(setup.format(image), test_from_face_locate_to_face_encording)))
    print()
