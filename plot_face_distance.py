import face_recognition
import matplotlib.pyplot as plt
import time
import pandas as pd
import seaborn as sns

# Load some images to compare against
picture = face_recognition.load_image_file("picture_of_me/0.jpg")
face_location = face_recognition.face_locations(picture, number_of_times_to_upsample=0, model="cnn")
encoding = face_recognition.face_encodings(picture,known_face_locations=face_location)[0]
my_face_encodings = []
unknown_face_encodings = []
my_face_failure_count = 0
unknown_face_failure_count = 0

print("load images")
for i in range(100):
    picture_of_me = face_recognition.load_image_file("picture_of_me/"+str(i)+".jpg")
    unknown_picture = face_recognition.load_image_file("unknown_picture/"+str(i)+".jpg")
    try:
        my_face_location = face_recognition.face_locations(picture_of_me, number_of_times_to_upsample=0, model="cnn")
        my_face_encoding = face_recognition.face_encodings(picture_of_me,known_face_locations=my_face_location)[0]
        my_face_encodings.append(my_face_encoding)
    except:
        my_face_failure_count += 1
    try:
        unknown_location = face_recognition.face_locations(unknown_picture, number_of_times_to_upsample=0, model="cnn")
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture,known_face_locations=unknown_location)[0]
        unknown_face_encodings.append(unknown_face_encoding)
    except:
        unknown_face_failure_count += 1
    if i == 50:
        print("Completes to load 50 images")
        print("Please wait to load the rest of 50 images")

print("loading completes")
print(my_face_failure_count,unknown_face_failure_count)

my_face_distances = face_recognition.face_distance(my_face_encodings,encoding)
unknown_face_distances = face_recognition.face_distance(unknown_face_encodings,encoding)

my_face_distances = my_face_distances[0:100]
unknown_face_distances = unknown_face_distances[0:100]

sns.set()
sns.set_style('whitegrid')
sns.set_palette('Set3')

df = pd.DataFrame({
    'picture_of_me': my_face_distances,
    'unknown_picture': unknown_face_distances
})

df_melt = pd.melt(df)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
sns.boxplot(x='variable', y='value', data=df_melt, showfliers=False, ax=ax)
sns.stripplot(x='variable', y='value', data=df_melt, jitter=True, color='black', ax=ax)
ax.set_xlabel('me? or others?')
ax.set_ylabel('Face distance')
ax.set_ylim(0, 1)

plt.show()
