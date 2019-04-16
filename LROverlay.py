import os, json
from PIL import Image
import linedraw

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

def ditherImage(file):
    global trackData
    trackData={"label":"Generated with code written by OllieMBM","creator":"Ollie","description":"Powered by Python","duration":0,"version":"6.2","startPosition":{"x":-0,"y":0},"lines":[]}
    frame=Image.open(file).convert("1")
    toLines(frame)

def contourImage(file):
    sf = 0.5
    lines = linedraw.sketch(file)
    linecount = 0
    for group in lines:
        for (x0,y0,x1,y1) in linemaker(group):
            linecount += 1
            createLine(linecount,x0*sf,y0*sf,x1*sf,y1*sf)

def linemaker(group):
    is_first = True
    x0 = y0 = 0
    for (x,y) in group:
        if is_first:
            x0 = x
            y0 = y
            is_first = False
        else:
            yield x0,y0,x,y
            x0,y0 = x,y

def Main():
    global trackData
    mode = input('''SELECT MODE:
    1. DITHER (Fast, less detail)
    2. CONTOUR (Slow, more detail)
    3. DITHER + CONTOUR (Slowest, most detail)

''')
    file = input("ENTER FILE NAME: ")
    if mode == "1":
        ditherImage(file)
    elif mode == "2":
        contourImage(file)
    elif mode == "3":
        ditherImage(file)
        contourImage(file)
    else:
        print("Invalid Mode")

    filename = file.split(".")[0]
    saveTrack(filename)                       
               
Main()
