import socket
import face_module,hand_module,hlstc_module
import cv2
import mediapipe as mp

host, port = "127.0.0.1", 25001
data = "1,2,3"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck2= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck3= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck4= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
vid=cv2.VideoCapture(0)
    
dct=face_module.facedetec()
hnd=hand_module.handetec()
hls=hlstc_module.bdetec()
sock.connect((host, port)) 
sck2.connect((host,25002))
sck3.connect((host,25003))
sck4.connect((host,25004))
try:
  while vid.isOpened():
      fl,img=vid.read()
      img=cv2.flip(img,1)
      img=dct.find_face(img,True)
      img=hnd.find_hands(img,True)
      img =hls.find_bd(img,True)
      cd_list=dct.find_pos(img)
      hnd_lst=hnd.find_pos(img)
      hnd_lst2=hnd.find_pos(img,1)
      bd_list=hls.find_pos(img)
      fn_list=[cd_list,hnd_lst,bd_list]
      if len(cd_list)!=0:
                  f_list=str(cd_list)
                  # Connect to the server and send the data
                  sock.sendall(f_list.encode("utf-8"))
                #   print (f_list)
      
      if len(hnd_lst)!=0:
                  f_list=str(hnd_lst)
                  # Connect to the server and send the data
                  sck2.sendall(f_list.encode("utf-8"))
                  print (f_list)
      if len(hnd_lst2)!=0:
                  f_list=str(hnd_lst2)
                  # Connect to the server and send the data
                  sck3.sendall(f_list.encode("utf-8"))
                  print (f_list)
      if len(bd_list)!=0:
                  f_list=str(bd_list)
                  # Connect to the server and send the data
                  sck4.sendall(f_list.encode("utf-8"))
                  print (f_list)
      if cv2.waitKey(1) & 0XFF==ord('a'):
              break
      #  if len(cd_list)!=0:
      #    print("face ",cd_list[4])
      #  if len(hnd_lst)!=0:
      #    print("hand ",hnd_lst[4])
      #  if len(bd_list)!=0:
      #   print("body ",bd_list[4])
      cv2.imshow('mc',img)

      if cv2.waitKey(1) & 0XFF==ord('a'):
          break
finally:
    sock.close() 
cv2.destroyAllWindows()
# SOCK_STREAM means TCP socket



# try:
#     # Connect to the server and send the data
#     sock.connect((host, port))
#     sock.sendall(data.encode("utf-8"))
#     response = sock.recv(1024).decode("utf-8")
#     print (response)

# finally:
#     sock.close() 
