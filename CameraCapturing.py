import cv2
import face_recognition
import threading

class CameraCapturing:

    def __init__(self, camera_url=0, student_images_path_name=[]):
        self.cap = cv2.VideoCapture(camera_url, cv2.CAP_V4L2)
        self.face_locations = []
        self.face_encodings = []
        self.face_names = set()
        self.know_image_encodings = []
        self.know_image_names = []
        self.capturing = False
        for student_image_path_name in student_images_path_name:
            image = face_recognition.load_image_file(student_image_path_name[0])
            face_encoding = face_recognition.face_encodings(image)[0]
            self.know_image_encodings.append(face_encoding)
            self.know_image_names.append(student_image_path_name[1])
    def start(self):
        self.capturing = True
        self.thread = threading.Thread(target=self.start_capturing)
        self.thread.start()
        
    def start_capturing(self):
        while self.capturing:
            print(self.capturing)
            suc, frame = self.cap.read()
            if suc:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)
                name = ""
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.know_image_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.know_image_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    # best_match_index = np.argmin(face_distances)
                    # if matches[best_match_index]:
                        # name = known_face_names[best_match_index]

                    self.face_names.add(name)
                # Display the results
                # cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                # time.sleep(10)

        self.cap.release()
    
    def stop_capturing(self):
        self.capturing = False
        return list(self.face_names)
        