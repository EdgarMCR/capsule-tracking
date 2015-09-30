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

def createRotatedRectangle(angle):
    blank_image = np.zeros((200,200), np.uint8)

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
                cv2.imshow('Image %d' %loopCounter,img)
                
#            ret, thresh = cv2.threshold(img,120,255,cv2.THRESH_BINARY)
            edges = cv2.Canny(img,80,160)
            cv2.imshow('Edge %d' %loopCounter,edges)
            
            contours, hierarchy = cv2.findContours(edges,cv2.cv.CV_RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_NONE) #CV_RETR_EXTERNAL or cv2.cv.CV_RETR_LIST ||  cv2.cv.CV_CHAIN_APPROX_NONE or cv2.cv.CV_CHAIN_APPROX_SIMPLE

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
                x,y,w,h = cv2.boundingRect(cnt)      
                centre, sides, angle=cv2.minAreaRect(cnt)
                xc, yc = centre
                wr, hr = sides
                
                print('Image %d: x,y,w,h = (%d, %d, %d, %d), angle is %.1f \t %d, %d, %d, %d' %(loopCounter, x, y, w, h, angle, x1, x2, y1, y2))
#                print(reslt)
                
                f1=plt.figure()
                plt.imshow(img,cmap = 'gray')
                
                #plot bounding rectangle
                plt.plot([x, x+w],[y, y], '-r')
                plt.plot([x, x+w],[y+h, y+h], '-r')
                plt.plot([x, x],[y, y+h], '-r')
                plt.plot([x+w, x+w],[y, y+h], '-r')
                
                #plot rotate rectangle
                plt.plot([x1, x2],[y1, y1], '-b')
                plt.plot([x1, x2],[y2, y2], '-b')
                plt.plot([x1, x1],[y1, y2], '-b')
                plt.plot([x2, x2],[y1, y2], '-b')

                
                plt.show()
                if platform.system() == 'Linux':
                    savepath=path+'Check\\'
                elif platform.system() == 'Windows': 
                    savepath=path+'Check/'
                if not os.path.exists(savepath): os.makedirs(savepath)
                filesavepath=savepath+'Plot_'+str(loopCounter)+'.png'
                plt.savefig(filesavepath, dpi=300,bbox_inches='tight')
                plt.close(f1)                
                
                
                
#                cv2.drawContours(img, contours,ID,(0,255,0),4)
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),2)  
                cv2.imwrite('ImageWContour_'+str(loopCounter)+'.png', img)
                    
        
                    
                    