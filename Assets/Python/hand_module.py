import cv2
import mediapipe as mp
class handetec():
    def __init__(self,
               sim=False,
               hand_num=2,
               mdcmp=1,
               mdc=0.5,
               mcc=0.5):
        self.sim=sim
        self.hand_num=hand_num
        self.mdcmp=mdcmp
        self.mdc=mdc
        self.mcc=mcc
        self.hands=mp.solutions.hands
        self.draw=mp.solutions.drawing_utils
        self.hf=self.hands.Hands(self.sim,
                                        self.hand_num,
                                        self.mdcmp,
                                        self.mdc,
                                        self.mcc)
    def find_hands(self,img,flag=False):
        #img=cv2.flip(img,1)
        irgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.processed_hands=self.hf.process(irgb)
        if self.processed_hands.multi_hand_landmarks and flag:
            for handk in self.processed_hands.multi_hand_landmarks:
                self.draw.draw_landmarks(img,handk,self.hands.HAND_CONNECTIONS)
        
        return img
    
    def find_pos(self,img,hand_no=0):
        cd_list=[]
        if self.processed_hands.multi_hand_landmarks:
            if hand_no<len(self.processed_hands.multi_hand_landmarks):
                handk=self.processed_hands.multi_hand_landmarks[hand_no]
                for id,lm in enumerate(handk.landmark):
                        x,y,h=img.shape
                        
                        cd_list.append([id,lm.x,lm.y,lm.z])
        return cd_list

        
def main():
    vid=cv2.VideoCapture(0)
    
    dct=handetec()
    while vid.isOpened():
        fl,img=vid.read()
        img=cv2.flip(img,1)
        img=dct.find_hands(img,True)
        cd_list=dct.find_pos(img)
        if len(cd_list)!=0:
         print(cd_list[8])
        cv2.imshow('mc',img)
         

        if cv2.waitKey(1) & 0XFF==ord('a'):
            break
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
 