import os
import glob
import pandas as pd
import re
import string
from collections import OrderedDict
import io
import csv
from itertools import zip_longest
import matplotlib
from matplotlib import pyplot as plt
import cv2
import time


def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")
    

xml_list = []
filename=[]
width=[]
height=[]
class_var=[]
xmin=[]
ymin=[]
xmax=[]
ymax=[]
errors=0
bad_files=[]
realHeight=[]
realWidth=[]

path=os.getcwd()

testduplicates=0

testdupList=[]

trainduplicates=0

traindupList=[]

matchDupList=[]

biggestMargin=0

unmatchedDims=[]
unmatchedFile=[]
foundDimMatch=[]

for filepath in glob.iglob(path+"*/*.csv*", recursive=True):
    print(filepath)
    
    nonascii = bytearray(range(0x80, 0x100))
    with open(filepath,'r', newline='') as infile:
        reader =csv.DictReader(infile)
        next(reader, None)
##    raw=open(filepath,'r')
##    data=raw.read()
##    raw.close()
##    printable = set(string.printable)
##    re.sub(r'[^\x00-\x7F]+',' ', data)
##    data=''.join(filter(lambda x: x in printable, data))
    #print("NEW DATA=                "+data)
    
    #print(re.search('<imageName>(.+?)</imageName>',data).group(1))
    #filename.append(re.search('<imageName>(.+?)</imageName>',data).group(1).rsplit('\\.*?\\',1)[-1])
    #idx=re.search('<imageName>(.+?)</imageName>',data).rfind("\\")
        for row in reader:
            

        #FIND VALUE, APPEND LIST:
        
            f=row['filename']
            for fn in filename:
                if fn ==f:
                    if 'test' in filepath:
                        testduplicates+=1
                        testdupList.append(fn)
                    else:
                        if 'train' in filepath:
                            trainduplicates+=1
                            traindupList.append(fn)
                            
            filename.append(f)
            co=0
            #print(f)
            newpath=re.compile("{f}$")
            #newpath2=re.compile("/{f}$")
            #print(path+'/train')
            for root, dirs, files in os.walk(path+'/train/'):
                for file in files:
                    co+=1
                    #print(file)
                    if newpath.match(file) or file==f:
                        #print("yay")
                        im = cv2.imread(path+'/train/'+file)
##                        print("File "+file+" is type: " +str(type(im)))
                        rh, rw, _ = im.shape
                        realWidth.append(rw)
                        realHeight.append(rh)
                    else:
                        pass
                        
                        
                
            for root, dirs, files in os.walk(path+'/test/'):
                for file in files:
                    co+=1
                    #print(file)
                    if newpath.match(file) or file==f:
                        #print("yay")
                        im = cv2.imread(path+"/test/"+file)
##                        print("File "+file+" is type: " +str(type(im)))
                        rh, rw, _ = im.shape
                        realWidth.append(rw)
                        realHeight.append(rh)
                    else:
                        pass
                            
                #print(f)
        
            
##                filename.append('unknown')
##                print('unknown')
            try:
                w=row['width']
                width.append(w)
        ##            print(w)
            except:
                width.append('na')
            try:
                h=row['height']
                height.append(h)
        ##            print(h)
            except:
                height.append('na')
            try:
                xmin1=row['xmin']
                xmin.append(xmin1)
        ##            print(xmin1)
            except:
                xmin.append('na')

            try:   
                ymin1=row['ymin']
                ymin.append(ymin1)
        ##            print(ymin1)
            except:
                ymin.append('na')
            try:
                xmax1=row['xmax']
                
                xmax.append(xmax1)
            except:
                xmax.append('na')

            try:  
                ymax1=row['ymax']
                
                ymax.append(ymax1)
                #print(ymax2)
            except:
                ymax.append('na')
            class_var.append(row['class'])
            if 'na' not in (xmin[len(xmin)-1],xmax[len(xmax)-1],ymin[len(ymin)-1],ymax[len(ymax)-1]):
                    
                    if int(xmin[len(xmin)-1]) < int(xmax[len(xmax)-1]) and int(ymin[len(ymin)-1]) < int(ymax[len(ymax)-1]):
                            pass
                            #print("My man!")
                    else:
                            bad_files.append(str(filename[len(filename)-1]+"  " +xmin[len(xmin)-1]+"  " + xmax[len(xmax)-1] +'  '+ ymin[len(ymin)-1]+ '  ' + ymax[len(ymax)-1]))
                            errors+=1
                            print("MISMATCHED ANNOTATIONS1: "+ xmin[len(xmin)-1]+"  " + xmax[len(xmax)-1] +'  '+ ymin[len(ymin)-1]+ '  ' + ymax[len(ymax)-1])
                    if int(xmax[len(xmax)-1])<= int(width[len(width)-1]) and int(ymax[len(ymax)-1]) <= int(height[len(height)-1]):
                            pass
                            #print("So far, so good")
                    else:
                            bad_files.append(str(filename[len(filename)-1]+"  " +xmax[len(xmax)-1]+"  " + width[len(width)-1] +'  '+ ymax[len(ymax)-1]+ '  ' + height[len(height)-1]))
                            errors+=1
                            ymax[len(ymax)-1]=ymax1
                            print("MISMATCHED ANNOTATIONS2: "+ xmax[len(xmax)-1]+"  " + width[len(width)-1] +'  '+ ymax[len(ymax)-1]+ '  ' + height[len(height)-1])
                            
                            
            else:
                    bad_files.append(str(filename[len(filename)-1]+"  " +xmin[len(xmin)-1]+"  " + xmax[len(xmax)-1] +'  '+ ymin[len(ymin)-1]+ '  ' + ymax[len(ymax)-1]))
                    errors+=1
                    pass
            try:
                if int(width[len(width)-1])!=int(realWidth[len(realWidth)-1]):
    ##                print("Incorrect Width. W="+width[len(width)-1]+"real= "+str(realWidth[len(realWidth)-1]))
                    if abs(int(width[len(width)-1])-int(realWidth[len(realWidth)-1]))>biggestMargin:
                        biggestMargin=abs(int(width[len(width)-1])-int(realWidth[len(realWidth)-1]))
                    errors+=1
                    bad_files.append(str(filename[len(filename)-1]+" W="+str(width[len(width)-1])+"real= "+str(realWidth[len(realWidth)-1])))
                if int(height[len(height)-1])!=int(realHeight[len(realHeight)-1]):
    ##                print("Incorrect Height. H="+height[len(height)-1]+"real= "+str(realHeight[len(realHeight)-1]))
                    if abs(int(width[len(width)-1])-int(realWidth[len(realWidth)-1]))>biggestMargin:
                        biggestMargin=abs(int(height[len(height)-1])-int(realHeight[len(realHeight)-1]))
                    errors+=1
                    bad_files.append(str(filename[len(filename)-1]+ " H="+height[len(height)-1])+"real= "+str(realHeight[len(realHeight)-1]))
                imageArea=int(width[len(width)-1])*int(height[len(height)-1])
                boxWidth  = int(xmax[len(xmax)-1]) - int(xmin[len(xmin)-1])
                boxHeight = int(ymax[len(ymax)-1]) - int(ymin[len(ymin)-1])
                boxArea = boxWidth * boxHeight
                if (boxArea < 0.01 * imageArea):
                        try:
                                xmax[len(xmax)-1]=str(round((int(xmax[len(xmax)-1])/2)))
                                xmin[len(xmin)-1]=str(round((int(xmin[len(xmin)-1])/2)))
                                ymax[len(ymax)-1]=str(int(ymax[len(ymax)-1])+100)
                                ymin[len(ymin)-1]=str(int(ymin[len(ymin)-1])+100)
                        except:
                                errors+=1
                                print(str(filename[len(filename)-1])+ " Too Small object, boxArea= "+str(boxArea)+' imageArea= '+str(imageArea))
                imageArea=int(width[len(width)-1])*int(height[len(height)-1])
                boxWidth  = int(xmax[len(xmax)-1]) - int(xmin[len(xmin)-1])
                boxHeight = int(ymax[len(ymax)-1]) - int(ymin[len(ymin)-1])
                boxArea = boxWidth * boxHeight
                if (boxArea < 0.01 * imageArea):
                        try:
                                xmax[len(xmax)-1]=str(round((int(xmax[len(xmax)-1])-100)))
                                xmin[len(xmin)-1]=str(round((int(xmin[len(xmin)-1])-100)))
                                ymax[len(ymax)-1]=str(int(ymax[len(ymax)-1])+120)
                                ymin[len(ymin)-1]=str(int(ymin[len(ymin)-1])+120)
                        except:
                                errors+=1
                                print(str(filename[len(filename)-1])+ " Too Small object, boxArea= "+str(boxArea)+' imageArea= '+str(imageArea))
            except:
                print("Assess failed, try fix")
print("Lengths: Filename: " + str(len(filename))+" xmin: " + str(len(xmin)))
if errors>=1:
        print("Sorry boss, you had "+str(errors)+" errors.")
        print(bad_files)
        print('Biggest Margin: '+str(biggestMargin))
if testduplicates >=1 or trainduplicates >=1:
    for dd in testdupList:
        if dd in traindupList:
            matchDupList.append(dd)
            testdupList.remove(dd)
            traindupList.remove(dd)
            testduplicates-=1
            trainduplicates-=1
    print("NUM OF DUPLICATES: BOTH: "+str(len(matchDupList)))
    print(matchDupList)
    print("NUM OF DUPLICATES: TEST: "+str(testduplicates))
    print(testdupList)
    print("NUM OF DUPLICATES: TRAIN: "+str(trainduplicates))
    print(traindupList)
qu='Fix? Y/N'

time.sleep(int(4))
if yes_or_no(qu):
    a=0
    for filepath in glob.iglob(path+"**/*.csv*", recursive=True):
        a+=1
        with open(filepath,'r', newline='') as infile, open(str(a)+'.csv','w',newline='') as outfile:
            fieldnames = ['filename', 'width', 'height', 'class', 'xmin','ymin','xmax','ymax']
            writer = csv.DictWriter(outfile,fieldnames=fieldnames,skipinitialspace=False,delimiter=',', quoting=csv.QUOTE_NONE)
            reader =csv.DictReader(infile)
            writer.writeheader()
            #writer.writerow(('filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'))
            #next(reader, None)
            for row in reader:
                imageArea=int(row['width'])*int(row['height'])
                boxWidth  = int(row['xmax']) - int(row['xmin'])
                boxHeight = int(row['ymax']) - int(row['ymin'])
                boxArea = boxWidth * boxHeight
                if (boxArea < 0.01 * imageArea):
                        try:
                                row['xmax']=str(round((int(row['xmax'])+4)))
                                row['xmin']=str(round((int(row['xmin'])-4)))
                                row['ymax']=str(int(row['ymax'])+4)
                                row['ymin']=str(int(row['ymin'])-4)
                        except:
                                print(str(filename[len(filename)-1])+ " Too Small object, boxArea= "+str(boxArea)+' imageArea= '+str(imageArea))
                imageArea=int(row['width'])*int(row['height'])
                boxWidth  = int(row['xmax']) - int(row['xmin'])
                boxHeight = int(row['ymax']) - int(row['ymin'])
                boxArea = boxWidth * boxHeight
                if (boxArea < 0.01 * imageArea):
                        try:
                                row['xmax']=str(round((int(row['xmax'])+12)))
                                row['xmin']=str(round((int(row['xmin'])-12)))
                                row['ymax']=str(int(row['ymax'])+12)
                                row['ymin']=str(int(row['ymin'])-12)
                        except:
                                print(str(filename[len(filename)-1])+ " Too Small object, boxArea= "+str(boxArea)+' imageArea= '+str(imageArea))


                if int(row['xmin']) > int(row['xmax']):
                    row['xmax']=str(int(row['xmax'])+100)
                    print("BoxBounds Increased")
                if int(row['ymin']) > int(row['ymax']):
                    row['ymax']=str(int(row['ymax'])+100)
                    print("BoxBounds Increased")
                if int(row['xmax'])>= int(row['width']):
                    row['xmax']=str(int(row['width'])-1)
                    print("Clamped BoxBounds")
                if int(row['ymax']) >= int(row['height']):
                    row['ymax']=str(int(row['height'])-1)
                    print("Clamped BoxBounds")
                row['xmax']=str(abs(int(row['xmax'])))
                row['xmin']=str(abs(int(row['xmin'])))
                row['ymax']=str(abs(int(row['ymax'])))
                row['ymin']=str(abs(int(row['ymin'])))
                found=False
                click=0
                matchedDims=0
                ff=row['filename']
                #print('ff= '+ff)
                if ff not in testdupList and ff not in traindupList and ff not in matchDupList:
                    strike=0
                    for root, dirs, files in os.walk(path+'/train/'):
                        for file in files:
                            newpath=re.compile("{ff}$")
                            if newpath.match(file) or file==ff:
                                found=True
                                im = cv2.imread(path+'/train/'+file)
                                rh, rw, _ = im.shape
                                if str(rw)==row['width']:
                                    matchedDims+=1
                                    #print("Positive")
                                else:
                                    matchedDims+=1
                                    row['height']=str(rh)
                                    row['width']=str(rw)
                                    print('Fixed')
                            else:
                                strike+=1
                                    
                    
                    for root, dirs, files in os.walk(path+'/test/'):
                        for file in files:
                            co+=1
                            newpath=re.compile("{ff}$")
                            #print(file)
                            
                            if newpath.match(file) or file==ff:
                                found=True
                                #print("yay")
                                im = cv2.imread(path+"/test/"+file)
        ##                      print("File "+file+" is type: " +str(type(im)))
                                rh, rw, _ = im.shape
                                if str(rw)==row['width']:
                                    matchedDims+=1
                                    #print("Positive")
                                    #writer.writerow(row)
                                else:
                                    matchedDims+=1
                                    row['height']=str(rh)
                                    row['width']=str(rw)
                                    print('Fixed')
                            else:
                                strike+=2
                if ff in testdupList:
                    testdupList.remove(row['filename'])
                    testduplicates-=1
                    for root, dirs, files in os.walk(path+'/train/'):
                        for file in files:
                            #print('file= '+file)
                            co+=1
                            newpath=re.compile("{ff}$")
                            #print(file)
                            if newpath.match(file) or file==ff:
                                found=True
                                #print("yay")
                                im = cv2.imread(path+'/train/'+file)
##                              print("File "+file+" is type: " +str(type(im)))
                                rh, rw, _ = im.shape
                                if str(rh)==row['height']:
                                    matchedDims+=1
                                    print("good, would write")
                                    #writer.writerow(row)
                                    
                    
                    for root, dirs, files in os.walk(path+'/test/'):
                        for file in files:
                            co+=1
                            newpath=re.compile("{ff}$")
                            #print(file)
                            
                            if newpath.match(file) or file==ff:
                                found=True
                                #print("yay")
                                im = cv2.imread(path+"/test/"+file)
        ##                      print("File "+file+" is type: " +str(type(im)))
                                rh, rw, _ = im.shape
                                if str(rh)==row['height']:
                                    matchedDims+=1
                                    print("good, would write")
                                    #writer.writerow(row)
                                    
                else:
                    click+=1
                if row['filename'] in traindupList:
                    traindupList.remove(row['filename'])
                    trainduplicates-=1
                    for root, dirs, files in os.walk(path+'/train/'):
                        for file in files:
                            
                            co+=1
                            newpath=re.compile("{ff}$")
                            #print(file)
                            if newpath.match(file) or file==ff:
                                found=True
                                #print("yay")
                                im = cv2.imread(path+'/train/'+file)
##                                      print("File "+file+" is type: " +str(type(im)))
                                rh, rw, _ = im.shape
                                if str(rh)==row['height']:
                                    matchedDims+=1
                                    print("good, would write")
                                    #writer.writerow(row)
                                    
                    for root, dirs, files in os.walk(path+'/test/'):
                        for file in files:
                            
                            co+=1
                            newpath=re.compile("{ff}$")
                            #print(file)
                            if newpath.match(file) or file==ff:
                                found=True
                                #print("yay")
                                im = cv2.imread(path+"/test/"+file)
        ##                        print("File "+file+" is type: " +str(type(im)))
                                rh, rw, _ = im.shape
                                if str(rh)==row['height']:
                                    matchedDims+=1
                                    print("good, would write")
                                    #writer.writerow(row)
                                    
                else:
                    click+=1
                #print(click)
                if click>=2 or matchedDims>0:
                    #print(zip_longest(*row, fillvalue = ''))
##                    for r in row
                    final=[row['filename'],row['width'],row['height'],row['class'],row['xmin'],row['ymin'],row['xmax'],row['ymax']]
                    #export_data = zip(*final, fillvalue = '')
                    #print(final)
                    if found==True:
                        writer.writerow(row)
                if matchedDims>0 and click<2:
                    print('How????')
                if matchedDims<1 and click<2:
                    if ff not in unmatchedDims:
                        unmatchedDims.append(ff)
                        for root, dirs, files in os.walk(path+'/train/'):
                            for file in files:
                                newpath=re.compile("{ff}$")
                                if newpath.match(file) or file==ff:
                                    os.remove(path+'/train/'+file)
                                        
                        
                        for root, dirs, files in os.walk(path+'/test/'):
                            for file in files:
                                co+=1
                                newpath=re.compile("{ff}$")
                                #print(file)
                                
                                if newpath.match(file) or file==ff:
                                    os.remove(path+'/test/'+file)
                if found!=True and click<2:
                    if row['filename'] not in unmatchedFile:
                        unmatchedFile.append(row['filename'])
                        
                 
                if row['filename'] in matchDupList:
                    matchDupList.remove(row['filename'])


print("Deleted "+str(len(unmatchedDims))+"Files with Unmatched Dimensions: ")
print(unmatchedDims)
if len(unmatchedFile)>=1:
    print("Unmatched Files: ")
    print(unmatchedFile)
for root, dirs, files in os.walk(path+'/train/'):
    for file in files:
        safe=False
        for filepath in glob.iglob(path+"**/train_labels.csv*", recursive=True): 
            with open(filepath,'r', newline='') as infile:
                reader =csv.DictReader(infile)
                for row in reader:
                    ff=row['filename']
                    newpath=re.compile("{ff}$")
                    if newpath.match(file) or file==ff:
                        safe=True
        if safe!=True:
            os.remove(path+'/train/'+file)
            print("Deleted file without labels")
                
                    
for root, dirs, files in os.walk(path+'/test/'):
    for file in files:
        safe=False
        for filepath in glob.iglob(path+"**/test_labels.csv*", recursive=True): 
            with open(filepath,'r', newline='') as infile:
                reader =csv.DictReader(infile)
                for row in reader:
                    ff=row['filename']
                    newpath=re.compile("{ff}$")
                    if newpath.match(file) or file==ff:
                        safe=True
        if safe!=True:
            os.remove(path+'/test/'+file)
            print("Deleted file without labels")

