from CameraCapturing import CameraCapturing
import time

def main():
    camera = CameraCapturing(2, [['know/Mishana.jpg', "Mishana"]])

    camera.start()
    print("im here")
    time.sleep(50)

    print("THIS SHIT WAS ENDED")
    print(camera.stop_capturing())
    
if __name__ == "__main__":
    main()
