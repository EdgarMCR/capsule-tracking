# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 11:49:32 2015

@author: mbbxkeh2
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
#Minimal Example

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
    
    
    
if __name__ == '__main__':
        path=os.getcwd()
        #assuming Windows path
        path=path+'\\Images'
        
        fileList=dir_list2(path)
        fileType='.png'
        lowerThreshold=80
        
        loopCounter=-1
        
        for fileName in fileList:
            loopCounter += 1
            #read image
            if (fileName[-4:len(fileName)] == fileType):
                img =cv2.imread(fileName,0)
                
#            blur = cv2.GaussianBlur(img,(5,5),0)
            edges = cv2.Canny(img,lowerThreshold,lowerThreshold*3)
#            edges0p8 = cv2.Canny(img,lowerThreshold*0.8,lowerThreshold*2*0.8)
#            edges0p6 = cv2.Canny(img,lowerThreshold*0.6,lowerThreshold*2*0.6)
#            edges1p2 = cv2.Canny(img,lowerThreshold*1.2,lowerThreshold*2*1.2)
#            
#            
#            f=plt.figure()
#            plt.subplot(221),plt.imshow(edges,cmap = 'gray')
#            plt.title('Original Edge %d' %lowerThreshold), plt.xticks([]), plt.yticks([])
#            plt.subplot(222),plt.imshow(edges0p8,cmap = 'gray')
#            plt.title('edges0p8'), plt.xticks([]), plt.yticks([])
#            plt.subplot(223),plt.imshow(edges0p6,cmap = 'gray')
#            plt.title('edges0p6'), plt.xticks([]), plt.yticks([])
#            plt.subplot(224),plt.imshow(edges1p2,cmap = 'gray')
#            plt.title('edges1p2'), plt.xticks([]), plt.yticks([])
#            plt.show()
#            filesavepath='ThresholdEdge_'+str(loopCounter)+'.png'
#            plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
#            plt.close(f)  
#            
            
            
            dispedges=edges.copy()
            
            kernel = np.ones((3,3),np.uint8)            
            edges33 = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            kernel = np.ones((5,5),np.uint8)            
            edges55 = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            kernel = np.ones((7,7),np.uint8)            
            edges77 = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

#            edges = cv2.dilate(edges,kernel,iterations = 1)
#            edges=cv2.erode(edges,element)
            
            f1=plt.figure()
            plt.subplot(221),plt.imshow(edges,cmap = 'gray')
            plt.title('Original Edge'), plt.xticks([]), plt.yticks([])
            plt.subplot(222),plt.imshow(edges33,cmap = 'gray')
            plt.title('3x3 Closing'), plt.xticks([]), plt.yticks([])
            plt.subplot(223),plt.imshow(edges55,cmap = 'gray')
            plt.title('5x5 Closing'), plt.xticks([]), plt.yticks([])
            plt.subplot(224),plt.imshow(edges77,cmap = 'gray')
            plt.title('7x7 Closing'), plt.xticks([]), plt.yticks([])
            plt.show()
            filesavepath='MorphologicalEdge_'+str(loopCounter)+'.png'
            plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
            plt.close(f1)  
            

            contours, hierarchy = cv2.findContours(edges,cv2.cv.CV_RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_NONE) #CV_RETR_EXTERNAL or cv2.cv.CV_RETR_LIST ||  cv2.cv.CV_CHAIN_APPROX_NONE or cv2.cv.CV_CHAIN_APPROX_SIMPLE
            contours33, hierarchy33 = cv2.findContours(edges33,cv2.cv.CV_RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_NONE)
            #Select longest contour as this should be the capsule
            lengthC=0
            ID=-1
            idCounter=-1
            for x in contours:
                idCounter=idCounter+1 
                if len(x) > lengthC:
                    lengthC=len(x)
                    ID=idCounter
            
            if ID != -1:
                    cnt = contours[ID]
                    cntFull=cnt.copy()
                    
                    #approximate the contour, where epsilon is the distance to 
                    #the original contour
                    cnt = cv2.approxPolyDP(cnt, epsilon=1, closed=True)
                    
                    #add the first point as the last point, to ensure it is closed
                    lenCnt=len(cnt)
                    cnt= np.append(cnt, [[cnt[0][0][0], cnt[0][0][1]]]) #[[cnt[0][0][0],cnt[0][0][1]]])
                    cnt=np.reshape(cnt, (lenCnt+1,1, 2))
                    
                    lenCntFull=len(cntFull)
                    cntFull= np.append(cntFull, [[cntFull[0][0][0], cntFull[0][0][1]]]) #[[cnt[0][0][0],cnt[0][0][1]]])
                    cntFull=np.reshape(cntFull, (lenCntFull+1,1, 2))
                    
                    M = cv2.moments(cnt)
                    MFull = cv2.moments(cntFull)
                    print('%d \tArea = %.2f \t Area of full contour= %.2f' %(loopCounter, M['m00'], MFull['m00']))
                    
                    
                    #==========================================================
                    #Saving images of contour to file
                    #==========================================================
                    #find bounding rectangle of countour
                    x,y,w,h = cv2.boundingRect(cnt)
                    cv2.rectangle(dispedges,(x,y),(x+w,y+h),(255,255,255),2) 

                    
                    f2=plt.figure()
                    plt.subplot(121),plt.imshow(img,cmap = 'gray')
                    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
                    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
                    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
                    
                    plt.show()
                    filesavepath='ImageAndContour_'+str(loopCounter)+'.png'
                    plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
                    plt.close(f2)                    
                    
                    f4=plt.figure()
                    xPlot=[]; yPlot=[]
                    xfPlot=[]; yfPlot=[]
                    cntFull
                    for gg in range(len(cnt)):
                        xPlot.append(cnt[gg][0][0])
                        yPlot.append(cnt[gg][0][1])
                    for hh in range(len(cntFull)):
                        xfPlot.append(cntFull[hh][0][0])
                        yfPlot.append(cntFull[hh][0][1])
                    plt.plot(xfPlot, yfPlot, 's', color='#1b9e77', label='Full Contour', markersize=2)
                    plt.plot(xPlot, yPlot, 'o', color='#7570b3', label='approxPolyDP Contour' ,  markersize=7)
            
                    plt.legend(loc=2, fontsize=6)
                    plt.show()
                    filesavepath='FoundContours_'+str(loopCounter)+'.png'
                    plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
                    plt.close(f4)
                    
                    f3=plt.figure()
                    plt.imshow(img,cmap = 'gray')
                    plt.plot(xfPlot, yfPlot, 'or', label='Full Contour', markersize=3)
                    plt.title('Original Image'), plt.xticks([]), plt.yticks([])

                    
                    plt.show()
                    filesavepath='ImageWithContour_'+str(loopCounter)+'.png'
                    plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
                    plt.close(f3)
                    
                    cv2.drawContours(img, contours,ID,(255,255,255),1)
                    cv2.imwrite('ImageWContour_'+str(loopCounter)+'.png', img)
        
                    
                    