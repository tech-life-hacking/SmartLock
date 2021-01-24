from face2name import FaceDetection

RaspberryPiIPAdress = '192.168.11.7'

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((RaspberryPiIPAdress, 50007))
        while True:
            try:
                flag = facedetection.run(True)
                if flag:
                    s.sendall(b'Me')
                else:
                    s.sendall(b'No Detected')
            except:
                pass


