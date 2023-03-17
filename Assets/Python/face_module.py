import cv2
import mediapipe as mp
class facedetec():
    def __init__(self,
               sim=False,
               face_num=1,
               rfc=False,
               mdc=0.5,
               mcc=0.5):
        self.sim=sim
        self.face_num=face_num
        self.rfc=rfc
        self.mdc=mdc
        self.mcc=mcc
        self.face=mp.solutions.face_mesh
        self.draw=mp.solutions.drawing_utils
        self.hf=self.face.FaceMesh(self.sim,
                                        self.face_num,
                                        self.rfc,
                                        self.mdc,
                                        self.mcc)
    def find_face(self,img,flag=False):
        #img=cv2.flip(img,1)
        irgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.processed_face=self.hf.process(irgb)
        if self.processed_face.multi_face_landmarks and flag:
            for fck in self.processed_face.multi_face_landmarks:
            #     self.draw.draw_landmarks( image=img,
            # landmark_list=fck,
            # connections=self.face.FACEMESH_TESSELATION,
            # landmark_drawing_spec=None,
            #     )
             self.draw.draw_landmarks(img,fck)
        
        return img
    
    def find_pos(self,img,face_no=0):
        cd_list=[]
        if self.processed_face.multi_face_landmarks:
            fck=self.processed_face.multi_face_landmarks[face_no]
            for fck in self.processed_face.multi_face_landmarks:
                  for id,lm in enumerate(fck.landmark):
                      x,y,h=img.shape
                      cd_list.append([id,lm.x,lm.y,lm.z])
        return cd_list

        
def main():
    vid=cv2.VideoCapture(0)
    
    dct=facedetec()
    while vid.isOpened():
        fl,img=vid.read()
        img=cv2.flip(img,1)
        img=dct.find_face(img,True)
        cd_list=dct.find_pos(img)
        if len(cd_list)!=0:
         print(cd_list[4],cd_list[1])
        cv2.imshow('mc',img)
         

        if cv2.waitKey(1) & 0XFF==ord('a'):
            break
cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
 