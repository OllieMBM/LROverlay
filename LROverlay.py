import os, cv2, json, numpy
from PIL import Image, ImageDraw
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
    frame.show()

def contourImage(file):
    sf = 0.5
    lines = linedraw.sketch(file)
    linecount = 0
    for group in lines:
        for (x0,y0,x1,y1) in linemaker(group):
            linecount += 1
            createLine(linecount,x0*sf,y0*sf,x1*sf,y1*sf)

def animate(video):
    res = (240,135)
    #res = (120,67)
    frames = []
    cap = cv2.VideoCapture(video)
    
    check, image = cap.read()
    im = Image.fromarray(image)
    name = video.split(".")[0]+"CONVERTED.mp4"
    new = cv2.VideoWriter(name, 0, 30, (1920,1080))
    
    while check:
        image = cv2.resize(image, res)
        frame = Image.fromarray(image)
        frame = frame.convert("1")
        frames.append(frame)
        check, image = cap.read()

    length = len(frames)
    print(str(length) + " frames captured")
    count = 0
    for frame in frames:
        count += 1
        print("Processing frame "+str(count)+".")
        
        newframe = Image.new("RGB",(1920,1080), (255,255,255))
        draw = ImageDraw.Draw(newframe)
        sourceCanvas = frame.load()
        x1,y1,x2,y2=None,None,None,None
        ls,lf=False,False
        for y in range(frame.height):
            if lf==True:
                sourceCanvas[x,y-1]=0
                draw.ellipse([x1*8,y1*8,x1*8+8,y1*8+8],fill="black")
                draw.rectangle((((x1*8)+4,(y1*8)),((x2*8)+4,(y2*8)+8)), fill="black")
                draw.ellipse([x2*8,y2*8,x2*8+8,y2*8+8],fill="black")
            x1,y1,x2,y2=None,None,None,None
            ls,lf=False,False
            for x in range(frame.width):
                if sourceCanvas[x,y]>0:
                    if lf==True:
                        sourceCanvas[x-1,y]=0
                        draw.ellipse([x1*8,y1*8,x1*8+8,y1*8+8],fill="black")
                        draw.rectangle((((x1*8)+4,(y1*8)),((x2*8)+4,(y2*8)+8)), fill="black")
                        draw.ellipse([x2*8,y2*8,x2*8+8,y2*8+8],fill="black")
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
                draw.ellipse([x1*8,y1*8,x1*8+8,y1*8+8],fill="black")
                draw.rectangle((((x1*8),(y1*8)+4),((x2*8)+8,(y2*8)+4)), fill="black")
                draw.ellipse([x2*8,y2*8,x2*8+8,y2*8+8],fill="black")

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
                        draw.ellipse([x1*8,y1*8,x1*8+8,y1*8+8],fill="black")
                        draw.rectangle((((x1*8),(y1*8)+4),((x2*8)+8,(y2*8)+4)), fill="black")
                        draw.ellipse([x2*8,y2*8,x2*8+8,y2*8+8],fill="black")
                    x1,y1,x2,y2=None,None,None,None
                    ls,lf=False,False
                    
        newframe = numpy.array(newframe)
        new.write(newframe)
    
    cv2.destroyAllWindows()
    new.release()
    print("Video saved to " +name)

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

    print('''LROverlay V0.3
    Some features are highly experimental and may not function correctly.
    If you have any issues getting any of the modes to work, please feel
    free to contact me via Discord (@Ollie#1153)
    
''')
    
    mode = input('''SELECT MODE:
    1. DITHER (Fastest, less detail)
    2. CONTOUR (Fast, more detail)
    3. DITHER + CONTOUR (Slow, most detail)
    4. DITHER + ANIMATE (Slowest, outputs .mp4)

''')
    file = input("ENTER FILE NAME: ")
    if mode == "1":
        ditherImage(file)
        filename = file.split(".")[0]
        saveTrack(filename)  
    elif mode == "2":
        contourImage(file)
        filename = file.split(".")[0]
        saveTrack(filename)  
    elif mode == "3":
        ditherImage(file)
        contourImage(file)
        filename = file.split(".")[0]
        saveTrack(filename)  
    elif mode == "4":
        if file.endswith(".mp4") or file.endswith(".gif"):
            animate(file)
    else:
        print("Invalid Mode")                     
               
Main()
