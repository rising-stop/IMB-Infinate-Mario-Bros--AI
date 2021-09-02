__author__ = "Sergey Karakovskiy, sergey at idsia fullstop ch"
__date__ = "$May 13, 2009 1:25:30 AM$"

from .client import Client
from .environment import Environment
from utils.dataadaptor import show


class TCPEnvironment(Environment):

    # Level settings
    _levelDifficulty = 1
    _levelType = 0
    _creaturesEnabled = True
    _initMarioMode = 0
    _levelSeed = 1
    _timeLimit = 100
    _fastTCP = False

    # Other settings
    _visualization = True
    _otherServerArgs = ""
    _numberOfFitnessValues = 5
    _numberOfObeservationValues = 6

    def __init__(self, agentname='UnnamedClient', host='localhost', port=4242, **otherargs):
        """General TCP Environment"""
        self._host = host
        self._port = port
        self._client = Client(host, port, agentname)
        self._connected = True

    def isAvailable(self):
        """returns the availability status of the environment"""
        return self._connected

    def to_unicode_or_bust(self, obj, encoding='utf-8'):
        if not isinstance(obj, str):
            obj = str(obj, 'utf-8')
        return obj

    def getObservation(self):
        """ receives an observation via tcp connection"""
        #        print "Looking forward to receive data"

        data = self._client.recvData()
        data = self.to_unicode_or_bust(data)

        if data == "ciao":
            self._client.disconnect()
            self._connected = False
        elif len(data) > 5:
            #        print data
            #            for i in range(31):
            #                cur_char = ord(data[i + 3])
            #                if (cur_char != 0):
            #                    print i + 3,
            #                    show(cur_char)
            return data

    def performAction(self, action):
        """takes a numpy array of ints and sends as a string to server"""
        actionStr = ""
        for i in range(5):
            if action[i] == 1:
                actionStr += '1'
            elif action[i] == 0:
                actionStr += '0'
            else:
                raise "something very dangerous happen...."
        actionStr += "\r\n"
        self._client.sendData(actionStr)

    def setDifficulty(self, difficulty):
        self._levelDifficulty = difficulty

    def reset(self):
        argstring = "-ld %d -lt %d -mm %d -ls %d -tl %d " % (self._levelDifficulty,
                                                             self._levelType,
                                                             self._initMarioMode,
                                                             self._levelSeed,
                                                             self._timeLimit
                                                             )
        argstring += "-zm 0 "
        if self._creaturesEnabled:
            argstring += "-pw off "
        else:
            argstring += "-pw on "
        if self._visualization:
            argstring += "-vis on "
        else:
            argstring += "-vis off "
        if self._fastTCP:
            argstring += "-fastTCP on"

        self._client.sendData("reset -maxFPS off " +
                              argstring + self._otherServerArgs + "\r\n")
