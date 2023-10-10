from __future__ import print_function
from imutils.video import WebcamVideoStream
import imutils
import cv2

vs = WebcamVideoStream(src=1).start()
while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=320)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break
cv2.destroyAllWindows()
vs.stop()