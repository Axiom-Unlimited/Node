import struct

# the first integer is the size in bytes of the message
# the second byte is the type of message
# any following bytes are the data associated with the type

#type is 1
captureCommand = 'iii255s'

#type is 0
# status messages
statusRequest = 'ii'

#type is 0
# sending messages
# the third integer can
statusReport = 'iii'