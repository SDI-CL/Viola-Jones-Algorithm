# import the necessary packages
import cv2

class ObjDetector:
	def __init__(self, objCascadePath):
		self.objCascade = cv2.CascadeClassifier(objCascadePath)

	def detect(self, image, scaleFactor = 1.1, minNeighbors = 5, minSize = (30, 30)):
		rects = self.objCascade.detectMultiScale(image,
			scaleFactor = scaleFactor, minNeighbors = minNeighbors,
			minSize = minSize, flags = cv2.CASCADE_SCALE_IMAGE)

		# return the rectangles representing bounding
		# boxes around the objects
		return rects
