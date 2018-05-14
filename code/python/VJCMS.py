#!/usr/bin/env python
# Author: Maximilian Langohr


#stamdard libs
from termcolor import colored
import cv2
import numpy as np
import socket
import sys
import struct
import threading
import argparse
from copy import copy, deepcopy
import time

#custome classes and libs
from utils.objdetector import ObjDetector
#from VideoStream import VideoStream
from utils.Viola import Viola
import utils.VJ_Exceptions as vje
from utils.VJ_Logging import VJ_Logging

# Parsing arguments

parser = argparse.ArgumentParser(prog='VJCMS.py', description='processing life video-feed, to detect trafic cones and trafic signs')
parser.add_argument('--debug',metavar='-d', type=int, nargs='?', const=1, default=0, help='0 = use PiCamera 1 = use video (Default = 0)')
parser.add_argument('--mode', metavar='-m', type=int, nargs='?', const=1, default=0, help='0 = detect and track, 1 = detect, 2 = optimized (Default = 0)')
parser.add_argument('--video', action='store_true',help="if true, safes video of current session")
parser.add_argument('--network', metavar='-n', type=int,nargs='?',const=1, default=0, help='0 = stream to local monitor, 1 = stream to network, 2 = no Videostream at all   (Default = 0)')
parser.add_argument('--ip', metavar='-ip', default='localhost', help='ip adress of server (Default = localhost)')
parser.add_argument('--port', metavar='-port', default=5001, help='port of server (Default = 5001)')
parser.add_argument('--verbose', metavar='-v', type=int,nargs='?',const=1,default=2, help=' 0 = INFO, 1 = INFO, WARNING, 2= INFO, WARNING, ERROR (Default = 0)')
#parser.add_argument('--ratio', metavar='-r', type=int, nargs='?',const=1,default=3, help='Set the RATIO by which you want to resize the picture (Default = 3)')
parser.add_argument('--track', metavar='-t' , type=int, nargs='?',const=1, default=50, help='Number of frames you want to track the object after detection (Default = 50)')
parser.add_argument('--skip', metavar='-s', type=int, nargs='?', const=1, default =5, help='Number of frames to bes skipped if no object is found (Default = 5)')
parser.add_argument('--objects' ,metavar='-o', action='append', default=['cone'], choices={'cone','stop','face','way','yield'}, help='List of objects to track {cone, stop, face, way, yield} (Default = cone)')



args = parser.parse_args()

# connect to camera and check if frame can be read
# depending on debug mode the video is used instead
cap = cv2.VideoCapture(0)
if(args.debug == 1):
    cap = cv2.VideoCapture('videos/smartcam_debug.mp4')

if (cap.isOpened() == False):
    logger.print_log(2,'pre main','camera could not be found or frame could not be read')
    raise vje.CameraNotConnected()


# global states or flags
TCP_IP = args.ip
TCP_PORT = args.port
logger = VJ_Logging('vjcms',args.verbose)
#frame is used as a global variable to share the current frame among the diffrent methods
frame = 0
#important Variables
WIDTH = int(cap.get(3))
HEIGHT = int(cap.get(4))
NETWORK =  args.network
MODE = args.mode
OBJECTS = args.objects
VIDEO = args.video
TRACK = args.track
SKIP = args.skip

# initialize the termination criteria for CAMSHIFT, indicating
# a maximum of ten iteRATIOns or movement by a least one pixel
# along with the bounding box of the ROI
termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)




# VideoWriter to create avi file
output_video = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'),25,(WIDTH,HEIGHT))

#start timer for FPS output
start_time = time.time()
fps_interval = 1 # displays the frame rate every 1 second
fps_counter = 0
fps = 0
####################################################################################################################
# is responsable for outputing frame to local monitor or Network, depending on NETWORK
def view(frame):
    s = None
    global start_time
    global fps_counter
    global fps_interval
    global fps
    fps_counter+=1

    if (time.time() - start_time) > fps_interval :
        fps = fps_counter / (time.time() - start_time)
        fps_counter = 0
        start_time = time.time()
        logger.log_fps(int(fps))
    cv2.putText(frame, "FPS: " + str(int(fps)) ,(WIDTH-150, HEIGHT-30),cv2.FONT_HERSHEY_COMPLEX_SMALL,.7,(225,0,0))

    if (NETWORK == 0):
        cv2.imshow("Objects",frame)
    elif (NETWORK == 1):
        try:
            sock = socket.socket()
        except socjet.error as mag:
            logger.print_log(2,'view','could not open socket')
            return
        try:
            sock.connect((TCP_IP, TCP_PORT))
        except socket.error as msg:
            logger.print_log(2,'view','could not open socket')
            s = None
            return
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(imgencode)
        stringData = data.tostring()
        sock.send( str(len(stringData)).ljust(16));
        sock.send( stringData )

    if VIDEO == True:
        output_video.write(frame)

####################################################################################################################
# shows the next SKIP# frames without detection or tracking
def justShow():
    global cap,SKIP, frame
    for k in range(0,SKIP):
        ret, frame = cap.read()
        if not ret:
            logger.print_log(1,'justShow','could not read frame from stream')
            break
        view(frame)
        cv2.waitKey(1)


####################################################################################################################
# track the objects found using CAMSHIFT algorithm
def trackObj(allRoiPts, allRoiHist):
    copy = deepcopy(allRoiPts)
    global frame
    for k in range(0, TRACK):
        ret, frame = cap.read()
        if not ret:
            logger.print_log(2,'trackObj','could not read frame from stream')
            return -1
            break
        i = 0
        k = 0
        #convert the given frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #For histogram of each window found, back project them on the current frame and track using CAMSHIFT
        for roiHist in allRoiHist:
            # Perform mean shift
            backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)
            # Apply cam shift to the back projection, convert the
            # points to a bounding box, and then draw them
            temp = (allRoiPts[i][0],allRoiPts[i][1],allRoiPts[i][2],allRoiPts[i][3])
            (r, allRoiPts[i]) = cv2.CamShift(backProj, temp, termination)
            #Error handling for bound exceeding
            for j in range(0,4):
                if allRoiPts[i][j] < 0:
                    allRoiPts[i][j] = 0
            pts = np.int0(cv2.boxPoints(r))
            #Draw bounding box around new position of the object
            cv2.polylines(frame, [pts], True, (0, 255, 255), 2)
            cv2.putText(frame,copy[i][4],(allRoiPts[i][0],allRoiPts[i][1]),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
            i = i + 1
            k = k + 1
        view(frame)
        cv2.waitKey(1)
    return 1

##########################################################################################################################
# calculates histogram of detected areas
def calHist(allRoiPts):
    orig = frame.copy()
    allRoiHist = []
    #For each object found, convert it to HSV and calculate the histogram of
    #that region
    for (x1,y1,x2,y2,tag) in allRoiPts:
        roiPts= [x1,y1,x2,y2]
        # Grab the ROI for the bounding box by cropping and convert it
        # to the HSV color space.
        roi = orig[roiPts[1]:roiPts[-1], roiPts[0]:roiPts[2]]
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # compute a HSV histogram for the ROI and store the
        # bounding box
        roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
        roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
        allRoiHist.append(roiHist);
    return allRoiHist
##########################################################################################################################
# printing bounding-boxes around objects and return frame
def print_boxes(frame,boxes):
    for (x,y,w,h,tag) in boxes:
        cv2.rectangle(frame,(x,y),(w,h) , (0, 255, 255), 2)
        cv2.putText(frame,tag,(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
    return frame

##########################################################################################################################
# detects and tracks objects identified by Viola Jones using CAMSHIFT
def detect_and_track():
    logger.print_log(0,'detect_and_track','Begin detect_and_track' )
    global cap
    global frame
    MAINFLAG = True
    logger.print_log(0,'detect_and_track','starting Thread for Viola')
    # Start viola in a diffrent thread
    viola = Viola().start()

    i=0
    logger.print_log(0,'detect_and_track','opening input stream')
    while(cap.isOpened()):
        # Try to find the objects using Viola-Jones. If objects are found, give the
        # pass to track it else for next five frames don't check any objects. Repeat until
        # a object is found in the frame
        if MAINFLAG:
            #Before each call empty the pervious objects and their hsv histograms
            allRoiPts = []
            allRoiHist = []
            ret, frame = cap.read()
            if not ret:
                logger.print_log(2,'detect_and_track','could not read frame from stream')
                cap.release()
                cv2.destroyAllWindows()
                return -1
            # save the objects found in the frame into a list
            allRoiPts = viola.find_objects(frame,OBJECTS)
            logger.log_boxes(allRoiPts)
            # Check if objects were found in the given frame
            if len(allRoiPts) != 0:
                allRoiHist = calHist(allRoiPts)
                MAINFLAG = False
            else:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logger.print_log(0,'detect_and_track','ending program now')
                    viola.stop()
                    break
                justShow()
        else:
            # Track the object found by viola jones for next TRACK number of frames using cam shift
            error = trackObj(allRoiPts, allRoiHist)
            if error == -1:
                logger.print_log(2,'detect_and_track','trackObj returned an error ' + str(error))
                cap.release()
                cv2.destroyAllWindows()
                viola.stop()
                return -1

            MAINFLAG = True
       		#Exit on key press of q
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.print_log(0,'detect_and_track','ending program now')
                viola.stop()
                break
    out.release()
    cv2.destroyAllWindows()
    return
####################################################################################################################
# detects objects in stream and sends positions to Output-Generator
def detect():
    global cap
    global frame
    viola = Viola().start()
    while (cap.isOpened()):
        #justShow()
        ret,frame = cap.read()
        cv2.waitKey(1)
        if not ret:
            logger.print_log(1,'detect','could not read frame from stream')
            cap.release()
            cv2.destroyAllWindows()
            viola.stop()
            return -1

        objects = viola.find_objects(frame,OBJECTS)
        if(len(objects) != 0):
            output_frame = print_boxes(frame,objects)
            view(output_frame)
            logger.log_boxes(objects)
            cv2.waitKey(1)
        else:
            view(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.print_log(0,'detect_and_track','ending program now')
            viola.stop()
            break
    return

####################################################################################################################
# optimized detection mode, which only focuses on ROI where treffic signs might appear

def optimized():
    global cap
    global frame
    global HEIGHT
    global WIDTH
    viola_left = Viola().start()
    viola_right = Viola().start()
    ret,frame = cap.read()
    while (cap.isOpened()):
        ret, frame = cap.read()
        cv2.waitKey(1)

        if not ret:
            logger.print_log(1,'optimized','could not read frame from stream')
            cap.release()
            cv2.destroyAllWindows()
            viola_left.stop()
            viola_right.stop()
            return -1

        seperator = round(WIDTH/3)
        roi_left = frame[0:HEIGHT,0:int(seperator)]
        roi_right = frame[0:HEIGHT,int(2*seperator):WIDTH]


        obj_left = viola_left.find_objects(roi_left,OBJECTS)
        obj_right = viola_right.find_objects(roi_right,OBJECTS)

        for (x,y,a,b,tag) in obj_right:
            obj_left.append((int(2*seperator + x),y,int(2*seperator+a),b,tag))
        if (len(obj_left) != 0):
            output_frame = print_boxes(frame,obj_left)
            view(output_frame)
            logger.log_boxes(obj_left)
            cv2.waitKey(1)
        else:
            view(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.print_log(0,'detect_and_track','ending program now')
            viola_left.stop()
            viola_right.stop()
            break
    return

####################################################################################################################
# coordinates what mode to use and some logging
def main():
    if ( MODE == 0):
        if (detect_and_track() != 0):
            logger.print_log(2,'main','dectect_and_track(): terminated with an error')
            return
    elif (MODE == 1):
        if (detect() != 0):
            logger.print_log(2,'main','dectect(): terminated with an error')
            return
    elif (MODE == 2):
        if(optimized() != 0):
            logger.print_log(2,'main','optimized(): terminated with an error')
    else:
        logger.print_log(2,'main','Invalid Mode')
        raise vje.InvalidMode()
        return
    return



####################################################################################################################
# call main() function
# get that shit going
if __name__ == "__main__":
    logger.print_log(0,'main','starting program')
    if (NETWORK == False):
        logger.print_log(0,'main','streaming to monitor')
    else:
        logger.print_log(0,'main','streaming to network')
    logger.print_log(0,'main', 'DEBUG ' + str(args.debug))
    logger.print_log(0,'main','MODE ' + str(args.mode))
    logger.print_log(0,'main','VERBOSE ' + str(args.verbose))
    main()
    sys.exit(1)
