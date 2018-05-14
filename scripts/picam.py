import time
import picamera

number_of_frames = 63
time_between_frames = 1 #in seconds
output_path = "/home/pi/camera/"
output_file_name = "bg.txt"



output =  open(output_path + output_file_name, 'w')
with picamera.PiCamera() as camera:
	camera.resolution = (640,480)
	camera.start_preview()
	for i in range(0,number_of_frames):
		time.sleep(time_between_frames)
		camera.capture(output_path + "img"+ str(i)+'.jpg')
		output.write("img/" + "img"+ str(i)+".jpg\n")
