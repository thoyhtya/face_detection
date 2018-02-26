import face_recognition
from os import listdir, makedirs
from os.path import isfile, join, exists, dirname
from shutil import copy2


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

    def add(self, face=Face()):
        self.faces.append(face)


def getFaces(imagePath):
    image = face_recognition.load_image_file(imagePath)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image)
    return face_encodings, face_locations


def imagesFromDirectory(path="."):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    images = []
    for file in files:
        if file.endswith(".jpg"):
            images.append(file)
        if file.endswith(".png"):
            images.append(file)
    return images


def saveImage(src, dst):
    dst_dir = dirname(dst)

    if not exists(dst_dir):
        print("Creating {}".format(dst_dir))
        makedirs(dst_dir)

    print("copying image to {}".format(dst))
    copy2(src, dst)
    

def initKnownFaces(path):
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
    imagePath = "images/"
    savePath = "people/"
    known_faces = initKnownFaces( path=join(imagePath, savePath) )

    images = imagesFromDirectory(imagePath)
    print(images)

    for image in images:
        try:
            face_encodings, face_locations = getFaces( join(imagePath, image))
            face_count = len(face_encodings)

            print()
            print(image)
            print("faces found {}".format(face_count))

            for i in range(face_count):
                matches = []
                face_encoding = face_encodings[i]
                face_location = face_locations[i]

                # compare_faces returns known_faces length list of True/False values
                matches = face_recognition.compare_faces(known_faces.get_encodings(), face_encoding)

                src = join(imagePath, image)

                if True in matches:
                    #atm expects that found face matches only to one known face
                    j = matches.index(True)
                    dst = join(known_faces.path, str(known_faces.faces[j].name), image)
                else:
                    face = Face(face_encoding)
                    known_faces.add(face)
                    dst = join(known_faces.path, face.name, image)

                saveImage(src, dst)

        except Exception as e:
            print(e)
            raise
