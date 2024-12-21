import maya.cmds as cmds
import maya.mel as mel

def createModels(count,size,moving):
    movetorus=1.25
    scaling=(1,1,1)
    for x in range(count):
        t=count-x   
        cmds.torus(n="disk1",r=size+(x*(size/5)),hr=0.5, po=1)
        cmds.rotate(0,0,90)
        cmds.move(0,movetorus,0)
        movetorus-=size*1.15
    for x in range(3):
        cmds.polyCylinder(n="tube1",r=0.25,h=count+2.5)
        cmds.move(moving*x,2,0)    
    
    cmds.polyCube(n="tubebase",w=15,h=0.75,d=5)
    cmds.move(4.5,movetorus,0)
    
def hanoiTower(n, source, destination, auxiliary, steps):
    if n==1:
        steps.append({"disk":n, "from":source,"to":destination})
        return steps        
    hanoiTower(n-1, source, auxiliary, destination,steps)
    steps.append({"disk":n, "from":source,"to":destination})
    hanoiTower(n-1, auxiliary, destination, source,steps)
         

def animateTorus(n,height):
    cmds.playbackOptions(min=0,max=(len(steps)*n)+20)
    actualframe=0
    for x in range(len(steps)):
        makekey= steps[x]
        animdisk= 'disk%d' % makekey["disk"]       
        Xdistance= (makekey["to"]-makekey["from"])*moving/2
        
        cmds.setKeyframe(animdisk,t=actualframe) 
        actualframe+=n/2        
        cmds.move(0,height+2.5,0,animdisk,relative=True)
        cmds.setKeyframe(animdisk,t=actualframe)
        actualframe+=n/2
        
        cmds.move(Xdistance,0,0,animdisk,relative=True)
        cmds.setKeyframe(animdisk,t=actualframe)
        actualframe+=n/2
        
        cmds.move(Xdistance,0,0,animdisk,relative=True)
        cmds.setKeyframe(animdisk,t=actualframe)
        actualframe+=n/2 
        cmds.move(0,-(height+2.5),0,animdisk,relative=True)
        cmds.setKeyframe(animdisk,t=actualframe)
        
#MAIN
number, size, moving = 5,0.6,5
frames=6
steps=[]

#CALL FUNCTIONS
createModels(number,size,moving)
hanoiTower(number,1,3,2,steps)
animateTorus(frames,number)
cmds.select(all=True)
cmds.keyTangent(time=(0, 340), inTangentType="step", outTangentType="step")
mel.eval("doUpdateTangentFeedback")