from os import listdir, makedirs
from os.path import isfile, join, exists, dirname
from shutil import copy2
import face_recognition


class Face:
    count = 0
    def __init__(self, encoding=False):
        self.encoding = encoding
        self.name = str(Face.count)
        Face.count += 1

class FaceCollection:
    def __init__(self, path="people/"):
        self.faces = []
        self.path = path

    def get_encodings(self):
        encodings = []
        for face in self.faces:
            encodings.append(face.encoding)
        return encodings

    def add(self, new_face=Face()):
        self.faces.append(new_face)


def get_faces(image_path):
    img = face_recognition.load_image_file(image_path)
    found_face_locations = face_recognition.face_locations(img)
    found_face_encodings = face_recognition.face_encodings(img)
    return found_face_encodings, found_face_locations


def images_from_directory(path="."):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    images = []
    for file in files:
        if file.endswith(".jpg"):
            images.append(file)
        if file.endswith(".png"):
            images.append(file)
    return images


def save_image(source, destination):
    dst_dir = dirname(destination)

    if not exists(dst_dir):
        print("Creating {}".format(dst_dir))
        makedirs(dst_dir)

    print("copying image to {}".format(destination))
    copy2(source, destination)


def init_known_faces(path):
    if exists(path):
        print("people path exists")
        #TODO try to init known faces based on people-directories
        return FaceCollection(path)
    else:
        return FaceCollection(path)


# go through images in directory
#   detect faces from each image
#       compare found faces to known faces
#           if matches
#               add image to known face's directory
#           else
#               create new face
if __name__ == "__main__":
    IMAGE_PATH = "images/"
    SAVE_PATH = "people/"
    KNOWN_FACES = init_known_faces(path=join(IMAGE_PATH, SAVE_PATH))

    IMAGES = images_from_directory(IMAGE_PATH)
    print(IMAGES)

    for image in IMAGES:
        try:
            face_encodings, face_locations = get_faces(join(IMAGE_PATH, image))
            face_count = len(face_encodings)

            print()
            print(image)
            print("faces found {}".format(face_count))

            for i in range(face_count):
                matches = []
                face_encoding = face_encodings[i]
                face_location = face_locations[i]

                # compare_faces returns known_faces length list of True/False values
                matches = face_recognition.compare_faces(KNOWN_FACES.get_encodings(), face_encoding)

                src = join(IMAGE_PATH, image)

                if True in matches:
                    #atm expects that found face matches only to one known face
                    j = matches.index(True)
                    dst = join(KNOWN_FACES.path, str(KNOWN_FACES.faces[j].name), image)
                else:
                    found_face = Face(face_encoding)
                    KNOWN_FACES.add(found_face)
                    dst = join(KNOWN_FACES.path, found_face.name, image)

                save_image(src, dst)

        except Exception as exception:
            print(exception)
            raise
