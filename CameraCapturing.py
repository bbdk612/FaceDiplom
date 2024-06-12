import cv2
import face_recognition
import threading
import urllib
import datetime
import os


class CameraCapturing:
    def __init__(self, camera_url=0, student_images_path_name=[]):
        """
        Initialize the CameraCapturing class with the given parameters.

        Parameters:
        camera_url (int, optional): The URL or index of the camera to capture frames from. Defaults to 0.
        student_images_path_name (list, optional): A list of tuples, where each tuple contains the URL of a student image and the corresponding name. Defaults to an empty list.

        Returns:
        None
        """
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
        """
        Begins the camera capturing process in a separate thread.

        This method sets the capturing flag to True, creates a new thread, and starts the thread.
        The thread will continuously capture frames from the camera, detect faces, and identify them.
        The identified faces will be stored in the 'face_names' attribute.

        Parameters:
        None

        Returns:
        None
        """
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
        """
        Continuously captures frames from the camera, detects faces, and identifies them.
        Saves the detected faces as images in the specified directory.
        Updates the 'face_names' attribute with the identified faces.

        Parameters:
        None

        Returns:
        None
        """
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

                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.know_image_names[first_match_index]
                    else:
                        unknown_count -= 1

                    ids.append(name)

                for (top, right, bottom, left), name in zip(face_locations, ids):
                    face = image[top:bottom, left:right]
                    filename = datetime.datetime.now().strftime(
                        f"{name}_%Y%m%d_%H%M%S.png"
                    )
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
        """
        Stops the camera capturing process and releases the camera resource.

        This method sets the capturing flag to False, waits for the capturing thread to finish,
        and then releases the camera resource. It also returns the list of identified faces.

        Parameters:
        None

        Returns:
        list: A list of dictionaries containing the identified faces. Each dictionary has the following keys:
              - 'id': The name or identifier of the face.
              - 'faceFile': The file path of the saved face image.
        """
        self.capturing = False
        del self.thread
        return self.face_names
