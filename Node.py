import struct
import socket
import Settings
import datetime as dt
import time
import threading


class Struct:
    pass


class UDPReceiver(threading.Thread):

    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callBack = callback

    def run(self):
        receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiverSocket.bind(('', Settings.broadcastPort))
        receiverSocket.settimeout(100)
        while True:
            # receive incoming commands
            try:
                data = receiverSocket.recv(8228)
                dataTuple = struct.unpack(BroadcastPackage, data)
                states = dataTuple[1]
                # to get index (260 * node offset)/260
                newStatus = struct.unpack(NodeState,
                                          states[(257 * Settings.nodePortId):(257 * Settings.nodePortId) + 257])
                self.callBack.update(newStatus)
            except BlockingIOError as e:
                print("no message received")
                pass


class Callback(object):
    def __init__(self):
        self.captureStatus = False
        self.captureName = ""

    def update(self, newStatus):
        self.captureName = newStatus[0].decode("utf-8").rstrip('\x00')
        self.captureStatus = newStatus[1]


# message structures
BroadcastPackage = '>i8224s'
NodeState = '>256s?'
NodeStatusPackage = '>i1000s?'

if __name__ == '__main__':

    camera = None
    isCapturing = False
    # # state variables
    callbackState = Callback()

    receiver = UDPReceiver(callbackState)
    receiver.start()
    # initialize the camera
    # camera = PiCamera()
    # camera.resolution = (settings.frameWidth, settings.frameHeight)
    # camera.framerate = (settings.frameRate)

    # initialize the udp sender
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    senderSocket.connect((Settings.ipAddress, Settings.basePort + Settings.nodePortId))  # base port + port offset

    while True:
        ts = time.time()

        # capture
        if callbackState.captureStatus:  # start capture
            if not isCapturing:
                if callbackState.captureName == "none":
                    st = dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
                    file = Settings.videoDataPath + "/" + "Node" + str(Settings.nodePortId) + " " + st + ".h264"
                    print(file)
                    # camera.start_recording(file)
                    isCapturing = True
                else:
                    file = str(Settings.videoDataPath) + "/" + "Node" + str(
                        Settings.nodePortId) + " " + callbackState.captureName + ".h264"
                    print(file)
                    isCapturing = True
                # camera.start_recording(file)
        else:  # stop capture
            isCapturing = False
            # camera.stop_recording()
        #     print()

        # send node state status
        message = struct.pack(NodeStatusPackage
                              , Settings.nodePortId
                              , bytes("no error", 'utf-8')
                              , callbackState.captureStatus)
        senderSocket.send(message)
