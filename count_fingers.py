import cv2

import mediapipe as mp


cap = cv2.VideoCapture(0)

mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils
hands=mp_hands.Hands(min_detection_confidence=0.5,min_tracking_confidence=0.5)

tip_ids=[4,8,12,16,20]

def countFingers(image,hand_landmarks,handNo=0):
    if hand_landmarks:
        landmarks=hand_landmarks[handNo].landmark
        fingers=[]
        for lm_index in tip_ids:
            fingerTipY=landmarks[lm_index].y
            fingerBottomY=landmarks[lm_index-2].y
            if lm_index !=4:
                if fingerTipY<fingerBottomY:
                    fingers.append(1)
                    print("finger With Id",lm_index," Is Open")
                
                if fingerTipY>fingerBottomY:
                    fingers.append(0)
                    print("finger With Id",lm_index," Is closed")
        totalFingers=fingers.count(1)
        print(totalFingers)
        cv2.putText(image,totalFingers,(50,50),cv2.FONT_HERSHEY_DUPLEX,1,(24,50,60),2)

def drawHandLandmarks(image,hand_landmarks):
    
    if hand_landmarks:
        
        for landmarks in hand_landmarks:
            mp_drawing.draw_landmarks(image,landmarks,mp_hands.HAND_CONNECTIONS)

while True:
    success, image = cap.read()
    image=cv2.flip(image,1)
    results=hands.process(image) 
    hand_landmarks=results.multi_hand_landmarks
    
    drawHandLandmarks(image,hand_landmarks)

    countFingers(image,hand_landmarks)
    cv2.imshow("Media Controller", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()

