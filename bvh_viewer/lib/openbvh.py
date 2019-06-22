import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os
import sys
from functools import reduce
names = []
class Channel(object):
    __slots__=['index', 'motion', 'matrix']
    def __init__(self, index=0):
        self.index=index
        self.motion=[]
        self.matrix=np.identity(4)

    def getValue(self, frame):
        assert(False)

    def getMatrix(self, frame):
        assert(False)

class ZeroChannel(Channel):
    __slots__=[]
    def getValue(self, frame):
        return 0

    def getMatrix(self):
        return np.identity(4)

class ChannelPositionX(Channel):
    __slots__=[]
    def __str__(self):
        return "px"

    def getValue(self, frame):
        return self.motion[frame]

    def getMatrix(self, frame):
        """
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, 0, 0, 1],
        """
        self.matrix[3, 0]=self.getValue(frame)
        return self.matrix

class ChannelPositionY(Channel):
    __slots__=[]
    def __str__(self):
        return "py"

    def getValue(self, frame):
        return self.motion[frame]

    def getMatrix(self, frame):
        """
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, z, 1],
        """
        self.matrix[3, 1]=self.getValue(frame)
        return self.matrix

class ChannelPositionZ(Channel):
    __slots__=[]
    def __str__(self):
        return "pz"

    def getValue(self, frame):
        return self.motion[frame]

    def getMatrix(self, frame):
        """
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, z, 1],
        """
        self.matrix[3, 2]=self.getValue(frame)
        return self.matrix

class ChannelRotationX(Channel):
    __slots__=[]
    def __str__(self):
        return "rx"

    def getValue(self, frame):
        return self.motion[frame]

    def getMatrix(self, frame):
        """
        [1, 0, 0, 0],
        [0, c, s, 0],
        [0,-s, c, 0],
        [0, 0, 0, 1],
        """
        radian=np.radians(self.getValue(frame))
        c=np.cos(radian)
        s=np.sin(radian)
        self.matrix[1, 1]=c
        self.matrix[1, 2]=s
        self.matrix[2, 1]=-s
        self.matrix[2, 2]=c
        return self.matrix

class ChannelRotationY(Channel):
    __slots__=[]
    def __str__(self):
        return "ry"

    def getValue(self, frame):
        return self.motion[frame]

    def getMatrix(self, frame):
        """
        [c, 0,-s, 0],
        [0, 1, 0, 0],
        [s, 0, c, 0],
        [0, 0, 0, 1],
        """
        radian=np.radians(self.getValue(frame))
        c=np.cos(radian)
        s=np.sin(radian)
        self.matrix[2, 2]=c
        self.matrix[2, 0]=s
        self.matrix[0, 2]=-s
        self.matrix[0, 0]=c
        return self.matrix

class ChannelRotationZ(Channel):
    __slots__=[]
    def __str__(self):
        return "rz"

    def getValue(self, frame):
        return self.motion[frame]

    def getMatrix(self, frame):
        """
        [ c, s, 0, 0],
        [-s, c, 0, 0],
        [ 0, 0, 1, 0],
        [ 0, 0, 0, 1],
        """
        radian=np.radians(self.getValue(frame))
        c=np.cos(radian)
        s=np.sin(radian)
        self.matrix[0, 0]=c
        self.matrix[0, 1]=s
        self.matrix[1, 0]=-s
        self.matrix[1, 1]=c
        return self.matrix

channel_map={
        'Xposition': ChannelPositionX,
        'Yposition': ChannelPositionY,
        'Zposition': ChannelPositionZ,
        'Xrotation': ChannelRotationX,
        'Yrotation': ChannelRotationY,
        'Zrotation': ChannelRotationZ,
        'XPOSITION': ChannelPositionX,
        'YPOSITION': ChannelPositionY,
        'ZPOSITION': ChannelPositionZ,
        'XROTATION': ChannelRotationX,
        'YROTATION': ChannelRotationY,
        'ZROTATION': ChannelRotationZ,
        }
def createChannel(key, index):
    if key in channel_map:
        return channel_map[key](index)

class Joint(object):
    __slots__=['name','parent','children','offset','tail','channels','channelMap']
    def __init__(self,name):
        self.name=name
        self.parent=None
        self.children=[]
        self.offset=None
        self.tail=None
        self.channels=[]
        self.channelMap={
            ChannelPositionX: ZeroChannel(),
            ChannelPositionY: ZeroChannel(),
            ChannelPositionZ: ZeroChannel(),
            ChannelRotationX: ZeroChannel(),
            ChannelRotationY: ZeroChannel(),
            ChannelRotationZ: ZeroChannel(),
            }
    def addChild(self, child):
        self.children.append(child)
        child.parent=self
        return child

    def addChannel(self, channel):
        self.channels.append(channel)
        self.channelMap[channel.__class__]=channel
    
    def show(self):
        global names
        names.append(self.name)
        # print(self.name, ' ')
        for child in self.children:
            child.show()
    def getOffsetMatrix(self):
        t=np.identity(4)
        t[3][0]=self.offset[0]
        t[3][1]=self.offset[1]
        t[3][2]=self.offset[2]
        return t
    def getMatrix(self, frame):
        m = reduce(lambda acum, ch: np.dot(ch.getMatrix(frame), acum),self.channels,np.identity(4))
        return m
class Loader(object):
    __slots__=[
            'root', 'channels',
            'frame_count', 'frame_interval',
            'joint_list',
            ]

    def __init__(self):
        self.joint_list=[]

    def load(self, path):
        io=open(path, "r")
        return self.process(io)

    def process(self, io):
        self.channels=[]
        if io.readline().strip() != "HIERARCHY":
            return print("This is not Hierarchy")
        # root
        name=io.readline().strip().split()
        self.root=Joint(name[1])
        self.joint_list.append(self.root)
        # joints
        self.parseJoint(io, self.root)
        # motion
        self.parseMotion(io)

    def parseJoint(self, io, joint):
        line=io.readline().strip()
        if line!="{":
            return print( "no {")

        # position
        offset, x, y, z=io.readline().strip().split()
        if offset!="OFFSET":
            return print("no OFFSET")
        joint.offset=[float(x), float(y), float(z)]

        # create channels
        tokens=io.readline().strip().split()
        if tokens.pop(0)!="CHANNELS":
            print("no CHANNELS")

        channelCount=int(tokens.pop(0))
        joint.channels=[]
        for channel in tokens:
            channel=createChannel(channel, len(self.channels))
            joint.addChannel(channel)
            self.channels.append(channel)
        assert(len(joint.channels)==channelCount)
        if joint.parent:
            # joint
            assert(channelCount==3)
        else:
            # root
            assert(channelCount==6)

        while True:
            line=io.readline()
            if line=="":
                return print("invalid eof")
            tokens=line.strip().split()
            if tokens[0]=="JOINT":
                child=joint.addChild(Joint(tokens[1]))
                self.joint_list.append(child)
                self.parseJoint(io, child)
            elif tokens[0]=="End":
                line=io.readline().strip()
                if line!="{":
                    print("no {")
                endoffset,x, y, z=io.readline().strip().split()
                joint.tail=[float(x), float(y), float(z)]
                if io.readline().strip()!="}":
                    print("no }")
            elif tokens[0]=="}":
                return
            else:
                print("unknown type")

    def parseMotion(self, io):
        line=io.readline().strip()
        if line!="MOTION":
            print("no MOTION")
        frame_count=io.readline().strip().split()
        tokens=io.readline().strip().split()
        if tokens[0]!="Frame":
            print("no Frame")
        if tokens[1]!="Time:":
            print("no Time:")
        self.frame_count=int(frame_count[1])
        self.frame_interval=float(tokens[2])
        print("Number of frames: ", self.frame_count)
        print("FPS: ", 1/self.frame_interval)
        print("joint number", len(self.joint_list))
        while True:
            line=io.readline()
            if line=="":
                break

            tokens=line.strip().split()
            assert(len(tokens)==len(self.channels))

            for i, t in enumerate(tokens):   
                self.channels[i].motion.append(float(t))

def load(path):
    l=Loader()
    l.load(path)
    l.root.show()
    print("joint list: ", names)
    return l