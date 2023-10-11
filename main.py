from imutils.video import WebcamVideoStream
import ShootingUDPServer
import imutils
import time
import cv2
import numpy as np


vid = WebcamVideoStream(src=1).start()
server = ShootingUDPServer.ShootingUDPServer().start()

max = 0
t = 240

    
#POINT MATRIX CALCULATION
curPoint = 0
increment = 10
points_src = np.array([[0, 0], [320, 0], [320, 240], [0, 240]], dtype=np.float32)
#points_src = np.array([[53,67],[256,73],[252,183],[55,186]], dtype=np.float32)
triggered = False
waiting = False
cooldown_time = 0.5
cooldown_end = 0

debug = False

while (True):
    frame = vid.read()
    small = imutils.resize(frame, width=320)

    smallgray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    ret, threshold = cv2.threshold(smallgray, t, 255, cv2.THRESH_BINARY)

    if (smallgray.max() > max):
        max = smallgray.max()

    #DETERMINATION OF HIGHEST LIGHT CENTERED POINT AFTER THRESHOLD
    contours, hierarchy = cv2.findContours(threshold, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
    if contours and not triggered:
        triggered = True
        cooldown_end = time.time() + cooldown_time
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        (x, y), radius = cv2.minEnclosingCircle(sorted_contours[0])
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(small, center, radius, (0, 255, 0), 1)
        if (debug):
            cv2.drawContours(small, [sorted_contours[0]], -1, (255, 0, 0), 1)
        point_p = np.array(center, dtype=np.float32)
        # # Matriz de transformación proyectiva
        matrix = cv2.getPerspectiveTransform(points_src, np.array([[0, 0], [320, 0], [320, 240], [0, 240]], dtype=np.float32))
        # # Transformación proyectiva del punto P
        point_p_transformed = cv2.perspectiveTransform(point_p.reshape(1, -1, 2), matrix)
        # # Coordenadas del punto P_p(x,y) transformado
        x_p_transformed, y_p_transformed = point_p_transformed[0][0]
        if waiting:
                points_src[curPoint][0] = x
                points_src[curPoint][1] = y
                waiting = False
        if  x_p_transformed >= 0 and x_p_transformed < 320 and y_p_transformed >= 0 and y_p_transformed<240:
            cv2.circle(small, (int(point_p[0]), int(point_p[1])), 0, (0, 255, 0), 3)
            cv2.circle(small, (int(x_p_transformed), int(y_p_transformed)), 0, (0, 0, 255), 3)
            # print(f"La coordenada del punto P transformado es ({x_p_transformed}, {y_p_transformed})")
            print(f"({x_p_transformed}, {y_p_transformed})")
            server.send(msg = str(x_p_transformed) + ", " + str(y_p_transformed))

    if triggered and time.time()> cooldown_end:
        triggered = False

    if debug:
        cv2.circle(small, (int(points_src[0][0]), int(points_src[0][1])), 0, (0, 255, 255 if curPoint==0 else 0), 3)
        cv2.circle(small, (int(points_src[1][0]), int(points_src[1][1])), 0, (0, 255, 255 if curPoint==1 else 0), 3)
        cv2.circle(small, (int(points_src[2][0]), int(points_src[2][1])), 0, (0, 255, 255 if curPoint==2 else 0), 3)
        cv2.circle(small, (int(points_src[3][0]), int(points_src[3][1])), 0, (0, 255, 255 if curPoint==3 else 0), 3)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('1'):
        curPoint = 0
        waiting = True
    if key == ord('2'):
        curPoint = 1
        waiting = True
    if key == ord('3'):
        curPoint = 2
        waiting = True
    if key == ord('4'):
        curPoint = 3
        waiting = True
    if key == ord('5'):
        increment = 1
    if key == ord('6'):
        increment = 10
    if key == ord('7'):
        print(f"new coords: [{points_src[0][0]},{points_src[0][1]}],[{points_src[1][0]},{points_src[1][1]}],[{points_src[2][0]},{points_src[2][1]}],[{points_src[3][0]},{points_src[3][1]}]")
    #Y-, Y+
    if key == ord('k'):
        points_src[curPoint][1] += increment
        if points_src[curPoint][1] > 240:
            points_src[curPoint][1] = 240
    if key == ord('i'):
        points_src[curPoint][1] -= increment
        if points_src[curPoint][1] < 0:
            points_src[curPoint][1] = 0
    #X+, X-            
    if key == ord('l'):
        points_src[curPoint][0] += increment
        if points_src[curPoint][0] > 320:
            points_src[curPoint][0] = 320
    if key == ord('j'):
        points_src[curPoint][0] -= increment
        if points_src[curPoint][0] < 0:
            points_src[curPoint][0] = 0
    if key == ord('r'):
        max = 0
    if key == ord('c'):
        debug = not (debug)
    elif key == ord('d'):
        t = t+10
        if (t > 255):
            t = 255
    elif key == ord('a'):
        t = t-10
        if (t < 0):
            t = 0
    elif key == ord('q'):
        break

    cv2.imshow('frame', small)

vid.release()
cv2.destroyAllWindows()