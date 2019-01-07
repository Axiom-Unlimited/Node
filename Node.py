import struct
import socket
import Settings
import datetime as dt
import time


class Struct:
    pass


# message structures
BroadcastPackage = '>i8224s'
NodeState = '>256s?'
NodeStatusPackage = '>i1000s?'


if __name__ == '__main__':

    camera = None

    # state variables
    captureStatus = False
    captureName = ""

    # initialize the camera
    # camera = PiCamera()
    # camera.resolution = (settings.frameWidth, settings.frameHeight)
    # camera.framerate = (settings.frameRate)

    # initialize the udp receiver
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiverSocket.bind(('', Settings.broadcastPort))
    receiverSocket.settimeout(10)
    # receiverSocket.setblocking(False)

    # initialize the udp sender
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    senderSocket.connect((Settings.ipAddress, Settings.basePort + Settings.nodePortId))  # base port + port offset

    while True:
        ts = time.time()

        # receive incoming commands
        try:
            data = receiverSocket.recv(8228)
            dataTuple = struct.unpack(BroadcastPackage, data)
            states = dataTuple[1]
            # to get index (260 * node offset)/260
            newStatus = struct.unpack(NodeState, states[(257 * Settings.nodePortId):(257 * Settings.nodePortId)+257])
            cap = str(newStatus[0])
            if cap.strip("0") != captureName:
                captureName = newStatus

            if newStatus[1] != captureStatus:
                captureStatus = newStatus[1]
        except BlockingIOError as e:
            pass
            # print("no message received")

        # capture
        if captureStatus:  # start capture
            if captureName == "":
                st = dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
                file = Settings.videoDataPath + "/" + "Node" + str(Settings.nodePortId) + " " + st + ".h264"
                print(file)
                # camera.start_recording(file)
            else:
                file = str(Settings.videoDataPath) + "/" + "Node" + str(Settings.nodePortId) + captureName + ".h264"
                print(file)
                # camera.start_recording(file)
        else:  # stop capture
            # camera.stop_recording()
            print()

        # send node state status
        message = struct.pack(NodeStatusPackage, Settings.nodePortId, bytes("no error", 'utf-8'), captureStatus)
        senderSocket.send(message)
