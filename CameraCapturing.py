import cv2
import face_recognition
import threading
import urllib
import datetime
import os

class CameraCapturing:
    def __init__(self, camera_url=0, student_images_path_name=[]):
        self.cap = cv2.VideoCapture(camera_url, cv2.CAP_V4L2)
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.know_image_encodings = []
        self.know_image_names = []
        self.capturing = False
        print(student_images_path_name)
        for student_image_path_name in student_images_path_name:
            response = urllib.request.urlopen(student_image_path_name[0])
            image = face_recognition.load_image_file(response)
            face_encoding = face_recognition.face_encodings(image)[0]
            self.know_image_encodings.append(face_encoding)
            self.know_image_names.append(student_image_path_name[1])

    def start(self):
        self.capturing = True
        self.thread = threading.Thread(target=self.capture)
        self.thread.start()

    def _find_in_faces(self, name):
        i = 0
        for face in self.face_names:
            if face["id"] == name:
                return i
            i += 1

        return -1

    def capture(self):
        while self.capturing:
            ids = []
            suc, image = self.cap.read()
            if suc:
                frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)
                unknown_count = -1
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        self.know_image_encodings, face_encoding
                    )
                    name = unknown_count

                    # # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.know_image_names[first_match_index]
                    else:
                        unknown_count -= 1

                    ids.append(name)

                for (top, right, bottom, left), name in zip(face_locations, ids):
                    face = image[top:bottom, left:right]
                    filename = datetime.datetime.now().strftime(f"{name}_%Y%m%d_%H%M%S.png")
                    cv2.imwrite(f"templates/static/faces/{filename}", face)
                    data = {
                        "id": name,
                        "faceFile": f"faces/{filename}",
                    }
                    faces_index = self._find_in_faces(name)
                    if faces_index == -1:
                        self.face_names.append(data)
                    else:
                        self.face_names[faces_index] = data

        self.cap.release()

    def stop_capturing(self):
        self.capturing = False
        del self.thread
        return self.face_names
