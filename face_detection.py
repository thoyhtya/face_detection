import face_recognition
import cv2
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


#TODO remove or refactor
def showImage(file, face_encodings, face_locations, known_face_encodings, known_face_names):
	image = face_recognition.load_image_file("keios.jpg", mode='RGB')
	image2 = face_recognition.load_image_file(file, mode='RGB')
	face_names = []
	for face_encoding in face_encodings:
		# See if the face is a match for the known face(s)
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
		name = "Unknown"

		# If a match was found in known_face_encodings, just use the first one.
		if True in matches:
			print("Found match 8)")
			first_match_index = matches.index(True)
			name = known_face_names[first_match_index]

	face_names.append(name)
	print(face_names)

	for (top, right, bottom, left), name in zip(face_locations, face_names):
		# Draw a box around the face
		cv2.rectangle(image2, (left, top), (right, bottom), (0, 0, 255), 2)

		# Draw a label with a name below the face
		cv2.rectangle(image2, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(image2, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


	img_to_show = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	img_to_show2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

	#stackowerflow
	# img =  cv2.imread('2-d.jpg')
	# cv2.namedWindow("test", cv2.WND_PROP_FULLSCREEN)          
	# cv2.setWindowProperty("test", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
	# cv2.imshow("test",img)

	# Display the resulting image
	# cv2.imshow('asd', img_to_show)

	cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)	
	cv2.imshow('Video', img_to_show2)

	cv2.waitKey(5000)
	cv2.destroyAllWindows()


def imagesFromDirectory(path="."):
	files = [f for f in listdir(path) if isfile(join(path, f))]
	return files

def saveImage(src, dst):
	dst_dir = dirname(dst)

	if not exists(dst_dir):
		print("Creating {}".format(dst_dir))
		makedirs(dst_dir)

	print("copying image to {}".format(dst))
	copy2(src, dst)


# go through images in directory
# 	detect faces from each image
# 		compare found faces to known faces
# 			if matches
# 				add image to known face's directory
# 			else
# 				create new face
if __name__ == "__main__":
	imagePath = "images/"
	savePath = "people/"
	known_faces = FaceCollection( path=join(imagePath, savePath) )

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
