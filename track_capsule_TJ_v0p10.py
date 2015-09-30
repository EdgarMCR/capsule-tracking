# -*- coding: utf-8 -*-
"""
Program to creat a list of photos in a folder, threshold them and measure 
various quanitities such as the area, perimeter and extension in the y ans x 
direction. 

To start, look at the bottom of the file in the 'if __name__ == '__main__':'
Statment

Created on Wed Sep 18 12:44:18 2013

@author: Edgar Haener
edgar.haner@gmail.com

"""
from __future__ import absolute_import, division, print_function
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import platform
import sys
#memory related imports
import gc

import shutil

#------------------------------------------------------------------------------
#CONSTANTS
#------------------------------------------------------------------------------
maxArea=1.15   #for judging contour quality
minArea=0.4
minAreaCH=0.7
maxCurvatureCutOff = 0.8

def wholeRun(directory, d0,  pPmm, rotateImages=0.0, threshold=150):
    """ Run the script for finding measurments on several folders"""
    import traceback
    listFolders=os.listdir(directory)
    indexDelet=[]
    for i in range(len(listFolders)):
        if os.path.isfile(directory+listFolders[i]):
            indexDelet.append(i)

    for i in range(len(indexDelet)-1, -1, -1):
        del listFolders[indexDelet[i]]
    
#    for i in range(len(listFolders)):
#        print(listFolders[i])
#    
#    
#    for i in range(len(listFolders)-1, 2, -1):
#        del listFolders[i]
#    
#    results =[[0 for x in xrange(4)] for x in xrange(len(listFolders))] 

    
#    counter=0
    for f in listFolders:
        try:
            print('\n Starting \t %s \n' %f)
            if platform.system() == 'Linux':
                find_max_extend(directory+f+'/', d0=d0, pPmm=pPmm, constantFrequency=True, rotate=rotateImages, plot=False, threshold=threshold, printDebugInfo=False)
            elif platform.system() == 'Windows': 
                find_max_extend(directory+f+'\\', d0=d0,  pPmm=pPmm, constantFrequency=True, rotate=rotateImages, plot=False, threshold=threshold, printDebugInfo=False)
            
#            find_max_extend(directory+f)
        except Exception, err:
            print('Didnt work for \t %s' %f)
            print(traceback.format_exc())
            
            
                
#        results[counter][0]=f
#        results[counter][1]=r[0]
#        results[counter][2]=r[1]
#        results[counter][3]=r[2]
#        counter=counter+1
#    
#    #Write results to file    
#    fo = open(directory+'Results.txt', "w")
#    #fo = open('/home/magda/Dropbox/PhD/CapsM:\EdgarHaener\Capsules\Batch190315-002\Experiments_200315\Batch190315-002-#1_10mlPmin-1ules/Batch141113-003/Flow/#3/141103-003_#3_1mlPs_25mlS_1r/Proccesed/Coordinates.txt', "w")
#    for i in range(len(results)) :
#        print(i)
#        fo.write("%s \t %.4f \t %.4f \t %.4f \n" %(results[i][0], results[i][1], results[i][2], results[i][3]))
#        
#    fo.close()
#    
#    for i in range(len(results)) :
#        print(i)
#        print("%s \t %.4f \t %.4f \t %.4f \n" %(results[i][0], results[i][1], results[i][2], results[i][3]))

def runOneFPS(directory, d0,  pPmm, FPS, rotateImages=0.0, threshold=150):
    """ Run the script for finding measurments on several folders"""
    import traceback
    listFolders=os.listdir(directory)
    indexDelet=[]
    for i in range(len(listFolders)):
        if os.path.isfile(directory+listFolders[i]):
            indexDelet.append(i)

    for i in range(len(indexDelet)-1, -1, -1):
        del listFolders[indexDelet[i]]

    for f in listFolders:
        sp1=f.find('FPS')
        sp2=f[:sp1].rfind('_')
        if sp2 == -1:
            sp2=f[:sp1].rfind('-')
#            print('entriesLine[0][sp2+1:sp1] = %s ' %entriesLine[0][sp2+1:sp1])
        
        try:
            FPSString=int(f[sp2+1:sp1])  
        
            if FPSString != FPS:
                continue
            
            print('\n Starting \t %s \n' %f)
            if platform.system() == 'Linux':
                find_max_extend(directory+f+'/', d0=d0, pPmm=pPmm, constantFrequency=True, rotate=rotateImages, plot=False, threshold=threshold, printDebugInfo=False)
            elif platform.system() == 'Windows': 
                find_max_extend(directory+f+'\\', d0=d0,  pPmm=pPmm, constantFrequency=True, rotate=rotateImages, plot=False, threshold=threshold, printDebugInfo=False)
            
#            find_max_extend(directory+f)
        except Exception, err:
            print('Didnt work for \t %s' %f)
            print(traceback.format_exc())

    
    
    
def addZeros(path):
    fileList=dir_list2(path)
    os.chdir(path)
    print(os.getcwd())
    underscore='_'
    jpg='.jpg'
    slash='\\'
    for i in fileList:
        a=i.find(underscore, -9, len(i))
        b=i.find(jpg, -9, len(i))
        c=i.find(slash, -45, len(i))
        if (b-a) == 3:
            filename=i[c+1:a+1]+'0'+i[a+1:len(i)]
            os.rename(i[c+1: len(i)], filename)
        elif (b-a) == 2:
            filename=i[c+1:a+1]+'00'+i[a+1:len(i)]
            os.rename(i[c+1: len(i)], filename)            
        else:
            filename=i[c+1:len(i)]
                
            
        print('%d \t %d \t %d %s' %(a, b, c, filename))
    fileList=dir_list2(path)
    fileList.sort()
    for i in fileList:
        print(i)
        
def renameRefolder(path):
    year='2015' #'2015' for data this year
    underscore='_'
    jpg='.jpg'
    TJ= 'T-J'
    dash='-'

    dirs = os.listdir(path)
    i=0
    for fname in dirs:
        if (fname[-4:len(fname)] == '.jpg'):
            i+=1
            print ('Filename',i,' is: ',fname)

            ndname = 'CopiedPhotos\\' #windows
#            ndname = 'CopiedPhotos/' #mac

            if not os.path.exists(path+ndname):
                os.makedirs(path+ndname)
            shutil.copy2(path+fname,path+ndname+fname)    

            a=fname.find(underscore,-8,len(fname))   
            b=fname.find(underscore,a-5,len(fname))
            c=fname.find(year,-45,len(fname))
            d=fname.find(jpg,-5,len(fname))

            #j=fname.find(TJ,-45,len(fname)) #for pictures with no milliseconds
            cfname = fname[c:b]+fname[d:len(fname)] #+fname[j+3:len(fname)] for no milliseconds

            e=cfname.find(dash,0,len(cfname))
            f=e+1+cfname[e+1:len(cfname)].find(dash,0,len(cfname))
            g=f+1+cfname[f+1:len(cfname)].find(dash,0,len(cfname))
            h=cfname.find(jpg,-5,len(cfname))

            print (e,', ',f,', ',g,', ',h)
            print (f-(e+1))
            print (g-(f+1))
            print (h-(g+1))
            print (cfname[:10])

            #Milliseconds (comment out if none)

            if (h-(g+1))==2:
                cfname = cfname[:g+1]+'0'+cfname[g+1:len(cfname)]
            elif (h-(g+1))==1:
                cfname = cfname[:g+1]+'00'+cfname[g+1:len(cfname)]
            elif (h-(g+1))==0:
                cfname = cfname[:g+1]+'000'+cfname[g+1:len(cfname)]

            #Seconds
            if (g-(f+1))==1:
                cfname = cfname[:f+1]+'0'+cfname[f+1:len(cfname)]
            elif (g-(f+1))==0:
                cfname = cfname[:f+1]+'00'+cfname[f+1:len(cfname)]

            #Minutes
            if (f-(e+1))==1:
                cfname = cfname[:e+1]+'0'+cfname[e+1:len(cfname)]
            elif (f-(e+1))==0:
                cfname = cfname[:e+1]+'00'+cfname[e+1:len(cfname)]

            os.rename(path + ndname + fname,path + ndname + cfname)

            print ('New directory',i,' is: ',ndname)

    for cfname in dirs:
        print (cfname)
        
def sortPhotos(path, prefixleng=10):
    """
    Takes the path to a directory and creates n x 2 matrix of all the jpg in 
    that directory, where the first entry is the filename and the second is the 
    millisecond time. 
    
    Typical filename :     23022015_24-2-2015-7-57-908_37.jpg
    """
    underscore='_'
    dash='-'

    dirs = os.listdir(path)
    j=0
    for fname in dirs:
        if (fname[-4:len(fname)] == '.jpg'):
            j+=1
    numberOfJPG=j
#    filenameList = [ filenameClass() for i in range(numberOfJPG)]
    filenameList=[]
            
    i=0
    for fname in dirs:
        if (fname[-4:len(fname)] == '.jpg'):
            i+=1            
#            print ('Filename',i,' is: ',fname)
            name=fname[prefixleng:-4] #adjust this depending how long the common prefix is
            
            #find first dash (day)
            d1=name.find(dash,0,3)
            name=name[d1+1:]
            
            #find second dash (month)
            d2=name.find(dash,0,3)
            name=name[d2+1:]
            
            #find third dash (year)
            d3=name.find(dash,0,5)
            name=name[d3+1:]

            #find last underscore from number
            u=name.find(underscore, -5,-1)
            number=int(float(name[u+1:]))
            name=name[0:u]
            

            #find hours
            d4=name.find(dash,0,3)
            minutesString=name[0:d4]
            minutes=int(abs(float(minutesString)))
#            print('name: ' + name + ' minutes = ' + str(minutes))
            name=name[d4+1:]
            
            #find seconds
            d5=name.find(dash,0,3)
            secondsString=name[0:d5]
            seconds=int(abs(float(secondsString)))
#            print(' seconds = ' + str(seconds))
            name=name[d4+1:]
            
            #find miliseconds
#            print('Name: ' + name)
            milliseconds=int(abs(float(name)))
            totalMillisecondTime=minutes*60.0*1000 + seconds*1000.0 + milliseconds
#            print('minutes= ' + str(minutes) + '\tseconds=' +str(seconds) + ' \t milliseconds  ' + str(milliseconds) + ' give total time = ' +str(totalMillisecondTime))
            
#            temp=filenameClass(fname, totalMillisecondTime, number)
            temp=filenameClass()
            temp.fn = fname
            temp.ms = totalMillisecondTime
            temp.number = number
            
            filenameList.append(temp)
    
    #sort by milliseconds
    newlist = sorted(filenameList, key=lambda filenameClass: filenameClass.number) 
    
    
#    for obj in newlist:
#        obj.printOut()
#        
    return newlist, numberOfJPG
    
def sortTiff(path, prefixleng=10):
    """
    Takes the path to a directory and creates n x 2 matrix of all the jpg in 
    that directory, where the first entry is the filename and the second is the 
    millisecond time. 
    
    Typical filename :     23022015_24-2-2015-7-57-908_37.jpg
    """
    underscore='_'
    dash='-'

    dirs = os.listdir(path)
    j=0
    for fname in dirs:
        if (fname[-5:len(fname)] == '.tiff'):
            j+=1
    numberOfJPG=j
#    filenameList = [ filenameClass() for i in range(numberOfJPG)]
    filenameList=[]
    
    i=-1
    for fname in dirs:
        if (fname[-5:len(fname)] == '.tiff'):
            i+=1            
            name=fname[:-5]

#            print('first number = ' + name[-3:] )

            
            temp=filenameClass()
            temp.fn = fname
            temp.number = int(float(name[-3:]))  
               
            filenameList.append(temp)
    
    #sort by milliseconds
    newlist = sorted(filenameList, key=lambda filenameClass: filenameClass.number) 
    
    
#    for obj in newlist:
#        obj.printOut()
#        
    return newlist, numberOfJPG


def sortPhotos2(path, prefixleng=10):
    """
    Takes the path to a directory and creates n x 2 matrix of all the jpg in 
    that directory, where the first entry is the filename and the second is the 
    millisecond time. 
    
    Typical filename :     23022015_24-2-2015-7-57-908_37.jpg
    """
    underscore='_'
    dash='-'

    dirs = os.listdir(path)
    j=0
    for fname in dirs:
        if (fname[-4:len(fname)] == '.bmp'):
            j+=1
    numberOfJPG=j
#    filenameList = [ filenameClass() for i in range(numberOfJPG)]
    filenameList=[]
    
    i=-1
    for fname in dirs:
        if (fname[-4:len(fname)] == '.bmp'):
            i+=1            
            name=fname[:-4]
            #find first dash (day)
            d1=name.find(dash,0,-1)
            print('first number = ' + name[0:d1] + '\t second number = ' + name[d1+1:])

            
            temp=filenameClass()
            temp.fn = fname
            temp.timestamp1 = int(float(name[0:d1]))  
            temp.timestamp2 = int(float(name[d1+1:]))
               
            filenameList.append(temp)
    
    #sort by milliseconds
    newlist = sorted(filenameList, key=lambda filenameClass: filenameClass.timestamp1) 
    
    
#    for obj in newlist:
#        obj.printOut()
#        
    return newlist, numberOfJPG
    
def sortPhotosPCO(path, prefixleng=10):
    """
    PCO camera
    
    Typical filename :     Capsule010315-002-#1-10mlPmin-2-0049
    """
    fileType='.png' #'.jpg'
    sperator='-' #'-'

    dirs = os.listdir(path)
    numberOfJPG=0

#    filenameList = [ filenameClass() for i in range(numberOfJPG)]
    filenameList=[]
    
    i=-1
    for fname in dirs:
        if (fname[-4:len(fname)] == fileType):
            d=fname.rfind('\\', 1, -1)
            if fname[d+1:d+3] == '._':
#                print(fname[d+1:d+3])
                continue
            i+=1            
            name=fname[:-4]
            #find first dash (day)
#            d1=name.find(dash,-6,-1)
            d1=name.find(sperator,-5,-1)
#            print('number = ' + name[d1+1:])

            temp=filenameClass()
            temp.fn = fname
            temp.number=abs(int(float(name[d1+1:])))
            temp.fps=-1
               
            filenameList.append(temp)
            numberOfJPG += 1
    
    #sort by milliseconds
    newlist = sorted(filenameList, key=lambda filenameClass: filenameClass.number) 
#    for obj in newlist:
#        obj.printOut()
    return newlist, numberOfJPG

    
class filenameClass:
    """Stores filename and millisecond time"""
    fn='-1'      #filename
    ms=-1        #millisecondtime   
    number=-1    #number in filename
    timestamp1=-1
    timestamp2=-1
    fps=-1
    
    def __repr__(self):
            return repr((self.fn, self.ms, self.number, self.timestamp1, self.timestamp2, self.fps))
            
#    def __init__(self, filename, millisecondTime, number):
#        self.fn = filename
#        self.ms = millisecondTime
#        self.number=number
        
    def printOut(self):
        print('Filename is \t %s and at \t %.d milliseconds and counter is %d.' %(self.fn, self.ms, self.number))

def get_immediate_subdirectories(directory):
    """ Retrieves the folders in a given path """
    return [x[0] for x in os.walk(directory)]

def dir_list2(dir_name, *args):
    """Returns a list of all files in a path, not looking into folders"""
    fileList = []
    for file in os.listdir(dir_name):
        dirfile = os.path.join(dir_name, file)
        if os.path.isfile(dirfile):
            if len(args) == 0:
                fileList.append(dirfile)
            else:
                if os.path.splitext(dirfile)[1][1:] in args:
                    fileList.append(dirfile)        #Check area
        '''
        elif os.path.isdir(dirfile):
            print "Accessing directory:", dirfile
            fileList += dir_list2(dirfile, *args)
        '''
    return fileList
    
def runningMean(x, N):  
    smoothed=np.zeros((len(x)), dtype=float)   
    smoothed[:-N+1]=np.convolve(x, np.ones((N,))/N, mode='valid')
    smoothed[-N:]=np.average(x)
    return smoothed
    
def find_batchName(path):
#    print('Started find_batchName(path)')
    if platform.system() == 'Linux':
        dSlash='/'
    elif platform.system() == 'Windows': 
        dSlash='\\'
    else:
        print('Unknow Oporating System - find_batchName(path) - failed')
        
    d1=path.rfind(dSlash,1,-3)
    reslt=path[d1+1:-1]
#    print('reslt1 = %s ' %reslt)
    
    d2=reslt.find(dSlash, 0, -1)
    if d2!=-1 :
        reslt="NameNotFound"

    
    return reslt
    
def gradient(x, h=1/64):
    dx = np.zeros((len(x)-4))
    for i in range(3,len(x)-2):
        dx[i-2] = (1/12*x[i-2]-2/3*x[i-1] + 2/3*x[i+1] - 1/12 * x[i+2])/h
    return dx
    
def rotateImage(image, angle):
    row,col = image.shape
    center=tuple(np.array([row,col])/2)
    rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
    new_image = cv2.warpAffine(image, rot_mat, (col,row))
    return new_image
    
def findContoursByThresholding(img, threshold, plot=False, counter=0, path=None, expectedArea=None, printDebugInfo=False):
    '''
    Take image, threshold it to a black and white image and find the longest
    contour. Fit a bounding box to this.
    Inputs:
    img         The image to be thresholded
    threshold   The threshold, between 0 and 255
    
    Outputs:
    cnt         the longest contour
    x           corner of bounding box
    y           corner of bounding box
    w           width of bounding box
    h           height of bounding box
    '''
#    print('Thresholding - Type img = ' +str(type(img)))
    
    #convert the image to B&W with the given threshold. 'thresh' is the 
    # the B&W image
    ret, thresh = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY) #192  
    th=thresh.copy()
    #find the contours in the image
    # Details under: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#findcontours
    #Good tutorial: http://opencvpython.blogspot.co.uk/2012/06/hi-this-article-is-tutorial-which-try.html
    contours, hierarchy = cv2.findContours(thresh, cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) #cv2.RETR_TREE


    cnt = None; x,y,w,h =-1, -1, -1, -1;
    notFoundMatchingContour=True
    counterWhile=-1
    
    while notFoundMatchingContour and counterWhile < len(contours):   
        counterWhile += 1
         #Select longest contour as this should be the capsule
        lengthC=0
        ID=-1
        idCounter=-1
        for xc in contours:
            idCounter=idCounter+1 
            if len(xc) > lengthC:
                lengthC=len(xc)
                ID=idCounter
        
        
        #if longest contour was found, then ID is the index of it
        if ID != -1:
            if len(contours[ID]) > 50:
                cnt = contours[ID] 
                if expectedArea != None:
                    M = cv2.moments(cnt)
                    if M['m00'] < 0.4*expectedArea or M['m00'] > 1.6*expectedArea:
                        
                        #find bounding rectangle of countour
                        x,y,w,h = cv2.boundingRect(cnt)
                        
                        #check that contour has reasonable aspect ratio, max is 6:1
                        if w >= h:
                            aspectRatio= w / h 
                        else:
                            aspectRatio= h/ w
                        
                        if aspectRatio < 7:
                            notFoundMatchingContour=False
                    else:
                        del contours[ID]
                        cnt=None
                else:
                    #find bounding rectangle of countour
                    x,y,w,h = cv2.boundingRect(cnt)
                    
                    #check that contour has reasonable aspect ratio, max is 6:1
                    if w >= h:
                        aspectRatio= w / h 
                    else:
                        aspectRatio= h/ w
                    
                    if aspectRatio < 7:
                        notFoundMatchingContour=False
                    
            else:
                del contours[ID]
                cnt=None

    if plot:
        imgForPlot=img.copy()
        cv2.rectangle(imgForPlot,(x,y),(x+w,y+h),(255,255,255),2)  
        if platform.system() == 'Linux':
            savepath=path+'Check/'
        elif platform.system() == 'Windows': 
            savepath=path+'Check\\'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+'ImageWContourFromThresholding_'+str(counter)+'.png'
        cv2.imwrite(filesavepath, imgForPlot)
        filesavepath=savepath+'Thres_'+str(counter)+'.png'
        cv2.imwrite(filesavepath, th)
        
        del imgForPlot

    
    return cnt, th, x,y,w,h
    
def findContoursByAdpativeThresholding(img,  plot=False, counter=0, path=None, expectedArea=None, printDebugInfo=False):
    '''
    Take image, threshold it to a black and white image and find the longest
    contour. Fit a bounding box to this.
    Inputs:
    img         The image to be thresholded
    threshold   The threshold, between 0 and 255
    
    Outputs:
    cnt         the longest contour
    x           corner of bounding box
    y           corner of bounding box
    w           width of bounding box
    h           height of bounding box
    '''
#    print('Thresholding - Type img = ' +str(type(img)))
    
    #convert the image to B&W with the given threshold. 'thresh' is the 
    # the B&W image
    blockSize=25
    c=5
    img = cv2.medianBlur(img,5)
    thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,blockSize,c)
    th=thresh.copy()
    #find the contours in the image
    # Details under: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#findcontours
    #Good tutorial: http://opencvpython.blogspot.co.uk/2012/06/hi-this-article-is-tutorial-which-try.html
    contours, hierarchy = cv2.findContours(thresh, cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) #cv2.RETR_TREE


    cnt = None; x,y,w,h =-1, -1, -1, -1;
    notFoundMatchingContour=True
    counterWhile=-1
    
    while notFoundMatchingContour and counterWhile < len(contours):   
        counterWhile += 1
         #Select longest contour as this should be the capsule
        lengthC=0
        ID=-1
        idCounter=-1
        for xc in contours:
            idCounter=idCounter+1 
            if len(xc) > lengthC:
                lengthC=len(xc)
                ID=idCounter
        
        
        #if longest contour was found, then ID is the index of it
        if ID != -1:
            if len(contours[ID]) > 50 and len(contours[ID]) < 250:
                cnt = contours[ID] 
                if expectedArea != None:
                    M = cv2.moments(cnt)
                    if M['m00'] > 0.2*expectedArea and M['m00'] < 1.8*expectedArea:
                        if printDebugInfo:
                            print('Adaptive Threshold: Area = %.f with length=%d' %(M['m00'], len(contours[ID])))
                        
                        #find bounding rectangle of countour
                        x,y,w,h = cv2.boundingRect(cnt)
                        
                        #check that contour has reasonable aspect ratio, max is 6:1
                        if w >= h:
                            aspectRatio= w / h 
                        else:
                            aspectRatio= h/ w
                        
                        if aspectRatio < 7:
                            notFoundMatchingContour=False
                    else:
                        del contours[ID]
                        cnt=None
                else:
                    #find bounding rectangle of countour
                    x,y,w,h = cv2.boundingRect(cnt)
                    
                    #check that contour has reasonable aspect ratio, max is 6:1
                    if w >= h:
                        aspectRatio= w / h 
                    else:
                        aspectRatio= h/ w
                    
                    if aspectRatio < 7:
                        notFoundMatchingContour=False
                    
            else:
                del contours[ID]
                cnt=None

    if plot:
        imgForPlot=img.copy()
        cv2.rectangle(imgForPlot,(x,y),(x+w,y+h),(255,255,255),2)  
        if platform.system() == 'Linux':
            savepath=path+'Check/'
        elif platform.system() == 'Windows': 
            savepath=path+'Check\\'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+'ImageWContourFromAdpativeThresholding_'+str(counter)+'.png'
        cv2.imwrite(filesavepath, imgForPlot)
        filesavepath=savepath+'Thres_'+str(counter)+'.png'
        cv2.imwrite(filesavepath, th)
        
        del imgForPlot

    
    return cnt, th, x,y,w,h
    
def print_polygon(polygon):
    print('Started print_polexpectedArea=-1,ygon')
    print('type = ' + str(type(polygon)))
    print('shape = ' + str(polygon.shape))
    counter=0
    for i in range(len(polygon)):
        print('%d %d %d' %(counter, polygon[i][0][0], polygon[i][0][1]))
        counter += 1

def area_for_polygon(polygon):
    result = 0
    imax = len(polygon)-1
    for i in range(0,imax):
        result += (polygon[i][0][0] * polygon[i+1][0][1]) - (polygon[i+1][0][0] * polygon[i][0][1])
    result += (polygon[imax][0][0] * polygon[0][0][1]) - (polygon[0][0][0] * polygon[imax][0][1])
    return result / 2.

def centroid_for_polygon(polygon):
    area = area_for_polygon(polygon)
    imax = len(polygon) -1

    result_x = 0
    result_y = 0
    for i in range(0,imax):
        result_x += (polygon[i][0][0] + polygon[i+1][0][0]) * ((polygon[i][0][0] * polygon[i+1][0][1]) - (polygon[i+1][0][0] * polygon[i][0][1]))
        result_y += (polygon[i][0][1] + polygon[i+1][0][1]) * ((polygon[i][0][0] * polygon[i+1][0][1]) - (polygon[i+1][0][0] * polygon[i][0][1]))
    result_x += (polygon[imax][0][0] + polygon[0][0][0]) * ((polygon[imax][0][0] * polygon[0][0][1]) - (polygon[0][0][0] * polygon[imax][0][1]))
    result_y += (polygon[imax][0][1] + polygon[0][0][1]) * ((polygon[imax][0][0] * polygon[0][0][1]) - (polygon[0][0][0] * polygon[imax][0][1]))
    result_x /= (area * 6.0)
    result_y /= (area * 6.0)

    return result_x, result_y #{'x': result_x, 'y': result_y}
    
def selectContour(contours):
    '''
    Select best contour
    
    Input:
    contours        List of Contours
    
    Output:
    cnt             Longest Contour
    x
    y
    w
    h
    '''
    cnt = None; x,y,w,h =-1, -1, -1, -1;
    notFoundMatchingContour=True
    counterWhile=0
    while notFoundMatchingContour and counterWhile < len(contours):   
         #Select longest contour as this should be the capsule
        lengthC=0
        ID=-1
        idCounter=-1
        for xc in contours:
            idCounter=idCounter+1 
            if len(xc) > lengthC:
                lengthC=len(xc)
                ID=idCounter
        
        
        #if longest contour was found, then ID is the index of it
        if ID != -1:
            if len(contours[ID]) > 50:
                cnt = contours[ID] 
                
                #find bounding rectangle of countour
                x,y,w,h = cv2.boundingRect(cnt)
                
                #check that contour has reasonable aspect ratio, max is 6:1
                if w >= h:
                    aspectRatio= w / h 
                else:
                    aspectRatio= h/ w
                
                if aspectRatio < 7:
                    notFoundMatchingContour=False
            else:
                del contours[ID]
                cnt=None
            
        else:
            print('No contour found')
            notFoundMatchingContour=False
            cnt = None
        counterWhile += 1
    
    return cnt, x, y, w, h
    
def findMaxCurvatureInContour(img, cnt, plot=False, path=None, ii=0, n=6):
    '''
    This function takes a contour and returns the maximum local curvature 
    found on it as a double. 
    
    Consider the angle between the ith and the ith+n point on contour
    
    Taken from http://stackoverflow.com/questions/22029548/is-it-possible-in-opencv-to-plot-local-curvature-as-a-heat-map-representing-an-o
    '''
    
    # Compute gradients
    GX = cv2.Scharr(img, cv2.CV_32F, 1, 0, scale=1)
    GY = cv2.Scharr(img, cv2.CV_32F, 0, 1, scale=1)
    GX = GX + 0.0001  # Avoid div by zero

    if plot:
        heatmap = np.zeros_like(img, dtype=np.float)
    
    contour = cnt.squeeze()
    measure = []
    N = len(contour)
    for i in xrange(N):
        x1, y1 = contour[i]
        x2, y2 = contour[(i + n) % N]

        # Angle between (gx1, gy1) and (gx2, gy2)
        gx1 = GX[y1, x1]
        gy1 = GY[y1, x1]
        gx2 = GX[y2, x2]
        gy2 = GY[y2, x2]
        cos_angle = gx1 * gx2 + gy1 * gy2
        cos_angle /= (np.linalg.norm((gx1, gy1)) * np.linalg.norm((gx2, gy2)))
        angle = np.arccos(cos_angle)
        
        if cos_angle < 0.0:
            angle = np.pi - angle

        x1, y1 = contour[((2*i + n) // 2) % N]  # Get the middle point between i and (i + n)
        if plot:
            heatmap[y1, x1] = angle  # Use angle between points as score
            
        measure.append((angle, x1, y1, gx1, gy1))
#    # # Possible to filter for those blobs with measure > val in heatmap instead.
#    pointed_points.append((x1, y1, gx1, gy1))    

    angle=[]
    for m in measure:
        angle.append(m[0])
    angle=np.array(angle)
    
#    if plot:
##        heatmap = cv2.GaussianBlur(heatmap, (3, 3), heatmap.max())
#        f2=plt.figure()
#        ax = f2.add_subplot(111)
#        plt.imshow(img,cmap = 'gray')
#        plt.imshow(heatmap, cmap=plt.cm.jet)
#        plt.colorbar()
#        measureCuravture = smooth(angle)
#        maxCurvature = max(measureCuravture)  # Most pointed point for each contour
#        plt.text(0.5, 0.5,'max Curavture = %f' %maxCurvature,
#             horizontalalignment='center',
#             verticalalignment='center',
#             transform = ax.transAxes)
#        plt.title('Curvature')
#        
#        plt.show()
#        if platform.system() == 'Linux':
#            savepath=path+'Check\\Curvature\\'+str(ii)+'\\'
#        elif platform.system() == 'Windows': 
#            savepath=path+'Check/Curvature/'+str(ii)+'/'
#        if not os.path.exists(savepath): os.makedirs(savepath)
#            
#        import time
#        millis = int(round(time.time() * 1000))
#        filesavepath=savepath+'Curavture_'+str(ii)+'_'+str(millis)+'.png'
#        plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
#        plt.close(f2)
    
    return angle
        
        

    
def findContour(img, lowerThreshold, ratio, closing=False, kernelsize=3, plot=False, path=None, i=0, printDebugInfo=False, mKernel=0):
    #Canny edge detection
    edges = cv2.Canny(img,lowerThreshold,lowerThreshold*ratio) 
    

    
    if edges is None:
        if printDebugInfo:
            print('\tin findContour: None from Canny edge detector')
        return None, -1, -1, -1, -1
        
    
    if  closing:
        #perform a morphplogical closing, to remove minor holes in the object
        kernel = np.ones((kernelsize,kernelsize),np.uint8)            
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        if edges is None:
            if printDebugInfo:
                print('\tin findContour: None from morphologyEx')
            return None, -1, -1, -1, -1
    
    #find Contours
    contours, hierarchy = cv2.findContours(edges,cv2.cv.CV_RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_NONE) #cv2.cv.CV_RETR_LIST || cv2.cv.CV_CHAIN_APPROX_NONE or cv2.cv.CV_CHAIN_APPROX_SIMPLE
    
    #select best contour
    cnt, x, y, w, h = selectContour(contours)
    
    if plot:
        if platform.system() == 'Linux':
            savepath=path+'Check\\Canny\\'+str(i)+'\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/Canny/'+str(i)+'/'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+'Edges_lT='+str(lowerThreshold)+'_ratio='+str(ratio)+'_closing='+str(closing)+'_kernel='+str(kernelsize)+'_mkernel='+str(mKernel)+'.jpg'
        cv2.imwrite(filesavepath, edges)


    
    return cnt, x, y, w, h
    
def tryAllParametersForContours(img, lowerThreshold, expectedArea, plot=False, path=None, i=-1, printDebugInfo=False):
    lowerThresholdList=[  lowerThreshold, lowerThreshold*0.95, lowerThreshold*1.05, lowerThreshold*0.9, lowerThreshold*1.1, lowerThreshold*1.2, lowerThreshold*0.8, lowerThreshold*1.3,  lowerThreshold*0.7, lowerThreshold*1.4,  lowerThreshold*0.6 , lowerThreshold*1.5,  lowerThreshold*0.5]
    ratioList=[1.5, 2, 2.5, 3]
    kernelSize=[-1,3,5, 7] 
    medianBlur=[-1, 5, 9, 13, 19]   
    for m in medianBlur:     
        if m != -1:
            img = cv2.medianBlur(img, m)
            
        for lt in lowerThresholdList:
            for r in ratioList:
                for k in kernelSize:
                    if k == -1:
                        cnt, x, y, w, h = findContour(img, lt, r, closing=False, kernelsize=3, plot=plot, path=path, i=i, printDebugInfo=printDebugInfo, mKernel=m)
                    else:
                        cnt, x, y, w, h = findContour(img, lt, r, closing=True, kernelsize=k, plot=plot, path=path, i=i,printDebugInfo=printDebugInfo, mKernel=m)
                    #check area
                    if cnt is not None:
                        measureCuravture = findMaxCurvatureInContour(img, cnt, plot=plot, path=path,ii=i)
                        measureCuravture = smooth(measureCuravture)
                        maxCurvature = max(measureCuravture)  # Most pointed point for each contour
                        
                        if maxCurvature < maxCurvatureCutOff and not np.isnan(maxCurvature):
                            M = cv2.moments(cnt)                           
                            if M['m00'] > minArea*expectedArea and M['m00'] < maxArea*expectedArea:
                                #Get size of image
                                yImg,xImg = img.shape
                                if w < xImg*0.95 and h < yImg*0.95:
                                    print('Winning parameter combination: threshold = %d ratio= %.1f kernel=%d convexHull = %r median blur =%d' %(lt, r, k, False, m))
                                    return cnt, x, y, w, h
                            else:
                                cnt = cv2.convexHull(cnt, returnPoints=True)
                                M = cv2.moments(cnt) 
                                if M['m00'] > minAreaCH*expectedArea and M['m00'] < maxArea*expectedArea:
                                    #Get size of image
                                    yImg,xImg = img.shape
                                    if w < xImg*0.95 and h < yImg*0.95:
                                        if findMaxDistanceInCountour(cnt, expectedArea):
                                            print('Winning parameter combination: threshold = %d ratio= %.1f kernel=%d convexHull = %r median blur =%d A/Ae = %.2f len(cnt) = %d' %(lt, r, k, True, m, M['m00']/expectedArea, len(cnt)))
                                            return cnt, x, y, w, h
                                elif printDebugInfo:
                                        print('%d: Area (=%f) was wrong (expected = %f) in tryAllParametersForContours' %(i, M['m00'], expectedArea))
                        elif printDebugInfo:
                                print('%d: Curvature too big = %f in  tryAllParametersForContours' %(i, maxCurvature))
                    
                
    #Still no contour found, probably no capsule in image
    if printDebugInfo:
        print('Returnng None from tryAllParametersForContours')
    return None, -1, -1, -1, -1
    
def findMaxDistanceInCountour(cnt, expectedArea, n=10.0):
    '''
    Check that max distance between two points on a contour doesn't exceed
    thelimit of n equally spaced point
    '''
    maxd = (2*np.sqrt(np.pi*expectedArea))/n
    
    N=len(cnt)
    for ii in range(N):
        xdelta=cnt[ii][0][0]   - cnt[(ii + 1) % N][0][0] 
        ydelta=cnt[ii][0][1]   - cnt[(ii + 1) % N][0][1] 
        tempd=np.sqrt((xdelta*xdelta)+(ydelta*ydelta))
        if tempd > maxd:
#                print('\t Convec Hull: too large gap! d = %f dmax = %f' %(d, maxd)),
            return False
    return True


def cannyEdgeFind(img, lowerThreshold, offsetX=0, offsetY=0, expectedArea=-1,plot=False, printDebugInfo=False, i=0,  path=None, ratio=2):
    '''
    Will take a image and apply a Canny edge detection to it. It will then
    return a B&W image with the interior of the line filled with colour. 
    The upper threshold is by default twice the lower threshold.
    Inputs:
    img             The image to be used for edge detection
    threshold       The lower canny threshold, between 0 and 255/ratio
    ratio           the ratio between the lower and upper canny threshold
    offsetX         If image has been cropped, offset in x direction
    offsetY         If image has been cropped, offset in y direction
    expectedArea    The expected area of the capsule
    
    Outputs:
    cnt, 
    edges, 
    xCanny
    yCanny
    wCanny
    hCanny
    
    Approche: find edges with Canny filter, find contours and evaluate results
    If that doesn't work and an expectedArea is provided, try morphological
    closing and increacing threshold
    '''
#    if printDebugInfo:
#        print('type(img) = ' +str(type(img))),
    
    cnt, x, y, w, h = findContour(img, lowerThreshold, ratio, closing=False, kernelsize=3)
    
    if printDebugInfo:
        if cnt == None:
            print('cnt is not None after first contour')
            
    if expectedArea != -1:            
        #Check area
        if cnt is not None:
            M = cv2.moments(cnt)
            if M['m00'] < 0.2*expectedArea or M['m00'] > 1.8*expectedArea:
                if printDebugInfo:
                    print('Contour Area is too small: %.2f against expected Area = %.2f' %(M['m00'], expectedArea))
                cnt, x, y, w, h = tryAllParametersForContours(img, lowerThreshold, expectedArea, plot=plot, path=path, i=i, printDebugInfo=printDebugInfo)
        else:
            cnt, x, y, w, h = tryAllParametersForContours(img, lowerThreshold, expectedArea, plot=plot, path=path, i=i, printDebugInfo=printDebugInfo)
    
             
    if plot:
        cntCopy=cnt
        img2=img.copy()
        if cnt is not None:  
            M = cv2.moments(cnt)
            centroid_x = float(M['m10']/M['m00'])
            centroid_y = float(M['m01']/M['m00'])    

            xTest, yTest = centroid_for_polygon(cntCopy)
            area = area_for_polygon(cntCopy)
            
            if printDebugInfo:
                print('doing test - m00 = %.2f m10 = %.2f m01 = %.2f' %(M['m00'],M['m10'],M['m01'])),
                print(' x,y = (%2f, %2f) \t x,y = (%2f, %2f) \t difference = (%2f, %2f) \t area = %.2f' %(centroid_x, centroid_y, xTest, yTest, centroid_x-xTest, centroid_y - yTest, area))

            cv2.circle(img2,(int(centroid_x),int(centroid_y)), 3, (255,255,255), 2)
      
        cv2.rectangle(img2,(x,y),(x+w,y+h),(255,255,255),2) 

        
        if platform.system() == 'Linux':
            savepath=path+'Check\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/'
            
        cv2.imwrite(savepath+'Img_'+str(i)+'.jpg', img)
        cv2.drawContours(img, cnt, -1, 255)
        cv2.imwrite(savepath+'CannyReturned_'+str(i)+'.jpg', img)
        
        cv2.imwrite(savepath+'ImgWRect_'+str(i)+'.jpg', img2)

        

    
    return cnt, offsetX+x,offsetY+y,w,h
    
def trimImgByCanny(img, lowerThreshold, offsetX=0, offsetY=0, plot=False, i=0,  path=None, ratio=3):
    '''
    Will take a image and apply a Canny edge detection to it. It will then
    return a B&W image with the interior of the line filled with colour. 
    The upper threshold is by default twice the lower threshold.
    Inputs:
    img         The image to be used for edge detection
    threshold   The lower canny threshold, between 0 and 255/ratio
    ratio       the ratio between the lower and upper canny threshold
    offsetX     If image has been cropped, offset in x direction
    offsetY     If image has been cropped, offset in y direction
    
    Outputs:
    cnt, 
    edges, 
    xCanny
    yCanny
    wCanny
    hCanny
    '''
    printDebugInfo=False
    
    if printDebugInfo:
        print('type(img) = ' +str(type(img))),
    
    cnt, x, y, w, h = findContour(img, lowerThreshold, ratio, closing=False, kernelsize=3)
        
    #add expected area check if need be
    
    imgCropped = img[y-2:y+h+2, x-2:x+w+2]
    offsetX2 = x-2; offsetY2=y-2;
             
    if plot:        
        plt.show()
        if platform.system() == 'Linux':
            savepath=path+'Check\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+'ImageWithContour_'+str(i)+'.jpg'
        cv2.drawContours(img, cnt, -1, 255)
        imgCropped = img[y-2:y+h+2, x-2:x+w+2]
        cv2.imwrite(filesavepath, imgCropped)

    return imgCropped, cnt, offsetX+offsetX2,offsetY+offsetY2,w,h
    


def find_max_extend(path, d0, pPmm, constantFrequency=False, rotate=0.0, plot=False, threshold=150, printDebugInfo=False):
    """Goes though all the pictures in directory, thresholds them and finds 
    several measurments for the resulting object, which should be a capsule if 
    the threshold has been chossen correctly
    """
    fileID=find_batchName(path);
    ERROR_CONST=-1
    
    #initial 2D projected area
    A0=np.pi*np.power(d0/2,2)
    #initial perimeter
    p0=2.0*np.pi*(d0/2)

    #close all graphs
    plt.close("all")
    
    #'forShow is a boolean variable that governs whether plot is displayed 
    #during program run. 
    forShow=False    
    
    #This sets the threshold what is counted as black in grayscale image and 
    #should be between 0-255
    #A threshold of 110 worked robustly over a wide range
#    threshold=150
    
    #get sorted list of filenames
    if constantFrequency:
        fileList, leng =sortPhotosPCO(path)
        print('Using sortPhotosPCO')
    else:
        fileList, leng =sortPhotos2(path)
        print('Using sortPhotos2')
    print('leng = %d' %leng)
    #Initializing variable to hold the area, perimeter and vertical distance
    #(y-direction) for each image
    area = np.zeros((leng), dtype=float)
    perimeter = np.zeros((leng), dtype=float)
    verticalDistance = np.zeros((leng), dtype=float)
    horizontalDistance = np.zeros((leng,1), dtype=float)
    width = np.zeros((leng), dtype=float)
    heigth = np.zeros((leng), dtype=float)
    centroid_x = np.zeros((leng), dtype=float)
    centroid_y = np.zeros((leng), dtype=float)
    D = np.zeros((leng), dtype=float)
    angle = np.zeros((leng), dtype=float)
    velx = np.zeros((leng), dtype=float)
    vely = np.zeros((leng), dtype=float)
    
    #counter of images
    counterL=-1
    
    #border that is added to image 
    borderSize=10
    
    fullMontyFailed=0
    failedIndexes=[]
   
    #Iterating over all pictures
    for i in range(leng):
        plt.close('all')
        gc.collect()
        counterL=counterL+1
        
        #print info every 10th picture
        if i%10 == 0:
            print("Current frame " + str(i) + "\t and counter is on " +  str(counterL))# + " and memory used is: ")
            
        #read image
        readPath=path+fileList[i].fn
#        print("readfind_max_extendPath: %s" %readPath)
        img =cv2.imread(readPath,0)
        
        if rotate != 0:
            img=rotateImage(img, rotate)

        if(plot):
            plt.figure(num='Initial', facecolor='w', edgecolor='k', figsize=(24, 8), dpi=600)
            a1=plt.subplot(131)
            plt.imshow(img, cmap='Greys')

        #add a border of black pixels around image in case capsule touches edge    
        img=cv2.copyMakeBorder(img,borderSize,borderSize,borderSize,borderSize,
                               cv2.BORDER_CONSTANT,value=(255, 255, 255))    
        
        #Get size of image
        yImg,xImg = img.shape
        
        #Add a rectanlge over areas of image not of intrest, to prevent 
        #interference from these areas        
        
        paddingOffset=5        
        
        topCropLevel=25+borderSize #where to cut the top of the image
#        topCropLevel=66+borderSize #where to cut the top of the image
        
#        dex=125  # daugther channel bottom edge        
        dex=114  # daugther channel bottom edge    
        leftEdge=559
        rightEdge=733
        
#        #PCO SETUp
#        cv2.rectangle(img, (0, dex+borderSize+paddingOffset), (540+borderSize-paddingOffset, yImg), 255,
#                      thickness=-1)   
#        cv2.rectangle(img, (725+borderSize+paddingOffset, dex+borderSize+paddingOffset), (xImg, yImg),  255,
#                      thickness=-1)
#        #Block out timestamp from pco camera
#        cv2.rectangle(img, (0+borderSize, 0+borderSize), (xImg+borderSize, topCropLevel), 255,
#                      thickness=-1)
                      
        #PCO SETUp
        cv2.rectangle(img, (0, dex+borderSize+paddingOffset), (leftEdge+borderSize-paddingOffset, yImg), 255,
                      thickness=-1)   
        cv2.rectangle(img, (rightEdge+borderSize+paddingOffset, dex+borderSize+paddingOffset), (xImg, yImg),  255,
                      thickness=-1)
        #Block out timestamp from pco camera
        cv2.rectangle(img, (0+borderSize, 0+borderSize), (xImg+borderSize, topCropLevel), 255,
                      thickness=-1)
                      
#        #special edge remover
#        trimBy=220
#        cv2.rectangle(img, (0+borderSize, 0+borderSize), (trimBy+borderSize, yImg), 255,  thickness=-1)
#        cv2.rectangle(img, (xImg-borderSize-trimBy, 0+borderSize), (xImg, yImg), 255,  thickness=-1)

        
        #make a copy, to ensure we are not changing the image
        im=img.copy()        
        
#        cnt, thresh, xBT,yBT,w,h = findContoursByThresholding(img, threshold, plot=plot, counter=i, path=path, expectedArea=A0*np.power(pPmm,2), printDebugInfo=printDebugInfo)
        cnt, thresh, xBT,yBT,w,h = findContoursByAdpativeThresholding(img,  plot=plot, counter=i, path=path, expectedArea=A0*np.power(pPmm,2), printDebugInfo=printDebugInfo)
        if printDebugInfo:
            print('\nPosition from Thresholding: x,y,w,h = (%d, %d, %d, %d) \t cnt[0][0][0] = %.2f' %(xBT,yBT,w,h, cnt[0][0][0]))
            
        padding=30
        top=yBT-padding
#        if top <  topCropLevel:
#            top= topCropLevel

        imgForCanny = img[top:yBT+h+padding, xBT-padding:xBT+w+padding]
        
        if plot:
            savepath=path+'Check\\'
            if not os.path.exists(savepath): os.makedirs(savepath)
            filesavepath=savepath+'imgForCanny-'+str(i)+'.jpg'
#            cv2.imwrite(filesavepath, imgForCanny)
#            filesavepath=savepath+'imgForCanny-Equalized-'+str(i)+'.jpg'
#            eql = cv2.equalizeHist(imgForCanny)
#            cv2.imwrite(filesavepath, eql)
#            filesavepath=savepath+'imgForCanny-Median-'+str(i)+'.jpg'
#            med = cv2.medianBlur(imgForCanny, 13)
#            cv2.imwrite(filesavepath, med)

            
        cntCanny, xCanny,yCanny,wCanny,hCanny = cannyEdgeFind(imgForCanny, threshold/3*2, offsetX=xBT-padding, offsetY=yBT-padding, expectedArea=A0*np.power(pPmm,2), plot=plot, printDebugInfo=printDebugInfo, i=i, path=path)
        
        if printDebugInfo:
            if cntCanny == None:
                print('cntCanny = ' +str(cntCanny)),
            else:
                print('cntCanny[0][0][0] = %.2f' %cntCanny[0][0][0]),

        contourFound=False
        
        if cntCanny is not None:
            contourFound=True
#        elif cntCanny == None and cnt is not None:
#            img2 = cv2.equalizeHist(img)
#            imgForCanny = img2[top:yBT+h+padding, xBT-padding:xBT+w+padding]
#            
#            for jj in range(5):
#                cntCanny, xCanny,yCanny,wCanny,hCanny = cannyEdgeFind(imgForCanny, 35*(jj+1), offsetX=xBT-padding, offsetY=yBT-padding, expectedArea=A0*np.power(pPmm,2), plot=plot, printDebugInfo=printDebugInfo, i=i, path=path)
#                if cntCanny != None:
#                    break
#                
#            if cntCanny == None:
#                fullMontyFailed +=1
#                failedIndexes.append(i)
#                if printDebugInfo:
#                    print('2nd try failed failed')
#                
#        elif cntCanny == None and cnt is not None:
#            fullMontyFailed +=1
#            failedIndexes.append(i)
#            if printDebugInfo:
#                print('Using Thresholding Image to startCanny')
#            
#            imgForCanny2 = thresh[top:yBT+h+padding, xBT-padding:xBT+w+padding]                
#            cntCanny, xCanny,yCanny,wCanny,hCanny = cannyEdgeFind(imgForCanny2, threshold/3*2, offsetX=xBT-padding, offsetY=yBT-padding, expectedArea=A0*np.power(pPmm,2), plot=plot, printDebugInfo=printDebugInfo, i=i, path=path)
#            
#            if cntCanny is None:
#                if printDebugInfo:
#                    print('Using Thresholding')
#                cntCanny, xCanny,yCanny,wCanny,hCanny =  cnt,  xBT,yBT,w,h
#                contourFound=True
#            else:
#                contourFound=True
        else:
            fullMontyFailed +=1
            failedIndexes.append(i)
            if printDebugInfo:
                print('Thresholding failed')
            
        if contourFound:  
            if(plot):
                a1=plt.subplot(132)
                plt.imshow(thresh, cmap='Greys')
                #draw bounding box and countour
                cv2.rectangle(im,(xCanny,yCanny),(xCanny+wCanny,yCanny+hCanny),(255,255,255),2)    
    #            cv2.drawContours(im, contours,ID,(255,255,255),2)
                
            #fit ellipse
            if len(cntCanny) <= 5:
                print('length1 less than 5 for i = %d' %(i));
                if i==37:
    #                    cv2.imshow('With Contours '+str(i)s,im)
                    plt.imshow(im)
                    
                                #find are of contour and perimeter
                area[counterL] = ERROR_CONST
                perimeter[counterL] = ERROR_CONST
                
                width[counterL]=ERROR_CONST
                heigth[counterL]=ERROR_CONST
                verticalDistance[counterL] = ERROR_CONST
                horizontalDistance[counterL] = ERROR_CONST  
                
                D[counterL]=ERROR_CONST
                centroid_x[counterL] = ERROR_CONST
                centroid_y[counterL] = ERROR_CONST
                velx[counterL]= ERROR_CONST
                vely[counterL]= ERROR_CONST
            else:
                #find are of contour and perimeter
                area[counterL] = cv2.contourArea(cntCanny)
                perimeter[counterL] = cv2.arcLength(cntCanny,True)
                
                
                width[counterL]=wCanny
                heigth[counterL]=hCanny
                verticalDistance[counterL] = (hCanny+0.0)/(pPmm+0.0)
                horizontalDistance[counterL] = (wCanny+0.0)/(pPmm+0.0)      
                
                #fit ellipse
                ellipse = cv2.fitEllipse(cntCanny)
                (x,y),(ma, MA),angle[counterL] = cv2.fitEllipse(cntCanny)
#                cv2.ellipse(im,ellipse,(0,255,255),2)
            
                #Taylor parameter
                D[counterL]=(MA-ma)/(MA+ma)
                
                if printDebugInfo:
                    print('(x,y) = (%d, %d) - width = %d height = %d \t Canny: (x,y) = (%d, %d) - width = %d height = %d  Taylor Deformation Parameter = %.2f (ma, MA) = (%.2f, %.2f)' %(x, y, w, h,  xCanny,yCanny,wCanny,hCanny, D[counterL], ma, MA)),
                else:
                    print('(x,y,w,h) = (%d, %d,%d, %d)\tD12 = %.2f (ma, MA) = (%.2f, %.2f)' %(xCanny,yCanny,wCanny,hCanny, D[counterL], ma, MA)),
    
                #find centroid
                M = cv2.moments(cntCanny)
                try:
#                    print('x = %d , borderSize = %d, padding = %d ' %(xBT, borderSize, padding))
                    centroid_x[counterL] = xBT - borderSize - padding + int(M['m10']/M['m00']) #xCanny + int(M['m10']/M['m00'])
                    centroid_y[counterL] = yBT - borderSize - padding + int(M['m01']/M['m00']) #yCanny + int(M['m01']/M['m00'])
                except: 
                    centroid_x[counterL] = ERROR_CONST
                    centroid_y[counterL] = ERROR_CONST
            
            if(plot):
                a1=plt.subplot(133)
                plt.imshow(im, cmap='Greys')
                plt.text(0.3, 0.85, 'V D =  %.3f ' % (verticalDistance[counterL]/(d0)),
                fontsize=12,
                color = 'w',
                horizontalalignment='left',
                verticalalignment='center',
                transform=a1.transAxes)
                #plt.show()        
            
            #print("BotomY = " +str(bottommost)+" TopY = "+str(topmost))
            #print("Area = " +str(area)+" Perimeter = "+str(perimeter))
            #savepath=path+'Check\\'
            if(plot):
                savepath=path+'Check\\'
                if not os.path.exists(savepath): os.makedirs(savepath)
                filesavepath=savepath+'Junction_'+str(i)+'.jpg'
                plt.savefig(filesavepath, dpi=300)
    
                fig = plt.figure(dpi=300,)
                plt.imshow(thresh, cmap='Greys')
                filesavepath=savepath+'Junction_Big_'+str(i)+'.jpg'
                plt.savefig(filesavepath, dpi=300)
                
                
                if(forShow==False):
                    plt.clf()
                    plt.close("all")
                    
        else:
            #savepath=path+'Check\\'
            if(plot):
                savepath=path+'Check\\'
                if not os.path.exists(savepath): os.makedirs(savepath)
                filesavepath=savepath+'Junction_'+str(i)+'.jpg'
                plt.savefig(filesavepath, dpi=300)
                if(forShow==False):
                    plt.clf()
                    plt.close("all")
            print("No contour!")
        
        del img
        gc.collect()
        #plt.close("all")
    
    disp_x  = np.zeros((leng-1), dtype=float)
    disp_y = np.zeros((leng-1), dtype=float)
    vel_x = np.zeros((leng-1), dtype=float)
    vel_y= np.zeros((leng-1), dtype=float)
#    speed_inPixels= np.zeros((leng-1,1), dtype=float)
    speed= np.zeros((leng-1), dtype=float)
    speed_ave= np.zeros((leng-1), dtype=float)
    time= np.zeros((leng), dtype=float)
    time[0]=0.0
    
    for i in range(1,leng-1):
        disp_x[i]= centroid_x[i] - centroid_x[i-1] 
        disp_y[i]= centroid_y[i] - centroid_y[i-1] 
        
        dispCutOff=100.0
        if abs(disp_x[i]) > dispCutOff:
            print('disp_x[i] > %f: disp_x[%d]=%e' %(dispCutOff, i,disp_x[i]))
            disp_x[i]=0
        
        if abs(disp_y[i]) > dispCutOff:
            print('disp_y[i] > %f: disp_y[%d]=%e' %(dispCutOff, i,disp_y[i]))
            disp_y[i]=0
                    
        if constantFrequency:
            fps=fileList[i].fps+0.0
            deltaT=1.0/fps
            time[i]=time[i-1]+deltaT
            vel_x[i] = (disp_x[i]/pPmm)/deltaT
            vel_y[i] = (disp_y[i]/pPmm)/deltaT            
        else:
            deltaT=((fileList[i].timestamp1-fileList[i-1].timestamp1)/1000.0)
            time[i]=time[i-1]+deltaT
            vel_x[i] = (disp_x[i]/pPmm)/deltaT
            vel_y[i] = (disp_y[i]/pPmm)/deltaT
        
        velocityCutOff=100.0
        if abs(vel_x[i]) > velocityCutOff:
            print('vel_x[i] > %f: vel_x[%d]=%e' %(velocityCutOff, i,vel_x[i]))
            vel_x[i]=0
        
        if abs(vel_y[i]) > velocityCutOff:
            print('vel_y[i] > %f: vel_y[%d]=%e' %(velocityCutOff, i,vel_y[i]))
            vel_y[i]=0
    
    #Running average
    aveWindow=4
    speed = np.sqrt( np.power( vel_x ,2) + np.power(vel_y ,2) )
    speed_ave = np.sqrt( np.power( runningMean(vel_x, aveWindow) ,2) + np.power(runningMean(vel_y, aveWindow) ,2) )
    speed_ave =  runningMean(speed_ave, aveWindow)  
    speed_ave =  runningMean(speed_ave, aveWindow)   
    
    #identify different regions
    dx = gradient(speed_ave, h=1/60)
    zx=np.arange(len(dx))
    
    plt.figure(1)
    plt.plot(zx, dx, 'oc',label='Gradient Speed', markersize=5)
    plt.title("dx"+" " + fileID)
    plt.ylabel("dx")
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_GradientSpeed_Graph.jpg")
    
    
    #Write results to file    
    fo = open(path+fileID+'_Results.txt', "w")
    fo.write("# \t Ver Dist \t Hor Dist \t Perimeter \t Area \t centroid_x \t centroid_y \t width[i] \t heigth[i] \t D \t angle \t time (s) \tvel_x (mm/s)\t vel_y (mm/s)\t  \n\n\n")
    for i in range(leng) :
        if i==0:
            fo.write("%d \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \n" %(i, verticalDistance[i], horizontalDistance[i], perimeter[i], area[i], centroid_x[i], centroid_y[i], width[i], heigth[i], D[i], angle[i],time[i]))
        else:
            fo.write("%d \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \n" %(i, verticalDistance[i], horizontalDistance[i], perimeter[i], area[i], centroid_x[i], centroid_y[i], width[i], heigth[i], D[i], angle[i],time[i], vel_x[i-1], vel_y[i-1]))
    fo.close()
    
    fo = open(path+fileID+'_Failed.txt', "w")
    fo.write('\bFailed to follow proper protocoll %d times. The indexes on which this occured are: \n' %fullMontyFailed)
    for s in failedIndexes :
        fo.write('\t %d' %s)
    fo.close()

    #plot all variables
                
    #Remove crazy entries
                
                
                
    x=np.arange(leng)
    
    #normalize by initial length
    verticalDistance=verticalDistance/(d0)
    horizontalDistance=horizontalDistance/(d0)
    
    #plost results
    plt.figure(2)
    plt.plot(x, verticalDistance, 'oc',label='Vertical', markersize=5)
    plt.plot(x, horizontalDistance, 'sb',label='Horizontal', markersize=5)
    plt.title("Extend of Capsule"+" " + fileID)
    plt.xlabel("Picture # ")
    plt.ylabel("Extend [d0]")
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_Extend_Graph.jpg")
    
    area=area/(np.power(pPmm,2))
    area=area/A0
    
    plt.figure(3)
    plt.plot(x, area, 'or',label='Area', markersize=5)
    plt.title("Area"+" " + fileID)
    plt.xlabel("Picture # ")
    plt.ylabel("Area / Initial Area")
    plt.savefig(path+fileID+"_Area_Graph.jpg")
    
    perimeter=perimeter/pPmm
    perimeter=perimeter/p0
    
    plt.figure(4)
    plt.plot(x, perimeter, 'sb',label='Perimeter', markersize=5)
    plt.title("Perimeter"+" " + fileID)
    plt.xlabel("Picture # ")
    plt.ylabel("Perimeter/ Initial Perimeter")
    plt.savefig(path+fileID+"_Perimeter_Graph.jpg")
    
    print("Max Values for vertical extend, perimeter and area \t"+ str(np.max(verticalDistance))+"\t"+ str(np.max(perimeter))+"\t"+ str(np.max(area)))
    
    r=np.zeros(3)
    r[0]=np.max(verticalDistance)
    r[1]=np.max(perimeter)
    r[2]=np.max(area)    
    
    #plotVelocity graphs
    # evaluate speed
    
    plt.figure(5)
    plt.plot(centroid_x,centroid_y, 'sb',label='Centroid Position', markersize=5)
    plt.title("Centroid Position"+" " + fileID)
    plt.xlabel("Z Position [pixels]")
    plt.ylabel("Y Position [pixels]")
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_CentroidPosition_Graph.jpg")        

    
    x1=np.arange(leng-1)
        
    plt.figure(6)
    plt.plot(x1, vel_x, 'sb',label='v_x', markersize=5)
    plt.plot(x1, vel_y, 'or',label='v_y', markersize=5)
    plt.title("Velocity"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Velocity [mm/s]")
    plt.legend()
    plt.savefig(path+fileID+"_Velocity_Graph.jpg")
    
    plt.figure(7)
    plt.plot(x1, disp_x, 'sb',label='disp_x', markersize=5)
    plt.plot(x1, disp_y, 'or',label='disp_y', markersize=5)
    plt.title("Displacment"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Displacment [pixels]")
    plt.legend()
    plt.savefig(path+fileID+"_Displacment_Graph.jpg")
    
    plt.figure(8)
    plt.plot(x, time, 'sb',label='Time (s)', markersize=5)
    plt.title("Time [s]"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Time [s] ")
    plt.legend()
    plt.savefig(path+fileID+"_Time_Graph.jpg")
    
    plt.figure(9)
    plt.plot(x1, speed_ave, 'sb',label='Speed Averaged', markersize=5)
    plt.title("SpeedAveraged"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Speed[mm/s]")
    plt.legend()
    plt.savefig(path+fileID+"_SpeedAve_Graph.jpg")
    
    plt.figure(10)
    plt.plot(x1, runningMean(disp_x, 6), 'sb',label='running mean disp_x', markersize=5)
    plt.plot(x1, runningMean(disp_y, 6), 'or',label='running mean disp_y', markersize=5)
    plt.title("Displacment Runnung Average"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Displacment [pixels]")
    plt.legend()
    plt.savefig(path+fileID+"_DisplacmentRunnungAverage_Graph.jpg")
    
    plt.figure(9)
    plt.plot(x1, speed, 'or',label='Speed', markersize=5)
    plt.title("Speed"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Speed[mm/s]")
    plt.legend()
    plt.savefig(path+fileID+"_Speed_Graph.jpg")
    
    plt.figure(11)
    plt.plot(x,centroid_x, 'sb',label='Centroid x ', markersize=5)
    plt.plot(x,centroid_y, 'or',label='Centroid y ', markersize=5)
    plt.title("Centroid Position"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Centroid Position [pixels]")
    plt.legend()
    plt.savefig(path+fileID+"_CentroidPosition2_Graph.jpg") 
    
    plt.figure(12)
    plt.plot(x,width, 'sb',label='Width ', markersize=5)
    plt.plot(x,heigth, 'or',label='Heigth', markersize=5)
    plt.title("Size of Particle"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Width / Hiegth [pixels]")
#    plt.ylim((70,82))
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_width-heigth_Graph.jpg") 
    
    plt.figure(13)
    plt.plot(x,D, 'sb',label='Taylor Deformation Parameter ', markersize=5)
    plt.title("Taylor Deformation Parameter"+" " + fileID)
    plt.xlabel("Taylor Deformation Parameter")
    plt.ylabel("Width / Hiegth [pixels]")
#    plt.ylim((70,82))
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_Talyor-Deformation_Graph.jpg")
    
    print('\b Failed to follow proper protocoll %d times out of %d images.' %(fullMontyFailed,leng))
        
    return r
    


def find2DOutlineMainChannel(path, pPmm,d0, startPic=-1, endPic=-1, threshold=110, plot=False, rotate=0.0):
    '''
    find the equivalent 2D outline in the straigth channel (i.e. without 
    parachute).
    
    path            path to folder containing the files
    pPmm            Pixels per milimeter
    d0              diameter of object in mm
    threshold       threshold for finding object (between 0 -255)
    plot            True/False create and save figures to check progress of program.
                    These are saved to a folder named 'Check'
    '''

    fileID=find_batchName(path);
    ERROR_CONST=-1

    #initial 2D projected area
    A0=np.pi*np.power(d0/2,2)
    #initial perimeter
    p0=2.0*np.pi*(d0/2)
    
    fileList, leng =sortPhotosPCO(path)

    #counter of images
    counterL=-1
    
    #border that is added to image 
    borderSize=10
   
    #Iterating over all pictures
    for i in range(leng):
        counterL=counterL+1
        
        if startPic !=-1 and endPic != -1:
            if i < startPic:
                continue
            elif i > endPic:
                break
        
        #print info every 10th picture
        if i%5 == 0:
            print("Current frame " + str(i) + "\t and counter is on " +  str(counterL))# + " and memory used is: ")
            
        #read image
        readPath=path+fileList[i].fn
#        print("readPath: %s" %readPath)
        img =cv2.imread(readPath,0)
        
        if rotate != 0:
            img=rotateImage(img, rotate)
        
        #Get size of image
        yImg,xImg = img.shape
        
        #Add a rectanlge over areas of image not of intrest, to prevent 
        #interference from these areas        
        paddingOffset=25        
        
        topCropLevel=63+borderSize #where to cut the top of the image
        
        #PCO SETUp
        cv2.rectangle(img, (0, 165+borderSize+paddingOffset), (545+borderSize-paddingOffset, yImg), 255,
                      thickness=-1)   
        cv2.rectangle(img, (720+borderSize+paddingOffset, 165+borderSize+paddingOffset), (xImg, yImg),  255,
                      thickness=-1)
        #Block out timestamp from pco camera
        cv2.rectangle(img, (0+borderSize, 0+borderSize), (xImg+borderSize, topCropLevel), 255,
                      thickness=-1)

        
        #make a copy, to ensure we are not changing the image
        im=img.copy()        
        
        cnt, thresh, x,y,w,h = findContoursByThresholding(img, threshold)
        
        padding=20
        top=y-padding
        if top <  topCropLevel:
            top= topCropLevel
        
        imgForCanny = img[top:y+h+padding, x-padding:x+w+padding]

        imgCropped, cntCanny, xCanny,yCanny,wCanny,hCanny = trimImgByCanny(imgForCanny, threshold/3*2, offsetX=x-padding, offsetY=y-padding, plot=False, i=i, path=path)

        if cntCanny is not None:  
            xPosMerged,yPosMerged=findParachute(imgCropped, threshold/3*2, plot=plot, path=path, i=i)
            
            padding=2*pPmm
            displayImage= img[yCanny-padding:yCanny+hCanny+padding, xCanny-padding:xCanny+wCanny+padding]
            
            #convert coordinates to image coordinates
            xPosMerged=np.array(xPosMerged); yPosMerged=np.array(yPosMerged)   
            xPosMerged=xPosMerged+padding
            yPosMerged=yPosMerged+padding
            
            ySize,xSize =displayImage.shape
            #create image and write to text file
            f1=plt.figure()
            plt.imshow(displayImage,cmap = 'gray')
 
            plt.plot(xPosMerged, yPosMerged, 'sw', markersize=1, markeredgecolor = 'w')
            
            plt.title(str(fileID) + ' Parachute Plot')
            plt.xlim(0, xSize)
            plt.ylim(ySize, 0)
            
            plt.show()
            if platform.system() == 'Linux':
                savepath=path+fileID+'_Parachute/'
            elif platform.system() == 'Windows': 
                savepath=path+fileID+'_Parachute\\'
            if not os.path.exists(savepath): os.makedirs(savepath)
            filesavepath=savepath+fileID+'_ParachutePlot_'+str(i)+'.jpg'
            plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
            plt.close(f1)            
            
            xPosMerged=xPosMerged+xCanny-padding
            yPosMerged=yPosMerged+yCanny-padding            
            
            #Write results to file    
            fo = open(savepath+fileID+'_Outline_'+str(i)+'.txt', "w")
            fo.write(" Outline for %s , the %d th picture with pixels/mm = %.2f . Below are the (x, y) coordinates of the outline without parachute. \n\n" %(fileID, i, pPmm))
            for qq in range(len(xPosMerged)) :
                fo.write("%d \t %d \n" %(xPosMerged[qq], yPosMerged[qq]))
            fo.close()
            
            plt.close('all')
            
        else:
            print("No contour!")
        
        del img
        gc.collect()
            
        
def findParachute(img, lowerThreshold, plot=False, path='', i=0):
    '''
    Find parachute assuming the capsule is traveling in the positive y direction
    '''
    
    #find the same contour
    
    printDebugInfo=False
    
    if printDebugInfo:
        print('type(img) = ' +str(type(img))),
    
    cnt, x, y, w, h = findContour(img, lowerThreshold, 2, closing=False, kernelsize=3)
    
    if plot:
        print('%d \t (w,h) = (%d, %d)' %(i, w, h))

    if cnt is not None:
        M = cv2.moments(cnt)
        areaWhole = M['m00']
        
        #create image that is white outside the capsule
        capsule=img.copy()
        ySize,xSize = capsule.shape
        #iterate through image
        for y in range(ySize):
            for x in range(xSize):
                returned = cv2.pointPolygonTest(cnt, (x,y), measureDist=False)
                if returned < 0:
                    capsule[y,x] = 0
        
        workImg=capsule.copy()
        
        #Set upper and lower threshold by taking the average value over strips
        upperIntensity=0
        upperIntensitycounter=0
        
        ySize,xSize = workImg.shape
        for y in range(int(ySize*0.5), int(ySize*0.6)):
            for x in range(xSize):
                if workImg[y,x] != 0 :
                    upperIntensity += workImg[y,x]
                    upperIntensitycounter += 1
        upperIntensity = upperIntensity/(upperIntensitycounter+0.0)
        
        #for Batch120415-002 #1 30ml/min: int(upperIntensity*1.1) 
        upperThreshold=int(upperIntensity*1.05) 
        
        lowerIntensity=0
        lowerIntensitycounter=0
        

        for y in range(int(ySize*0.9), ySize):
            for x in range(xSize):
                if workImg[y,x] != 0 :
                    lowerIntensity += workImg[y,x]
                    lowerIntensitycounter += 1
        lowerIntensity = lowerIntensity/(lowerIntensitycounter+0.0)
        
        lowerThreshold=lowerIntensity*0.8
        
        if plot:
            print('upperIntensity = %.2f \t upperThreshold= %.2f \t lowerIntensity = %.2f \t lowerThreshold= %.2f' %(upperIntensity, upperThreshold, lowerIntensity, lowerThreshold)  )
        
        #Canny edge detection
        edges = cv2.Canny(workImg, lowerThreshold, upperThreshold)  
        
        if edges == None:
            return 
        
        #find Contours
        contours, hierarchy = cv2.findContours(edges,cv2.cv.CV_RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_NONE) #cv2.cv.CV_RETR_LIST || cv2.cv.CV_CHAIN_APPROX_NONE or cv2.cv.CV_CHAIN_APPROX_SIMPLE
        
        workImg2=workImg.copy()
        cv2.drawContours(workImg2,contours,-1,(255,255,255),1)
        
        #define edge as middel of the average intensities
        edgeThreshold=(lowerIntensity+upperIntensity)/2.0
        xIntrest=np.arange(int(0.2*xSize), int(0.8*xSize))
        parachutePos = np.zeros((len(xIntrest),2), dtype=float)# x,y
        
        counter=0
        for x in xIntrest:
            continueNow=False
            hasReachParachuteAverageIntensity=False
            for y in range(ySize-1, -1, -1):
                if workImg[y,x] >= lowerIntensity:
                     hasReachParachuteAverageIntensity=True
                     
                if workImg[y,x] <= upperThreshold and workImg[y,x] != 0 and continueNow == False and hasReachParachuteAverageIntensity:
                     parachutePos[counter][0]=x
                     parachutePos[counter][1]=y
#                     print('(%d, %d) Position added with intensity %d (threshold = %d)' %(x,y, workImg[y,x], edgeThreshold))
                     counter+=1
                     continueNow=True
                
                 
        #print(parachutePos)
        yPos=[]; xPos=[]; yPosCnt=[]; xPosCnt=[]; yPosMerged=[]; xPosMerged=[]
        
        for kk in range(len(parachutePos)):
            xPos.append(parachutePos[kk][0])
            yPos.append(parachutePos[kk][1])
            yPosMerged.append(parachutePos[kk][1])
            xPosMerged.append(parachutePos[kk][0])
        #Identify the part of the contour that needs ignoring
        
        yCutOff=np.max(yPos)*1.05
        print('yCutOff = %d' %yCutOff)
        
        for gg in range(len(cnt)):
            xPosCnt.append(cnt[gg][0][0])
            yPosCnt.append(cnt[gg][0][1])
            if yPosCnt[gg] < yCutOff:
                yPosMerged.append(yPosCnt[gg])
                xPosMerged.append(xPosCnt[gg])
        
                
            
        
    
    
#        print(cv2.pointPolygonTest(cnt, (x,y), measureDist=False))
             
    if plot:
        img2=img.copy()
        cv2.rectangle(img2,(x,y),(x+w,y+h),(255,255,255),1)     
        
        if platform.system() == 'Linux':
            savepath=path+'Check\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/'
        if not os.path.exists(savepath): os.makedirs(savepath)
            
        cv2.imwrite(savepath+'ImageCropped_'+str(i)+'.png', img2)
        
#        cv2.imwrite(savepath+'ImageCapsule_'+str(i)+'.png', capsule)
        
        cv2.imwrite(savepath+'WorkingImage_'+str(i)+'.png', workImg)
        cv2.imwrite(savepath+'WorkingImageWContour_'+str(i)+'.png', workImg2)
        
#        cv2.drawContours(img2, contours,ID,(255,255,255),1)
        f1=plt.figure()
        plt.imshow(workImg,cmap = 'gray')
        


        plt.plot(xPos, yPos, 'or', markersize=1)
        
        plt.title('Parachute Plot')
        
        plt.show()
        if platform.system() == 'Linux':
            savepath=path+'Check\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+'ParachutePlot_'+str(i)+'.png'
        plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
        plt.close(f1)
        
        f3=plt.figure()

        plt.plot(xPos, yPos, 'or', markersize=3, label='Parachute')
        plt.plot(xPosCnt, yPosCnt, 'ob', markersize=3, label='Contour')
        plt.plot(xPosMerged, yPosMerged, 'sb', markersize=1, label='Merged')
        plt.title('Parachute Plot')
        
        plt.show()
        if platform.system() == 'Linux':
            savepath=path+'Check\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+'Parachute_'+str(i)+'.png'
        plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
        plt.close(f3)
        
#        xPlot=[]; yPlot=[]
#        if cnt is not None:  
#            M = cv2.moments(cnt)
#            centroid_x = float(M['m10']/M['m00'])
#            centroid_y = float(M['m01']/M['m00'])    
#
#            xTest, yTest = centroid_for_polygon(cntCopy)
#            area = area_for_polygon(cntCopy)
#            
#            if printDebugInfo:
#                print('doing test - m00 = %.2f m10 = %.2f m01 = %.2f' %(M['m00'],M['m10'],M['m01']))
#                print('x,y = (%2f, %2f) \t x,y = (%2f, %2f) \t difference = (%2f, %2f) \t area = %.2f' %(centroid_x, centroid_y, xTest, yTest, centroid_x-xTest, centroid_y - yTest, area))
#
#            cv2.circle(img2,(int(centroid_x),int(centroid_y)), 3, (255,255,255), 2)
#            
#
#            for gg in range(len(cntCopy)):
#                xPlot.append(cntCopy[gg][0][0])
#                yPlot.append(cntCopy[gg][0][1])
#        
        f2=plt.figure()
        xaxis=np.arange(ySize)
        intensity25=[]
        intensity5=[]
        intensity75=[]
        for y in range(ySize):
            intensity25.append(workImg[y, int(xSize/4.0)])
            intensity5.append(workImg[y, int(xSize/2.0)])
            intensity75.append(workImg[y, int(3*xSize/4.0)])
        plt.plot(xaxis, intensity25, label='0.25')
        plt.plot(xaxis, intensity5, label='0.5')
        plt.plot(xaxis, intensity75, label='0.75')
        
        plt.plot([xaxis[0], xaxis[-1]], [lowerIntensity, lowerIntensity], label='Parachute Average Intensity', linestyle='-', linewidth=1)
        plt.plot([xaxis[0], xaxis[-1]], [upperIntensity, upperIntensity], label='Capsule Average Intensity', linestyle='-.', linewidth=1)        
        plt.plot([xaxis[0], xaxis[-1]], [lowerThreshold, lowerThreshold], label='Parachute Threshold', linestyle='--', linewidth=1)
        plt.plot([xaxis[0], xaxis[-1]], [upperThreshold, upperThreshold], label='Capsule Threshold', linestyle=':', linewidth=1)        
        plt.legend(loc=2, fontsize=6)
        plt.xlabel("Y-Coordinate [pixels]")
        plt.ylabel("Intensity (0 - Black, 255 - White)")
        
        plt.title('Intensity Plot')
        
        plt.show()
        if platform.system() == 'Linux':
            savepath=path+'Check\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+'IntensityPlot_'+str(i)+'.png'
        plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
        plt.close(f2)
        
    return xPosMerged,yPosMerged

def testThresholds(path, rotate=0, thresholds=[30, 60, 90, 120, 150, 180], tiff=False):
    
    fileID=find_batchName(path);
    ERROR_CONST=-1
    
    if tiff:
        fileList, leng =sortTiff(path)
    else:
        fileList, leng =sortPhotosPCO(path)
    
    

    pictures=[int(leng/7),int(2*leng/7), int(3*leng/7),int(4*leng/7), int(5*leng/7),int(6*leng/7) ]

    #Iterating over all pictures
    for i in pictures:
        #read image
        readPath=path+fileList[i].fn
#        print("readPath: %s" %readPath)
        img =cv2.imread(readPath,0)
        
        if rotate != 0:
            img=rotateImage(img, rotate)
        print('Thresholds = [%d, %d, %d, %d, %d, %d]' %(thresholds[0], thresholds[1], thresholds[2], thresholds[3], thresholds[4], thresholds[5]))
        ret, thresh50 = cv2.threshold(img,thresholds[0],255,cv2.THRESH_BINARY)
        ret, thresh80 = cv2.threshold(img,thresholds[1],255,cv2.THRESH_BINARY)
        ret, thresh120 = cv2.threshold(img,thresholds[2],255,cv2.THRESH_BINARY)
        ret, thresh150 = cv2.threshold(img,thresholds[3],255,cv2.THRESH_BINARY)
        ret, thresh5 = cv2.threshold(img,thresholds[4],255,cv2.THRESH_BINARY)
        ret, thresh6 = cv2.threshold(img,thresholds[5],255,cv2.THRESH_BINARY)
        
        xpos, ypos= 50, 50
        cv2.putText(thresh50,"Threshold = %d" %thresholds[0], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, thickness=4)
        cv2.putText(thresh80,"Threshold = %d" %thresholds[1], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, thickness=4)
        cv2.putText(thresh120,"Threshold = %d" %thresholds[2], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, thickness=4)
        cv2.putText(thresh150,"Threshold = %d" %thresholds[3], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, thickness=4)
        cv2.putText(thresh5,"Threshold = %d" %thresholds[4], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, thickness=4)
        cv2.putText(thresh6,"Threshold = %d" %thresholds[5], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, thickness=4)
        
        xpos, ypos= 50, 100
        cv2.putText(thresh50,"Threshold = %d" %thresholds[0], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, thickness=4)
        cv2.putText(thresh80,"Threshold = %d" %thresholds[1], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, thickness=4)
        cv2.putText(thresh120,"Threshold = %d" %thresholds[2], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, thickness=4)
        cv2.putText(thresh150,"Threshold = %d" %thresholds[3], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, thickness=4)
        cv2.putText(thresh5,"Threshold = %d" %thresholds[4], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, thickness=4)
        cv2.putText(thresh6,"Threshold = %d" %thresholds[5], (xpos, ypos), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, thickness=4)
                
        
        plotFour(thresh50, thresh80, thresh120, thresh150,thresh5, thresh6, path, 'CheckThreshold', 'CheckThreshold_'+str(i)+'.jpg', i)
            
def plotFour(img1, img2, img3, img4, img5, img6, path, folder, name, i):
        f2=plt.figure(dpi=200)
        f2.add_subplot(231)
        plt.imshow(img1,cmap = 'gray')
        f2.add_subplot(232)
        plt.imshow(img2, cmap = 'gray')
        f2.add_subplot(233)
        plt.imshow(img3, cmap = 'gray')
        f2.add_subplot(234)
        plt.imshow(img4, cmap = 'gray')
        f2.add_subplot(235)
        plt.imshow(img5, cmap = 'gray')
        f2.add_subplot(236)
        plt.imshow(img6, cmap = 'gray')
        plt.show()
        if platform.system() == 'Linux':
            savepath=path+folder+'/'
        elif platform.system() == 'Windows': 
            savepath=path+folder+'\\'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+name
        plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
        plt.close(f2)
        
        cv2.imwrite(savepath+'Thres1_'+str(i)+'.jpg', img1)
        cv2.imwrite(savepath+'Thres2_'+str(i)+'.jpg', img2)
        cv2.imwrite(savepath+'Thres3_'+str(i)+'.jpg', img3)
        cv2.imwrite(savepath+'Thres4_'+str(i)+'.jpg', img4)
        cv2.imwrite(savepath+'Thres5_'+str(i)+'.jpg', img5)
        cv2.imwrite(savepath+'Thres6_'+str(i)+'.jpg', img6)
    
    
    
def returnVelocityForSphericalRigidParticle(r,w,h, Q, rho=1000, viscosity=1000):
    '''
    Calculates the velocity of a rigid spherical particle for a rectangular
    channel of w * h given that the aspect ratio is less than 2. 
    Input:
    r           particle radius
    w           channel width 
    h           channel height
    viscosity   viscosity of the carrier fluid in cSt
    Q           volumn flux in ml / min
    
    Output:
    up          particle velocity
    v           maximum fluid velocity 
    '''
    assert w/h < 2.1 and w/h >0.49    
    #find size ratio
    sr= r / np.sqrt(w*h) 
    
    k1, k2 = getDragCoef(sr)
    
    vmax=maxVgivenQ(Q, y=0.0, z=h/2.0, w=2, h=h, nmax=10, rho=1000, nu = 1000)
    
    up = (k2/k1) *vmax
    return k1, k2, up
    
def getDragCoef(lamb):
    '''Based on the data reported in Al Quaddus et al (2008)
    
    Returns the drag coefficients K1, K2, defind as
    F = 6 * pi * mu * r *(k1 * u - k2 * v ) where u is the particle velocity 
    and v is the velocity of the fluid on that streamline at infinity
    '''
    if lamb <= 0.5:
        lamb0, k10, k20 = 0.0, 1.0, 1.0
        a1, b1 = 1.845, 0.7999
        a2, b2 = 1.694, 0.7751
    elif lamb <=0.8:
        lamb0, k10, k20 = 0.5, 5.9471, 4.9950
        a1, b1 = 3.604, 12.01
        a2, b2 = 3.445, 8.548
    elif lamb <= 0.95:
        lamb0, k10, k20 = 0.8, 74.6702, 47.6201
        a1, b1 = 9.364, 310.1
        a2, b2 = 9.236, 177.8
    else:
        import inspect
        print('In function %s called by %s : lambda is outside allowed ratio (0.0-0.95)' %( inspect.stack()[0][3],inspect.stack()[1][3] ))
        
    
    k1 = b1* ( lamb - lamb0) * np.exp( np.exp( a1 *  ( lamb - lamb0) ) ) + k10
    k2 = b2* ( lamb - lamb0) * np.exp( np.exp( a2 *  ( lamb - lamb0) ) ) + k20
    
    return k1, k2
        
        
def maxVgivenQ(Q, y, z, w=1, h=1, nmax=10, rho=1000, nu = 1000):
    '''
    Returns the maximum velocity for a rectangular channel of dimensions w x h
    at a volumn flux Q [ml/min]
    
    nmax    determines the number of fourier series terms to take into account. 
    rho     is the density of the fluid
    nu      is the viscosity in cSt
    
    y = [-w/2, w/2]
    z = [0,h]
    
    Based on http://web-files.ait.dtu.dk/bruus/tmf/publications/3week/jun2004hydraulicres.pdf
    '''
    #Get the pressure difference from the volumn flux, eqn 2.46
    nu=cStToSI(nu)
    Q=mlPminToSI(Q)
    
#    y=h/2.0
#    z=w/2.0
    
    y=0.2
    z=0.2
    
    
    psum=0
    for n in range(1, nmax, 2):   
        psum += (192 * h / (np.pi**5 *w * n**5 )) * np.tanh(n*np.pi * w/(2*h))
    
    P = Q* 12 * nu / ( rho* w * h**3 * (1-psum) )
    
    vsum=0
    for n in range(1, nmax*2, 2):  
        vsum += 1/n**3 * ( 1 - ( (np.cosh( n* np.pi * y/h)) / (np.cosh( n* np.pi * w/(2*h))) ) ) * np.sin( n* np.pi * z/h)
        
    v= (P* h**2 * 4) / (nu**2 * np.pi**3)  * vsum
    return v
    
def maxVgivenP( y,z, P=1, w=1, h=1, nmax=10, rho=1000, nu = 1000):
    '''
    Returns the maximum velocity for a rectangular channel of dimensions w x h
    at a volumn flux Q [ml/min]
    
    nmax    determines the number of fourier series terms to take into account. 
    rho     is the density of the fluid
    nu      is the viscosity in cSt
    
    Based on http://web-files.ait.dtu.dk/bruus/tmf/publications/3week/jun2004hydraulicres.pdf
    '''
    #Get the pressure difference from the volumn flux, eqn 2.46
    nu=cStToSI(nu)
    
    vsum=0
    for n in range(1, nmax*2, 2):  
        vsum += 1/n**3 * ( 1 - ( (np.cosh( n* np.pi * y/h)) / (np.cosh( n* np.pi * w/(2*h))) ) ) * np.sin( n* np.pi * z/h)
        
    v= (P* h**2 * 4) / (nu**2 * np.pi**3)  * vsum
    return v
    
def maxVgivenP2(x,y, nmax=20):  
    da=-5/2*(x - 1)*x;
    for n in range(nmax):
        top=(-4*1**2*5*np.cosh((n*np.pi*(1 - 2*y))/(2*1)) * (1/(np.cosh(1*n*np.pi/(2*1))))*np.sin(n*np.pi/2)**2  *np.sin(n*np.pi*x/1))
        bottom = (np.power(n,3) * np.pi**3)
#        print('top = %f bottom = %f' %(top, bottom))
        if top != 0.0 and bottom != 0.0:
            da=da+ top/bottom;
    
    return da
    
#def maxVgivenP2(y,z, nmax=10):
#    nu=cStToSI(nu)
#    xpoints=30
#    ypoints=30
#    
#    dx=1/xpoints
#    dy=1/ypoints    
#    
#    da = 0
#    
#    for ii in range(xpoints):
#        x=(ii-1)*dx;
#        for jj in range(ypoints):
#            y=(jj-1)*dy;
#            da(ii,jj)=-5/2*(x - 1)*x;
#            for n in range(nmax):
#                da(ii,jj)=da(ii,jj)+(-4*1^2*5*np.cosh((n*np.pi*(1 - 2*y))/(2*1)) \
#                * (1/(np.cosh(1*n*np.pi/(2*1))))*np.sin(n*np.pi/2)**2  \
#                *np.sin(n*np.pi*x/1))/(n^3*np.pi**3);
#    
#    return da

    
def cStToSI(nu):
    return nu/(10**6)

def mlPminToSI(Q):
    return Q * 10**(-6)/60
    
def track_bubble(path, d0, pPmm, constantFrequency=False, rotate=0.0, plot=False, threshold=150, printDebugInfo=False):
    """Goes though all the pictures in directory, thresholds them and finds 
    several measurments for the resulting object, which should be a capsule if 
    the threshold has been chossen correctly
    """
    fileID= 'Bubble';
    ERROR_CONST=-1
    
    #initial 2D projected area
    A0=np.pi*np.power(d0/2,2)
    #initial perimeter
    p0=2.0*np.pi*(d0/2)

    #close all graphs
    plt.close("all")
    
    #'forShow is a boolean variable that governs whether plot is displayed 
    #during program run. 
    forShow=False    
    
    #This sets the threshold what is counted as black in grayscale image and 
    #should be between 0-255
    #A threshold of 110 worked robustly over a wide range
#    threshold=150
    
    #get sorted list of filenames
    fileList, leng =sortTiff(path)

    print('leng = %d' %leng)
    imgArray=[]    
    for jj in range(8):
        readPath=path+fileList[jj].fn
        imgArray.append(cv2.imread(readPath,0))
        
    
    #Create subtracted image
    img11 = cv2.addWeighted(imgArray[0], 0.5, imgArray[1], 0.5, 0.0)   
    img12 = cv2.addWeighted(imgArray[2], 0.5, imgArray[3], 0.5, 0.0) 
    img13 = cv2.addWeighted(imgArray[4], 0.5, imgArray[5], 0.5, 0.0) 
    img14 = cv2.addWeighted(imgArray[6], 0.5, imgArray[7], 0.5, 0.0) 
    
    img21 = cv2.addWeighted(img11, 0.5, img12, 0.5, 0.0) 
    img22 = cv2.addWeighted(img13, 0.5, img14, 0.5, 0.0) 
    
    img31 = cv2.addWeighted(img21, 0.5, img22, 0.5, 0.0) 
    
    cv2.imwrite(path+'Check\\subtractImage.jpg', img31)
    
    #Initializing variable to hold the area, perimeter and vertical distance
    #(y-direction) for each image
    area = np.zeros((leng), dtype=float)
    perimeter = np.zeros((leng), dtype=float)
    verticalDistance = np.zeros((leng), dtype=float)
    horizontalDistance = np.zeros((leng,1), dtype=float)
    width = np.zeros((leng), dtype=float)
    heigth = np.zeros((leng), dtype=float)
    centroid_x = np.zeros((leng), dtype=float)
    centroid_y = np.zeros((leng), dtype=float)
    D = np.zeros((leng), dtype=float)
    angle = np.zeros((leng), dtype=float)
    velx = np.zeros((leng), dtype=float)
    vely = np.zeros((leng), dtype=float)
    
    #counter of images
    counterL=-1
    
    #border that is added to image 
    borderSize=10
    
    fullMontyFailed=0
    failedIndexes=[]
    
    fgbg1 = cv2.BackgroundSubtractorMOG()
#    fgbg2 = cv2.BackgroundSubtractorMOG2()
    
    #Iterating over all pictures
    for i in range(leng):
        plt.close('all')
        gc.collect()
        counterL=counterL+1
        
        #print info every 10th picture
        if i%10 == 0:
            print("Current frame " + str(i) + "\t and counter is on " +  str(counterL))# + " and memory used is: ")
            
        #read image
        readPath=path+fileList[i].fn
#        print("readPath: %s" %readPath)
        img =cv2.imread(readPath,0)
        
        if rotate != 0:
            img=rotateImage(img, rotate)

        if(plot):
            plt.figure(num='Initial', facecolor='w', edgecolor='k', figsize=(24, 8), dpi=600)
            a1=plt.subplot(131)
            plt.imshow(img, cmap='Greys')
            
        fgmask1 = fgbg1.apply(img)
  #        fgmask2 = fgbg2.apply(img)
        
#        img = img - img31         
#        cv2.imwrite(path+'Check\\subtractImage_'+str(i) + '.jpg', img)
        cv2.imwrite(path+'Check\\fgmask1_'+str(i) + '.jpg', fgmask1)
#        cv2.imwrite(path+'Check\\fgmas2k_'+str(i) + '.jpg', fgmask2)
        
        #add a border of black pixels around image in case capsule touches edge    
        img=cv2.copyMakeBorder(img,borderSize,borderSize,borderSize,borderSize,
                               cv2.BORDER_CONSTANT,value=(255, 255, 255))    
        
        #Get size of image
        yImg,xImg = img.shape
        
        #Add a rectanlge over areas of image not of intrest, to prevent 
        #interference from these areas        
        
        paddingOffset=25        
        
#        topCropLevel=30+borderSize #where to cut the top of the image
#        topCropLevel=66+borderSize #where to cut the top of the image
        
        dex=125  # daugther channel bottom edge        
        
        #PCO SETUp
        cv2.rectangle(img, (0, 0), (xImg, 140), 255, thickness=-1)  
        cv2.rectangle(img, (0, 300), (xImg, yImg), 255, thickness=-1) 
        
        cv2.rectangle(img, (0, 0), (650, yImg), 255, thickness=-1) 
        cv2.rectangle(img, (1840, 0), (xImg, yImg), 255, thickness=-1)

        
        #make a copy, to ensure we are not changing the image
        im=img.copy()        
        
        cnt, thresh, xBT,yBT,w,h = findContoursByThresholding(img, threshold, plot=plot, counter=i, path=path)
        
        if printDebugInfo:
            print('\nPosition from Thresholding: x,y,w,h = (%d, %d, %d, %d) \t cnt[0][0][0] = %.2f' %(xBT,yBT,w,h, cnt[0][0][0]))
            
        padding=20
        top=yBT-padding
#        if top <  topCropLevel:
#            top= topCropLevel
        
        imgForCanny = img[top:yBT+h+padding, xBT-padding:xBT+w+padding]
            
        cntCanny, xCanny,yCanny,wCanny,hCanny = cannyEdgeFind(imgForCanny, threshold/3*2, offsetX=xBT-padding, offsetY=yBT-padding, expectedArea=A0*np.power(pPmm,2), plot=plot, printDebugInfo=printDebugInfo, i=i, path=path)
        if printDebugInfo:
            if cntCanny == None:
                print('cntCanny = ' +str(cntCanny)),
            else:
                print('cntCanny[0][0][0] = %.2f' %cntCanny[0][0][0]),

        contourFound=False
        
        if cntCanny is not None:
            contourFound=True
        elif cntCanny == None and cnt is not None:
            fullMontyFailed +=1
            failedIndexes.append(i)
            if printDebugInfo:
                print('Using Thresholding Image to startCanny')
            
            imgForCanny2 = thresh[top:yBT+h+padding, xBT-padding:xBT+w+padding]                
            cntCanny, xCanny,yCanny,wCanny,hCanny = cannyEdgeFind(imgForCanny2, threshold/3*2, offsetX=xBT-padding, offsetY=yBT-padding, expectedArea=A0*np.power(pPmm,2), plot=plot, printDebugInfo=printDebugInfo, i=i, path=path)
            
            if cntCanny is None:
                if printDebugInfo:
                    print('Using Thresholding')
                cntCanny, xCanny,yCanny,wCanny,hCanny =  cnt,  xBT,yBT,w,h
                contourFound=True
            else:
                contourFound=True
        else:
            fullMontyFailed +=1
            failedIndexes.append(i)
            if printDebugInfo:
                print('Thresholding failed')
            
        if contourFound:  
            if(plot):
                a1=plt.subplot(132)
                plt.imshow(thresh, cmap='Greys')
    
                #draw bounding box and countour
                cv2.rectangle(im,(xCanny,yCanny),(xCanny+wCanny,yCanny+hCanny),(255,255,255),2)    
    #            cv2.drawContours(im, contours,ID,(255,255,255),2)
                
            #fit ellipse
            if len(cntCanny) <= 5:
                print('length1 less than 5 for i = %d' %(i));
                if i==37:
    #                    cv2.imshow('With Contours '+str(i)s,im)
                    plt.imshow(im)
                    
                                #find are of contour and perimeter
                area[counterL] = ERROR_CONST
                perimeter[counterL] = ERROR_CONST
                
                width[counterL]=ERROR_CONST
                heigth[counterL]=ERROR_CONST
                verticalDistance[counterL] = ERROR_CONST
                horizontalDistance[counterL] = ERROR_CONST  
                
                D[counterL]=ERROR_CONST
                centroid_x[counterL] = ERROR_CONST
                centroid_y[counterL] = ERROR_CONST
                velx[counterL]= ERROR_CONST
                vely[counterL]= ERROR_CONST
            else:
                #find are of contour and perimeter
                area[counterL] = cv2.contourArea(cntCanny)
                perimeter[counterL] = cv2.arcLength(cntCanny,True)
                
                
                width[counterL]=wCanny
                heigth[counterL]=hCanny
                verticalDistance[counterL] = (hCanny+0.0)/(pPmm+0.0)
                horizontalDistance[counterL] = (wCanny+0.0)/(pPmm+0.0)      
                
                #fit ellipse
                ellipse = cv2.fitEllipse(cntCanny)
                (x,y),(ma, MA),angle[counterL] = cv2.fitEllipse(cntCanny)
#                cv2.ellipse(im,ellipse,(0,255,255),2)
            
                #Taylor parameter
                D[counterL]=(MA-ma)/(MA+ma)
                
                if printDebugInfo:
                    print('(x,y) = (%d, %d) - width = %d height = %d \t Canny: (x,y) = (%d, %d) - width = %d height = %d  Taylor Deformation Parameter = %.2f (ma, MA) = (%.2f, %.2f)' %(x, y, w, h,  xCanny,yCanny,wCanny,hCanny, D[counterL], ma, MA)),
                else:
                    print('(x,y,w,h) = (%d, %d,%d, %d)\tD12 = %.2f (ma, MA) = (%.2f, %.2f)' %(xCanny,yCanny,wCanny,hCanny, D[counterL], ma, MA)),
    
                #find centroid
                M = cv2.moments(cntCanny)
                try:
#                    print('x = %d , borderSize = %d, padding = %d ' %(xBT, borderSize, padding))
                    centroid_x[counterL] = xBT - borderSize - padding + int(M['m10']/M['m00']) #xCanny + int(M['m10']/M['m00'])
                    centroid_y[counterL] = yBT - borderSize - padding + int(M['m01']/M['m00']) #yCanny + int(M['m01']/M['m00'])
                except: 
                    centroid_x[counterL] = ERROR_CONST
                    centroid_y[counterL] = ERROR_CONST
            
            if(plot):
                a1=plt.subplot(133)
                plt.imshow(im, cmap='Greys')
                plt.text(0.3, 0.85, 'V D =  %.3f ' % (verticalDistance[counterL]/(d0)),
                fontsize=12,
                color = 'w',
                horizontalalignment='left',
                verticalalignment='center',
                transform=a1.transAxes)
                #plt.show()        
            
            #print("BotomY = " +str(bottommost)+" TopY = "+str(topmost))
            #print("Area = " +str(area)+" Perimeter = "+str(perimeter))
            #savepath=path+'Check\\'
            if(plot):
                savepath=path+'Check\\'
                if not os.path.exists(savepath): os.makedirs(savepath)
                filesavepath=savepath+'Junction_'+str(i)+'.jpg'
                plt.savefig(filesavepath, dpi=300)
    
                fig = plt.figure(dpi=300,)
                plt.imshow(thresh, cmap='Greys')
                filesavepath=savepath+'Junction_Big_'+str(i)+'.jpg'
                plt.savefig(filesavepath, dpi=300)
                
                
                if(forShow==False):
                    plt.clf()
                    plt.close("all")
                    
        else:
            #savepath=path+'Check\\'
            if(plot):
                savepath=path+'Check\\'
                if not os.path.exists(savepath): os.makedirs(savepath)
                filesavepath=savepath+'Junction_'+str(i)+'.jpg'
                plt.savefig(filesavepath, dpi=300)
                if(forShow==False):
                    plt.clf()
                    plt.close("all")
            print("No contour!")
        
        del img
        gc.collect()
        #plt.close("all")
    
    disp_x  = np.zeros((leng-1), dtype=float)
    disp_y = np.zeros((leng-1), dtype=float)
    vel_x = np.zeros((leng-1), dtype=float)
    vel_y= np.zeros((leng-1), dtype=float)
#    speed_inPixels= np.zeros((leng-1,1), dtype=float)
    speed= np.zeros((leng-1), dtype=float)
    speed_ave= np.zeros((leng-1), dtype=float)
    time= np.zeros((leng), dtype=float)
    time[0]=0.0
    
    for i in range(1,leng-1):
        disp_x[i]= centroid_x[i] - centroid_x[i-1] 
        disp_y[i]= centroid_y[i] - centroid_y[i-1] 
        
        dispCutOff=100.0
        if abs(disp_x[i]) > dispCutOff:
            print('disp_x[i] > %f: disp_x[%d]=%e' %(dispCutOff, i,disp_x[i]))
            disp_x[i]=0
        
        if abs(disp_y[i]) > dispCutOff:
            print('disp_y[i] > %f: disp_y[%d]=%e' %(dispCutOff, i,disp_y[i]))
            disp_y[i]=0
                    
        if constantFrequency:
            fps=fileList[i].fps+0.0
            deltaT=1.0/fps
            time[i]=time[i-1]+deltaT
            vel_x[i] = (disp_x[i]/pPmm)/deltaT
            vel_y[i] = (disp_y[i]/pPmm)/deltaT            
        else:
            deltaT=((fileList[i].timestamp1-fileList[i-1].timestamp1)/1000.0)
            time[i]=time[i-1]+deltaT
            vel_x[i] = (disp_x[i]/pPmm)/deltaT
            vel_y[i] = (disp_y[i]/pPmm)/deltaT
        
        velocityCutOff=100.0
        if abs(vel_x[i]) > velocityCutOff:
            print('vel_x[i] > %f: vel_x[%d]=%e' %(velocityCutOff, i,vel_x[i]))
            vel_x[i]=0
        
        if abs(vel_y[i]) > velocityCutOff:
            print('vel_y[i] > %f: vel_y[%d]=%e' %(velocityCutOff, i,vel_y[i]))
            vel_y[i]=0
    
    #Running average
    aveWindow=4
    speed = np.sqrt( np.power( vel_x ,2) + np.power(vel_y ,2) )
    speed_ave = np.sqrt( np.power( runningMean(vel_x, aveWindow) ,2) + np.power(runningMean(vel_y, aveWindow) ,2) )
    speed_ave =  runningMean(speed_ave, aveWindow)  
    speed_ave =  runningMean(speed_ave, aveWindow)   
    
    #identify different regions
    dx = gradient(speed_ave, h=1/60)
    zx=np.arange(len(dx))
    
    plt.figure(1)
    plt.plot(zx, dx, 'oc',label='Gradient Speed', markersize=5)
    plt.title("dx"+" " + fileID)
    plt.ylabel("dx")
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_GradientSpeed_Graph.jpg")
    
    
    #Write results to file    
    fo = open(path+fileID+'_Results.txt', "w")
    fo.write("# \t Ver Dist \t Hor Dist \t Perimeter \t Area \t centroid_x \t centroid_y \t width[i] \t heigth[i] \t D \t angle \t time (s) \tvel_x (mm/s)\t vel_y (mm/s)\t  \n\n\n")
    for i in range(leng) :
        if i==0:
            fo.write("%d \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \n" %(i, verticalDistance[i], horizontalDistance[i], perimeter[i], area[i], centroid_x[i], centroid_y[i], width[i], heigth[i], D[i], angle[i],time[i]))
        else:
            fo.write("%d \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \t %.4f \n" %(i, verticalDistance[i], horizontalDistance[i], perimeter[i], area[i], centroid_x[i], centroid_y[i], width[i], heigth[i], D[i], angle[i],time[i], vel_x[i-1], vel_y[i-1]))
    fo.close()
    
    fo = open(path+fileID+'_Failed.txt', "w")
    fo.write('\bFailed to follow proper protocoll %d times. The indexes on which this occured are: \n' %fullMontyFailed)
    for s in failedIndexes :
        fo.write('\t %d' %s)
    fo.close()

    #plot all variables
                
    #Remove crazy entries
                
                
                
    x=np.arange(leng)
    
    #normalize by initial length
    verticalDistance=verticalDistance/(d0)
    horizontalDistance=horizontalDistance/(d0)
    
    #plost results
    plt.figure(2)
    plt.plot(x, verticalDistance, 'oc',label='Vertical', markersize=5)
    plt.plot(x, horizontalDistance, 'sb',label='Horizontal', markersize=5)
    plt.title("Extend of Capsule"+" " + fileID)
    plt.xlabel("Picture # ")
    plt.ylabel("Extend [d0]")
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_Extend_Graph.jpg")
    
    area=area/(np.power(pPmm,2))
    area=area/A0
    
    plt.figure(3)
    plt.plot(x, area, 'or',label='Area', markersize=5)
    plt.title("Area"+" " + fileID)
    plt.xlabel("Picture # ")
    plt.ylabel("Area / Initial Area")
    plt.savefig(path+fileID+"_Area_Graph.jpg")
    
    perimeter=perimeter/pPmm
    perimeter=perimeter/p0
    
    plt.figure(4)
    plt.plot(x, perimeter, 'sb',label='Perimeter', markersize=5)
    plt.title("Perimeter"+" " + fileID)
    plt.xlabel("Picture # ")
    plt.ylabel("Perimeter/ Initial Perimeter")
    plt.savefig(path+fileID+"_Perimeter_Graph.jpg")
    
    print("Max Values for vertical extend, perimeter and area \t"+ str(np.max(verticalDistance))+"\t"+ str(np.max(perimeter))+"\t"+ str(np.max(area)))
    
    r=np.zeros(3)
    r[0]=np.max(verticalDistance)
    r[1]=np.max(perimeter)
    r[2]=np.max(area)    
    
    #plotVelocity graphs
    # evaluate speed
    
    plt.figure(5)
    plt.plot(centroid_x,centroid_y, 'sb',label='Centroid Position', markersize=5)
    plt.title("Centroid Position"+" " + fileID)
    plt.xlabel("Z Position [pixels]")
    plt.ylabel("Y Position [pixels]")
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_CentroidPosition_Graph.jpg")        

    
    x1=np.arange(leng-1)
        
    plt.figure(6)
    plt.plot(x1, vel_x, 'sb',label='v_x', markersize=5)
    plt.plot(x1, vel_y, 'or',label='v_y', markersize=5)
    plt.title("Velocity"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Velocity [mm/s]")
    plt.legend()
    plt.savefig(path+fileID+"_Velocity_Graph.jpg")
    
    plt.figure(7)
    plt.plot(x1, disp_x, 'sb',label='disp_x', markersize=5)
    plt.plot(x1, disp_y, 'or',label='disp_y', markersize=5)
    plt.title("Displacment"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Displacment [pixels]")
    plt.legend()
    plt.savefig(path+fileID+"_Displacment_Graph.jpg")
    
    plt.figure(8)
    plt.plot(x, time, 'sb',label='Time (s)', markersize=5)
    plt.title("Time [s]"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Time [s] ")
    plt.legend()
    plt.savefig(path+fileID+"_Time_Graph.jpg")
    
    plt.figure(9)
    plt.plot(x1, speed_ave, 'sb',label='Speed Averaged', markersize=5)
    plt.title("SpeedAveraged"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Speed[mm/s]")
    plt.legend()
    plt.savefig(path+fileID+"_SpeedAve_Graph.jpg")
    
    plt.figure(10)
    plt.plot(x1, runningMean(disp_x, 6), 'sb',label='running mean disp_x', markersize=5)
    plt.plot(x1, runningMean(disp_y, 6), 'or',label='running mean disp_y', markersize=5)
    plt.title("Displacment Runnung Average"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Displacment [pixels]")
    plt.legend()
    plt.savefig(path+fileID+"_DisplacmentRunnungAverage_Graph.jpg")
    
    plt.figure(9)
    plt.plot(x1, speed, 'or',label='Speed', markersize=5)
    plt.title("Speed"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Speed[mm/s]")
    plt.legend()
    plt.savefig(path+fileID+"_Speed_Graph.jpg")
    
    plt.figure(11)
    plt.plot(x,centroid_x, 'sb',label='Centroid x ', markersize=5)
    plt.plot(x,centroid_y, 'or',label='Centroid y ', markersize=5)
    plt.title("Centroid Position"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Centroid Position [pixels]")
    plt.legend()
    plt.savefig(path+fileID+"_CentroidPosition2_Graph.jpg") 
    
    plt.figure(12)
    plt.plot(x,width, 'sb',label='Width ', markersize=5)
    plt.plot(x,heigth, 'or',label='Heigth', markersize=5)
    plt.title("Size of Particle"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Width / Hiegth [pixels]")
#    plt.ylim((70,82))
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_width-heigth_Graph.jpg") 
    
    plt.figure(13)
    plt.plot(x,D, 'sb',label='Taylor Deformation Parameter ', markersize=5)
    plt.title("Taylor Deformation Parameter"+" " + fileID)
    plt.xlabel("Taylor Deformation Parameter")
    plt.ylabel("Width / Hiegth [pixels]")
#    plt.ylim((70,82))
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_Talyor-Deformation_Graph.jpg")
    
    print('\b Failed to follow proper protocoll %d times out of %d images.' %(fullMontyFailed,leng))
        
    return r

    
        
    
        
    
        
    
def test(path, d0, pPmm, constantFrequency=False, rotate=0.0, plot=False, threshold=150, printDebugInfo=False, equialize=False):
    """Goes though all the pictures in directory, thresholds them and finds 
    several measurments for the resulting object, which should be a capsule if 
    the threshold has been chossen correctly
    """
    fileID=find_batchName(path);
    ERROR_CONST=-1
    
    #initial 2D projected area
    A0=np.pi*np.power(d0/2,2)
    #initial perimeter
    p0=2.0*np.pi*(d0/2)

    #close all graphs
    plt.close("all")
    
    #'forShow is a boolean variable that governs whether plot is displayed 
    #during program run. 
    forShow=False    
    
    #This sets the threshold what is counted as black in grayscale image and 
    #should be between 0-255
    #A threshold of 110 worked robustly over a wide range
#    threshold=150
    
    #get sorted list of filenames
    if constantFrequency:
        fileList, leng =sortPhotosPCO(path)
        print('Using sortPhotosPCO')
    else:
        fileList, leng =sortPhotos2(path)
        print('Using sortPhotos2')
    print('leng = %d' %leng)
    #Initializing variable to hold the area, perimeter and vertical distance
    #(y-direction) for each image
    area = np.zeros((leng), dtype=float)
    perimeter = np.zeros((leng), dtype=float)
    verticalDistance = np.zeros((leng), dtype=float)
    horizontalDistance = np.zeros((leng,1), dtype=float)
    width = np.zeros((leng), dtype=float)
    heigth = np.zeros((leng), dtype=float)
    centroid_x = np.zeros((leng), dtype=float)
    centroid_y = np.zeros((leng), dtype=float)
    D = np.zeros((leng), dtype=float)
    angle = np.zeros((leng), dtype=float)
    velx = np.zeros((leng), dtype=float)
    vely = np.zeros((leng), dtype=float)
    
    #counter of images
    counterL=-1
    
    #border that is added to image 
    borderSize=10
    
    fullMontyFailed=0
    failedIndexes=[]
   
    #Iterating over all pictures
    for i in range(leng):
        plt.close('all')
        gc.collect()
        counterL=counterL+1
        
        #print info every 10th picture
        if i%10 == 0:
            print("Current frame " + str(i) + "\t and counter is on " +  str(counterL))# + " and memory used is: ")
            
        #read image
        readPath=path+fileList[i].fn
#        print("readPath: %s" %readPath)
        img =cv2.imread(readPath,0)
        
        if rotate != 0:
            img=rotateImage(img, rotate)
            
        if equialize:
#            img = cv2.equalizeHist(img) 
            kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            close = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel1)
            div = np.float32(img)/(close)
            img = np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX))

        if(plot):
            plt.figure(num='Initial', facecolor='w', edgecolor='k', figsize=(24, 8), dpi=600)
            a1=plt.subplot(131)
            plt.imshow(img, cmap='Greys')

        #add a border of black pixels around image in case capsule touches edge    
        img=cv2.copyMakeBorder(img,borderSize,borderSize,borderSize,borderSize,
                               cv2.BORDER_CONSTANT,value=(255, 255, 255))    
        
        #Get size of image
        yImg,xImg = img.shape
        
        #Add a rectanlge over areas of image not of intrest, to prevent 
        #interference from these areas        
        
        paddingOffset=5        
        
        topCropLevel=25+borderSize #where to cut the top of the image
#        topCropLevel=66+borderSize #where to cut the top of the image
        
#        dex=125  # daugther channel bottom edge        
        dex=114  # daugther channel bottom edge    
        leftEdge=559
        rightEdge=733
        
#        #PCO SETUp
#        cv2.rectangle(img, (0, dex+borderSize+paddingOffset), (540+borderSize-paddingOffset, yImg), 255,
#                      thickness=-1)   
#        cv2.rectangle(img, (725+borderSize+paddingOffset, dex+borderSize+paddingOffset), (xImg, yImg),  255,
#                      thickness=-1)
#        #Block out timestamp from pco camera
#        cv2.rectangle(img, (0+borderSize, 0+borderSize), (xImg+borderSize, topCropLevel), 255,
#                      thickness=-1)
                      
        #PCO SETUp
        cv2.rectangle(img, (0, dex+borderSize+paddingOffset), (leftEdge+borderSize-paddingOffset, yImg), 255,
                      thickness=-1)   
        cv2.rectangle(img, (rightEdge+borderSize+paddingOffset, dex+borderSize+paddingOffset), (xImg, yImg),  255,
                      thickness=-1)
        #Block out timestamp from pco camera
        cv2.rectangle(img, (0+borderSize, 0+borderSize), (xImg+borderSize, topCropLevel), 255,thickness=-1)


def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    
    From: http://wiki.scipy.org/Cookbook/SignalSmooth
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y