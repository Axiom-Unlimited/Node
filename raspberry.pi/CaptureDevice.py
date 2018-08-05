from picamera.array import PiRGBArray
from picamera import PiCamera
import Settings as settings
import NodeSocket as sock
import struct
import CommandStructs as cs
import sys
import time
import datetime

camera = None
socket = None
status = 0

if __name__ == '__main__':
    print("===========================================================================================================")
    print("Node: " + str(settings.nodePortId) + " started!")
    print("===========================================================================================================")
    camera = PiCamera()
    socket = sock.NodeSocket()
    ts = time.time()

    nodePort = settings.basePort + settings.nodePortId
    print("Attempting to Connect to socket at port:" + str(nodePort) + " ...")
    socket.connect(settings.ipAddress, nodePort)
    camera.resolution(settings.frameWidth, settings.frameHeight)
    camera.framerate(settings.frameRate)

    print("Camera and Port initialized!")

    while True:
        cmdMessage = socket.receive()
        if not cmdMessage.isEmpty():
            cmdType = cmdMessage.type
            if cmdType is 1:  # the incoming command is capture command
                cmd = cmdMessage.getField("command")
                if cmd is 1: # record to the file specified
                    if cmdMessage.getField("filename") is "":
                        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
                        file = settings.videoDataPath + "/" + st + ".h264"
                        camera.start_recording(file)
                    else:
                        file = settings.videoDataPath + "/" + cmdMessage.getField("filename")
                        camera.start_recording(file)
                elif cmd is 0:  # stop recording
                    camera.stop_recording()
            elif cmdType is 0:  # the incoming command is a status request
                report = [int(0), int(0), int(status)]
                reportSize = sys.getsizeof(report)
                report[0] = reportSize
                data = struct.pack(cs.statusReport, report)
                socket.send(data)
