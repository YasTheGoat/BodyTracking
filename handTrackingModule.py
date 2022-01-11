from turtle import fillcolor
import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self):
        self.mpHolistic = mp.solutions.holistic
        self.holistic = self.mpHolistic.Holistic()

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()

        self.mpDraw = mp.solutions.drawing_utils

    def findHand(self , frame, back, draw=True, face_pose=False):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.handResults = self.hands.process(imgRGB)
        bodyResults = self.holistic.process(imgRGB)

        if self.handResults.multi_hand_landmarks:
            for handLms in self.handResults.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(back, handLms, self.mpHands.HAND_CONNECTIONS)

        if draw and face_pose:
            self.mpDraw.draw_landmarks(back, bodyResults.face_landmarks)
            self.mpDraw.draw_landmarks(back, bodyResults.pose_landmarks, self.mpHolistic.POSE_CONNECTIONS)

        return back
    
    def findPosition(self, back, HandNo=0, finger=0, draw=True):
        lmList = []

        if self.handResults.multi_hand_landmarks:
            myHand = self.handResults.multi_hand_landmarks[HandNo]
            for id, lm in enumerate(myHand.landmark):
                h,w,c = back.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if id==finger and draw:
                    cv2.circle(back, (cx,cy), 10, (255,0,255),cv2.FILLED)
            
        return lmList



##############
#DUMMY CODE
#############


# def main():
#     webcam = cv2.VideoCapture(0)

#     ctime = 0
#     ptime = 0   

#     detector = handDetector()
#     while True:
#         back = cv2.imread("./back.jpg")
#         success, frame = webcam.read()
#         frame = cv2.flip(frame,1)

#         back = detector.findHand(frame, back)
#         lmList = detector.findPosition(back)

#         if len(lmList) != 0:
#             print(lmList[4])

#         ctime = time.time()
#         fps = 1/(ctime-ptime)
#         ptime = ctime

#         cv2.putText(back, f'FPS:{int(fps)}', (10,70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

#         cv2.imshow("handTracking", back)
#         key = cv2.waitKey(1)
#         if key == 81 or key == 113:
#             break



# if __name__ == "__main__":
#     main()



##############
#DUMMY CODE
#############
