import cv2
import time
import handTrackingModule as htm
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def run(showfps, background, body, showVol, isControllable):
    webcam = cv2.VideoCapture(0)

    ctime = 0
    ptime = 0   

    volBar = 0
    vol = 0

    detector = htm.handDetector()


    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMasterVolumeLevel()
    # volume.SetMasterVolumeLevel(-20.0, None)
    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]


    while True:
        back = cv2.imread("./back.jpg")
        success, frame = webcam.read()
        frame = cv2.flip(frame,1)
        
        if background.lower() == 'y':
            back = frame

        back = detector.findHand(frame, back, face_pose=body)
        lmList = detector.findPosition(back,draw=False)

        if len(lmList) != 0 and isControllable.lower() == 'y':
            #print(lmList[4], lmList[8])

            #index and thumb length
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1+x2)//2, (y1+y2)//2

            #confirm finger and wrist
            x3, y3 = lmList[20][1], lmList[20][2]
            x4, y4 = lmList[0][1], lmList[0][2]
            c_x, c_y = (x3+x4)//2, (y3+y4)//2

            cv2.circle(back, (x1,y1), 5, (255,0,255),cv2.FILLED)
            cv2.circle(back, (x2,y2), 5, (255,0,255),cv2.FILLED)
            cv2.line(back, (x1,y1),(x2,y2), (255, 0, 255), 3)
            cv2.circle(back, (cx,cy), 5, (255,0,255),cv2.FILLED)

            cv2.circle(back, (x3,y3), 5, (255,0,255),cv2.FILLED)
            cv2.circle(back, (x4,y4), 5, (255,0,255),cv2.FILLED)
            cv2.line(back, (x3,y3),(x4,y4), (255, 0, 255), 3)
            cv2.circle(back, (c_x,c_y), 5, (255,0,255),cv2.FILLED)

            length1 = math.hypot(x2-x1,y2-y1)
            length2 = math.hypot(x4-x3,y4-y3)

            vol = np.interp(length1, [50,200], [minVol, maxVol])
            volBar = np.interp(length1, [50,200], [500, 150])

            if length1 < 25:
                cv2.circle(back, (cx,cy), 15, (0,255,0),cv2.FILLED)
                volume.SetMute(1, None)
            else:
                volume.SetMute(0, None)

            if length2 < 200:
                if length1 < 25:
                    volume.SetMute(1, None)
                else:
                    volume.SetMute(0, None)
                    volume.SetMasterVolumeLevel(vol, None)



        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime

        volumeDisplay = ((vol + 65.25) / 65.25) * 100

        if showfps.lower() == 'y':
            cv2.putText(back, f'FPS:{int(fps)}', (10,70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        if showVol.lower() == 'y':
            cv2.rectangle(back,(50,int(volBar)),(84,500),(0,255,0), cv2.FILLED)
            cv2.rectangle(back,(50,150),(84,500),(0,255,0),3)
            cv2.putText(back, f'VOL:{int(volume.GetMasterVolumeLevel())} / {int(volumeDisplay)}', (10,100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)


        cv2.imshow("hand Tracking", back)
        key = cv2.waitKey(1)
        if key == 81 or key == 113:
            break