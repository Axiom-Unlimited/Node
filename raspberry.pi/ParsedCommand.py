import struct
import CommandStructs as cs


class ParsedCommand:
    type = None  # the type of command
    cmdFields = {}  # all of the data that came with the command

    def __init__(self, type, data):
        self.type = type

        if type is 1:  # command is a capture command
            dataTuple = struct.unpack(cs.captureCommand, data)
            self.cmdFields["size"] = dataTuple[0]
            self.cmdFields["type"] = dataTuple[1]
            self.cmdFields["command"] = dataTuple[2]
            self.cmdFields["filename"] = dataTuple[4]
        elif type is 0:  # command is status request
            dataTuple = struct.unpack(cs.statusRequest, data)
            self.cmdFields["size"] = dataTuple[0]
            self.cmdFields["type"] = dataTuple[1]

    def getField(self,fieldname):
        return self.cmdFields[fieldname]

    def getAllKeys(self):
        return self.cmdFields.keys()

    def isEmpty(self):
        return len(self.cmdFields) is 0