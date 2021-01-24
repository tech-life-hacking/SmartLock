from face2name import FaceDetection
import socket

RaspberryPiIPAdress = '192.168.11.7'

facedetection = FaceDetection()

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((RaspberryPiIPAdress, 50002))
        while True:
            try:
                flag = facedetection.run()
                if flag:
                    s.sendall(b'Me')
                else:
                    s.sendall(b'No Detected')
            except:
                pass
