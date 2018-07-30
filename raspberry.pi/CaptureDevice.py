from picamera.array import PiRGBArray
from picamera import PiCamera
import Settings as settings

def writeVideoToFile(filename, camera):
    filePath = settings.videoDataPath + filename
    camera.wait_recording(1)
    camera.start_recording(filePath)


def stopWriteVideoToFile(filename, camera):
    camera.stop_recording()

if __name__ == '__main__':
    print()
