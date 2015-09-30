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

 

def wholeRun(directory, rotateImages=0.0, threshold=150):
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
                find_max_extend(directory+f+'/', constantFrequency=True, rotate=rotateImages, threshold=threshold)
            elif platform.system() == 'Windows': 
                find_max_extend(directory+f+'\\', constantFrequency=True, rotate=rotateImages, threshold=threshold)
            
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
    sperator='_' #'-'

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
                    fileList.append(dirfile)
        '''
        elif os.path.isdir(dirfile):
            print "Accessing directory:", dirfile
            fileList += dir_list2(dirfile, *args)
        '''
    return fileList
    
def runningMean(x, N):
    y = np.zeros((len(x),))
    
    assert len(x) > 2*N
    
    for ctr in range(N):
        y[ctr] = np.sum(x[ctr:(ctr+N)])
    
    for ctr in range(N,len(x)-N):
        n=round(N/2)
        y[ctr] = np.sum(x[ctr-n:(ctr+n)])
        
    for ctr in range(len(x)-N, len(x)):
        y[ctr] = np.sum(x[ctr-N:(ctr)])
        
    return y/N
    
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
        reslt="notfound"
        
#    print(reslt)    
#    print('Ended find_batchName(path)')
    return reslt
    
def gradient(x, h=1/64):
    dx = np.zeros((len(x)-4,1))
    for i in range(3,len(x)-2):
        dx[i-2] = (1/12*x[i-2]-2/3*x[i-1] + 2/3*x[i+1] - 1/12 * x[i+2])/h
    return dx
    
def rotateImage(image, angle):
    row,col = image.shape
    center=tuple(np.array([row,col])/2)
    rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
    new_image = cv2.warpAffine(image, rot_mat, (col,row))
    return new_image
    
def findContoursByThresholding(img, threshold, plot=False, counter=0, path=None):
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

    #Select longest contour as this should be the capsule
    lengthC=0
    ID=-1
    idCounter=-1
    for x in contours:
        idCounter=idCounter+1
        if len(x) > lengthC:
            lengthC=len(x)
            ID=idCounter
    
    
    #if longest contour was found, then ID is the index of it
    if ID != -1:
        cnt = contours[ID]
        #find bounding rectangle of countour
        x,y,w,h = cv2.boundingRect(cnt)
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
    else:
        cnt=None
        x,y,w,h = -1, -1, -1 ,-1
    
    return cnt, th, x,y,w,h
    
def print_polygon(polygon):
    print('Started print_polygon')
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
    
def findContour(img, lowerThreshold, ratio, closing=False, kernelsize=3, plot=False, path=None, printDebugInfo=False):
    #Canny edge detection
    edges = cv2.Canny(img,lowerThreshold,lowerThreshold*ratio) 
    
    if plot:
        cv2.imwrite(path, edges)
    
    if edges == None:
        if printDebugInfo:
            print('\tin findContour: None from Canny edge detector')
        return None, -1, -1, -1, -1
        
    
    if  closing:
        #perform a morphplogical closing, to remove minor holes in the object
        kernel = np.ones((kernelsize,kernelsize),np.uint8)            
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        if edges == None:
            if printDebugInfo:
                print('\tin findContour: None from morphologyEx')
            return None, -1, -1, -1, -1
    
    #find Contours
    contours, hierarchy = cv2.findContours(edges,cv2.cv.CV_RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_NONE) #cv2.cv.CV_RETR_LIST || cv2.cv.CV_CHAIN_APPROX_NONE or cv2.cv.CV_CHAIN_APPROX_SIMPLE
    
    #select best contour
    cnt, x, y, w, h = selectContour(contours)
    
    return cnt, x, y, w, h
    
def tryAllParametersForContours(img, lowerThreshold, expectedArea, plot=False, path=None, printDebugInfo=False):
    lowerThresholdList=[  lowerThreshold, lowerThreshold*0.95, lowerThreshold*1.05, lowerThreshold*0.9, lowerThreshold*1.1, lowerThreshold*0.8, lowerThreshold*1.2,  lowerThreshold*0.7, lowerThreshold*1.3, lowerThreshold*0.6, lowerThreshold*1.4]
    ratioList=[1.5, 2, 2.5, 3]
    kernelSize=[-1,3,5]
    for lt in lowerThresholdList:
        for r in ratioList:
            for k in kernelSize:
                if k == -1:
                    cnt, x, y, w, h = findContour(img, lt, r, closing=False, kernelsize=3, plot=plot, path=path, printDebugInfo=printDebugInfo)
                else:
                    cnt, x, y, w, h = findContour(img, lt, r, closing=True, kernelsize=k, plot=plot, path=path, printDebugInfo=printDebugInfo)
                #check area
                if cnt != None:
                    M = cv2.moments(cnt)
                    if M['m00'] > 0.5*expectedArea and M['m00'] < 1.5*expectedArea:
                        print('Winning parameter combination: threshold = %d ratio= %.1f kernel=%d' %(lt, r, k))
                        return cnt, x, y, w, h
                    
    #Still no contour found, probably no capsule in image
    if printDebugInfo:
        print('Returnng None from tryAllParametersForContours')
    return None, -1, -1, -1, -1
    

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
            print('cnt is None after first contour')
            
    if expectedArea != -1:
        if plot:
            if platform.system() == 'Linux':
                savepath=path+'Check\\Edges_'+str(i)+'.jpg'
            elif platform.system() == 'Windows': 
                savepath=path+'Check/Edges_'+str(i)+'.jpg'
        else:
            savepath=None
            
        #Check area
        if cnt != None:
            M = cv2.moments(cnt)
            if M['m00'] < 0.2*expectedArea or M['m00'] > 1.8*expectedArea:
                if printDebugInfo:
                    print('Contour Area is too small: %.2f against expected Area = %.2f' %(M['m00'], expectedArea))
                cnt, x, y, w, h = tryAllParametersForContours(img, lowerThreshold, expectedArea, plot=plot, path=savepath, printDebugInfo=printDebugInfo)
        else:
            cnt, x, y, w, h = tryAllParametersForContours(img, lowerThreshold, expectedArea, plot=plot, path=savepath, printDebugInfo=printDebugInfo)
             
    if plot:
        cntCopy=cnt
        img2=img.copy()
        
        xPlot=[]; yPlot=[]
        if cnt != None:  
            M = cv2.moments(cnt)
            centroid_x = float(M['m10']/M['m00'])
            centroid_y = float(M['m01']/M['m00'])    

            xTest, yTest = centroid_for_polygon(cntCopy)
            area = area_for_polygon(cntCopy)
            
            if printDebugInfo:
                print('doing test - m00 = %.2f m10 = %.2f m01 = %.2f' %(M['m00'],M['m10'],M['m01'])),
                print(' x,y = (%2f, %2f) \t x,y = (%2f, %2f) \t difference = (%2f, %2f) \t area = %.2f' %(centroid_x, centroid_y, xTest, yTest, centroid_x-xTest, centroid_y - yTest, area))

            cv2.circle(img2,(int(centroid_x),int(centroid_y)), 3, (255,255,255), 2)
            

            for gg in range(len(cntCopy)):
                xPlot.append(cntCopy[gg][0][0])
                yPlot.append(cntCopy[gg][0][1])
        
        f2=plt.figure()
        plt.subplot(121),plt.imshow(img,cmap = 'gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        
        cv2.rectangle(img2,(x,y),(x+w,y+h),(255,255,255),2) 
        
        plt.subplot(122),plt.imshow(img2,cmap = 'gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        
        plt.show()
        if platform.system() == 'Linux':
            savepath=path+'Check\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+'Canny2_'+str(i)+'.png'
        plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
        plt.close(f2)
        
#        f4=plt.figure()

#        plt.plot(xPlot, yPlot, 'o', color='#7570b3',  markersize=2)
#
#        
#        plt.show()
#        if platform.system() == 'Linux':
#            savepath=path+'Check\\'
#        elif platform.system() == 'Windows': 
#            savepath=path+'Check/'
#        if not os.path.exists(savepath): os.makedirs(savepath)
#        filesavepath=savepath+'Canny4_'+str(i)+'.png'
#        plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
#        plt.close(f4)
        
        f3=plt.figure()
        plt.imshow(img,cmap = 'gray')
        plt.plot(xPlot, yPlot, 'or', label='Full Contour', markersize=1)
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])

        
        plt.show()
        if platform.system() == 'Linux':
            savepath=path+'Check\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+'ImageWithContour_'+str(i)+'.png'
        plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
        plt.close(f3)

    
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
        xPlot=[]; yPlot=[]
        if cnt != None:  
            for gg in range(len(cnt)):
                xPlot.append(cnt[gg][0][0])
                yPlot.append(cnt[gg][0][1])
        
        f3=plt.figure()
        plt.imshow(img,cmap = 'gray')
        plt.plot(xPlot, yPlot, 'or', label='Full Contour', markersize=1)
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])

        
        plt.show()
        if platform.system() == 'Linux':
            savepath=path+'Check\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/'
        if not os.path.exists(savepath): os.makedirs(savepath)
        filesavepath=savepath+'ImageWithContour_'+str(i)+'.png'
        plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
        plt.close(f3)
        
        cv2.imwrite(savepath+'ImageCropped_'+str(i)+'.png', imgCropped)

    return imgCropped, cnt, offsetX+offsetX2,offsetY+offsetY2,w,h
    


def find_max_extend(path, d0, constantFrequency=False, rotate=0.0, plot=False, threshold=150, printDebugInfo=False):
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
    
    #pixels per milimeter in the image
    pPmm=22.3

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
    area = np.zeros((leng,1), dtype=float)
    perimeter = np.zeros((leng,1), dtype=float)
    verticalDistance = np.zeros((leng,1), dtype=float)
    horizontalDistance = np.zeros((leng,1), dtype=float)
    width = np.zeros((leng,1), dtype=float)
    heigth = np.zeros((leng,1), dtype=float)
    centroid_x = np.zeros((leng,1), dtype=float)
    centroid_y = np.zeros((leng,1), dtype=float)
    D = np.zeros((leng,1), dtype=float)
    angle = np.zeros((leng,1), dtype=float)
    velx = np.zeros((leng,1), dtype=float)
    vely = np.zeros((leng,1), dtype=float)
    
    #counter of images
    counterL=-1
    
    #border that is added to image 
    borderSize=10
    
    fullMontyFailed=0
   
    #Iterating over all pictures
    for i in range(leng):
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

        #add a border of black pixels around image in case capsule touches edge    
        img=cv2.copyMakeBorder(img,borderSize,borderSize,borderSize,borderSize,
                               cv2.BORDER_CONSTANT,value=(255, 255, 255))    
        
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
        
        cnt, thresh, x,y,w,h = findContoursByThresholding(img, threshold, plot=plot, counter=i, path=path)
        
        if printDebugInfo:
            print('\nPosition from Thresholding: x,y,w,h = (%d, %d, %d, %d) \t cnt[0][0][0] = %.2f' %(x,y,w,h, cnt[0][0][0]))
            
        padding=20
#        top=y-padding
#        if top <  topCropLevel:
#            top= topCropLevel
        
        imgForCanny = img[y-padding:y+h+padding, x-padding:x+w+padding]
            
        cntCanny, xCanny,yCanny,wCanny,hCanny = cannyEdgeFind(imgForCanny, threshold/3*2, offsetX=x-padding, offsetY=y-padding, expectedArea=A0*np.power(pPmm,2), plot=plot, printDebugInfo=printDebugInfo, i=i, path=path)
        if printDebugInfo:
            if cntCanny == None:
                print('cntCanny = ' +str(cntCanny)),
            else:
                print('cntCanny[0][0][0] = %.2f' %cntCanny[0][0][0]),

        contourFound=False
        
        if cntCanny != None:
            contourFound=True
        elif cntCanny == None and cnt != None:
            fullMontyFailed +=1
            if printDebugInfo:
                print('Using Thresholding Image to startCanny')
            
            imgForCanny2 = thresh[top:y+h+padding, x-padding:x+w+padding]                
            cntCanny, xCanny,yCanny,wCanny,hCanny = cannyEdgeFind(imgForCanny2, threshold/3*2, offsetX=x-padding, offsetY=y-padding, expectedArea=A0*np.power(pPmm,2), plot=plot, printDebugInfo=printDebugInfo, i=i, path=path)
            
            if cntCanny == None:
                if printDebugInfo:
                    print('Using Thresholding')
                cntCanny, xCanny,yCanny,wCanny,hCanny =  cnt,  x,y,w,h
                contourFound=True
            else:
                contourFound=True
        else:
            fullMontyFailed +=1
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
                    centroid_x[counterL] = xCanny + int(M['m10']/M['m00'])
                    centroid_y[counterL] = yCanny + int(M['m01']/M['m00'])
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
                ax3 = fig.add_subplot(111)
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
    
    disp_x  = np.zeros((leng-1,1), dtype=float)
    disp_y = np.zeros((leng-1,1), dtype=float)
    vel_x = np.zeros((leng-1,1), dtype=float)
    vel_y= np.zeros((leng-1,1), dtype=float)
#    speed_inPixels= np.zeros((leng-1,1), dtype=float)
    speed= np.zeros((leng-1,1), dtype=float)
    speed_ave= np.zeros((leng-1,1), dtype=float)
    time= np.zeros((leng,1), dtype=float)
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
    aveWindow=2
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
    
    print('\bFailed to follow proper protocoll %d times.' %fullMontyFailed)
        
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

        if cntCanny != None:  
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
    printDebugInfo=False
    
    if printDebugInfo:
        print('type(img) = ' +str(type(img))),
    
    cnt, x, y, w, h = findContour(img, lowerThreshold, 2, closing=False, kernelsize=3)
    
    if plot:
        print('%d \t (w,h) = (%d, %d)' %(i, w, h))

    if cnt != None:
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
             
    if plot:
        img2=img.copy()
        cv2.rectangle(img2,(x,y),(x+w,y+h),(255,255,255),1)     
        
        if platform.system() == 'Linux':
            savepath=path+'Check\\'
        elif platform.system() == 'Windows': 
            savepath=path+'Check/'
        if not os.path.exists(savepath): os.makedirs(savepath)
            
        cv2.imwrite(savepath+'ImageCropped_'+str(i)+'.png', img2)   
        cv2.imwrite(savepath+'WorkingImage_'+str(i)+'.png', workImg)
        cv2.imwrite(savepath+'WorkingImageWContour_'+str(i)+'.png', workImg2)

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

def testThresholds(path, rotate=0, thresholds=[30, 60, 90, 120, 150, 180]):
    
    fileID=find_batchName(path);
    ERROR_CONST=-1
    
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
        plt.imshow(img3, cmap = 'gray')
        f2.add_subplot(236)
        plt.imshow(img4, cmap = 'gray')
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
    
    
    

    
    
