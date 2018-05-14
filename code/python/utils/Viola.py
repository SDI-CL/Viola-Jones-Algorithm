from termcolor import colored
from utils.objdetector import ObjDetector
from threading import Thread, Lock

import cv2
import numpy as np



class Viola:
	RATIO = 3
	def __init__(self):
		self.termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
		self.frame = 0
		self.started = False
		self.read_lock = Lock()

	def start(self):
		if self.started:
			return None
		self.started = True
		self.thread = Thread(target=self.update, args=())
		self.thread.start()
		return self

	def update(self):
		while self.started:
			self.read_lock.acquire()
			self.read_lock.release()


	def set_frame(self,frame):
		self.read_lock.acquire()
		self.frame = frame
		self.read_lock.release()

	def stop(self):
		self.started = False
		self.thread.join()

	def tag_list(self,list, tag):
		result = []
		for (x,y,w,h) in list:
			x = self.RATIO*(x+10)
			y = self.RATIO*(y+10)
			w = self.RATIO*(w-15)
			h = self.RATIO*(h-15)
			result.append((x,y,x+w,y+h,tag))
		return result

	def find_objects(self,frame,list):
		allRoiPts = []
		allClasses = []
		allRects = []
		result = []
		frame_copy = frame.copy()
		dim = (frame.shape[1]/self.RATIO, frame.shape[0]/self.RATIO);
		resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
		gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
		#geht durch die Liste der Objecte und erstellt fuer jedes Object ein Viola-Modul
		for elem in list:
			if (elem == "cone"):
				coneDetect = ObjDetector('cascades/cone_cascade.xml')
				ConeRects = coneDetect.detect(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (10, 10))
				allRects.append(self.tag_list(ConeRects,'Cone'))
			if (elem == "stop"):
				stopDetect = ObjDetector('cascades/haarcascade_stop_sign.xml')
				stopRects = stopDetect.detect(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (10, 10))
				allRects.append(self.tag_list(stopRects,'Stop'))
			if (elem == "face"):
				faceDetect = ObjDetector('cascades/haarcascade_frontalface_default.xml')
				faceRects = faceDetect.detect(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (10, 10))
				allRects.append(self.tag_list(faceRects,'Face'))
			if (elem == "way"):
				wayDetect = ObjDetector('cascades/vorfahrt_cascade.xml')
				wayRects = wayDetect.detect(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (10, 10))
				allRects.append(self.tag_list(wayRects,"Right_of_way"))
			if (elem == "yield"):
				wayDetect = ObjDetector('cascades/yield_cascade.xml')
				wayRects = wayDetect.detect(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (10, 10))
				allRects.append(self.tag_list(wayRects,"Yield"))
		for rects in allRects:
			for entry in rects:
				result.append(entry)

		return result
