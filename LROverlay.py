import os, json
from PIL import Image

trackData={"label":"Generated with code written by OllieMBM","creator":"Ollie","description":"Powered by Python","duration":0,"version":"6.2","startPosition":{"x":-0,"y":0},"lines":[]}
linecount=0

def createLine(idno,x1,y1,x2,y2):
    x1=x1*2
    y1=y1*2
    x2=x2*2
    y2=y2*2
    newLine={"id":idno,"type":2,"x1":int(x1),"y1":int(y1),"x2":int(x2),"y2":int(y2)}
    trackData['lines'].append(newLine)

def saveTrack(filename):
    global trackData
    with open(str(filename)+".json", "w") as track:
        print("Writing to file...")
        json.dump(trackData, track)
        print("Saved to "+str(filename)+".json")

def toLines(frame):
    print("Converting image to lines...")
    global linecount
    linecount = 0
    sourceCanvas=frame.load()
    x1,y1,x2,y2=None,None,None,None
    ls,lf=False,False
    for y in range(frame.height):
        if lf==True:
            sourceCanvas[x,y-1]=0
            linecount+=1
            createLine(linecount,x1,y1,x2+0.1,y2)
        x1,y1,x2,y2=None,None,None,None
        ls,lf=False,False
        for x in range(frame.width):
            if sourceCanvas[x,y]>0:
                if lf==True:
                    sourceCanvas[x-1,y]=0
                    linecount+=1
                    createLine(linecount,x1,y1,x2+0.1,y2)
                x1,y1,x2,y2=None,None,None,None
                ls,lf=False,False
            if sourceCanvas[x,y]==0:
                if ls==True:
                    x2,y2=x,y
                    sourceCanvas[x,y]=1
                    lf=True
                if ls==False:
                    x1,y1,x2,y2=x,y,x,y
                    ls=True
    for x in range(frame.width):
            if lf==True:
                linecount+=1
                createLine(linecount,x1,y1,x2,y2+0.1)
            x1,y1,x2,y2=None,None,None,None
            ls,lf=False,False
            for y in range(frame.height):
                if sourceCanvas[x,y]<=1:
                    if ls==True:
                        x2,y2=x,y
                        lf=True
                    if ls==False:
                        x1,y1,x2,y2=x,y,x,y
                        ls=True
                if sourceCanvas[x,y]>1:
                    if lf==True:
                        linecount+=1
                        createLine(linecount,x1,y1,x2,y2+0.1)
                    x1,y1,x2,y2=None,None,None,None
                    ls,lf=False,False

    print("Generated "+str(linecount)+" lines...")

def convertImage(file):
    global trackData
    trackData={"label":"Generated with code written by OllieMBM","creator":"Ollie","description":"Powered by Python","duration":0,"version":"6.2","startPosition":{"x":-0,"y":0},"lines":[]}
    filename = file.split(".")[0]
    frame=Image.open(file).convert("1")
    toLines(frame)
    saveTrack(filename)

def Main():
    global trackData
    for file in os.listdir():
        if file.endswith(".jpg"):
            convertImage(file)
        if file.endswith(".png"):
            convertImage(file)
Main()
    
