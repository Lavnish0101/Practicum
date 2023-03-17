import cv2
import mediapipe as mp
class bdetec():
    def __init__(self,
               sim=False,
               mdcmp=1,
               slm=True,
               est=False,
               sst=True,
               rfc=False,
               mdc=0.5,
               mcc=0.5):
        self.sim=sim
        self.mdcmp=mdcmp
        self.slm=slm
        self.est=est
        self.sst=sst
        self.rfc=rfc
       
        self.mdc=mdc
        self.mcc=mcc
        self.bd=mp.solutions.holistic
        self.draw=mp.solutions.drawing_utils
        self.hf=self.bd.Holistic( self.sim,
                                    self.mdcmp,
                                    self.slm,
                                    self.est,
                                    self.sst,
                                    self.rfc)
    def find_bd(self,img,flag=False):
        #img=cv2.flip(img,1)
        irgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.processed_bd=self.hf.process(irgb)
        if self.processed_bd.pose_landmarks and flag:
             bdk= self.processed_bd.pose_landmarks
             self.draw.draw_landmarks(img,bdk,self.bd.POSE_CONNECTIONS)
        
        return img
    
    def find_pos(self,img,hand_no=0):
        cd_list=[]
        if self.processed_bd.pose_landmarks:
            bdk=self.processed_bd.pose_landmarks
            for id,lm in enumerate(bdk.landmark):
                 x,y,h=img.shape
                 cd_list.append([id,lm.x,lm.y,lm.z])
        return cd_list

        
def main():
    vid=cv2.VideoCapture(0)
    
    dct=bdetec()
    while vid.isOpened():
        fl,img=vid.read()
        img=cv2.flip(img,1)
        img=dct.find_bd(img,True)
        cd_list=dct.find_pos(img)
        if len(cd_list)!=0:
         print(cd_list[4])
        cv2.imshow('mc',img)
         

        if cv2.waitKey(1) & 0XFF==ord('a'):
            break
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main() 
