# -*- coding: utf-8 -*-
"""
Draw a cirlce on a pixel grid to get upper bound on pixilation error

Created on Mon Sep 14 21:19:30 2015

@author: magda
"""

from __future__ import absolute_import, division, print_function
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

import track_capsule_TJ_v0p12 as tr

def drawCircle(offset = 0.0, pixelsPerDiameter=1):
#    size = ( w, h,channels) = (2*pixelsPerDiameter+4, pixelsPerDiameter +4, 1)
    h, w = int(2*pixelsPerDiameter+10), int(pixelsPerDiameter +4)
#    print('w, h = (%d, %d) ' %(w, h))
    img = np.zeros((w,h), np.uint8)
    
    #Inefficient method, just walk through every pixel and set relevant ones to zero
    centre_x = pixelsPerDiameter/2.0 +1.5 
    centre_y = pixelsPerDiameter/2.0 +1.5 + offset
    for x in range(w):
        for y in range(h):
            r = np.sqrt((centre_x - (x+0.5))**2 + (centre_y - (y+0.5))**2)
            if r <= pixelsPerDiameter/2.0:
                img[x,y] = 254
    
    return img, centre_y, centre_x
    

#cv2.startWindowThread()
#cv2.namedWindow("preview")
#cv2.imshow('preview', img)

def findCentroidOpenCV(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    centroid_x, centroid_y = -1, -1
    
    if len(contours) > 0:
        M = cv2.moments(contours[0])
        if M['m00'] == 0 or M['m10'] == 0 or M['m01'] == 0:
            print('%f, %f, %f' %(M['m00'], M['m10'], M['m01']))
        else:
            centroid_x = float(M['m10']/M['m00'])
            centroid_y = float(M['m01']/M['m00'])
    return centroid_x, centroid_y
    

def runTest(diameter=10.0, maxOffset=21, increment=10.0):
    c_x = []; c_y = []; fc_x=[]; fc_y= []; offset=[]
    for ii in range(maxOffset):
        offset.append(ii/increment)
        img, centre_x, centre_y = drawCircle(offset = offset[ii], pixelsPerDiameter=diameter)
        
        path =''
        savepath1=path +'Pixelation'
        if not os.path.exists(savepath1): os.makedirs(savepath1)
        pathFile2=os.path.join(path, 'Pixelation', 'Size_%d_Offset_%.2f.jpg' %(diameter, offset[ii]))
        cv2.imwrite(pathFile2, img)        
        
        centroid_x, centroid_y = findCentroidOpenCV(img)
        c_x.append(centre_x)
        c_y.append(centre_y)
        fc_x.append(centroid_x)
        fc_y.append(centroid_y)

        
    fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
    plt.plot(c_x, c_y, 'sb', linestyle='None', label='Actual')
    plt.plot( fc_x, fc_y,  'or', linestyle='None', label='Image Analysis')
    plt.show()
    
    plt.ylim([0,10])
#    plt.ylim([0,10])
    plt.xlabel('x-Poistion [pixels]')
    plt.ylabel('y-Poistion [pixels]')
    plt.title('%d pixel diameter sphere, incrimented at 1/%.f pixels to right' %(diameter, increment))
    plt.legend(loc='best')
    

    fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
    plt.plot(offset, c_x, 'sb', linestyle='None', label='Actual')
    plt.plot(offset, fc_x,   'or', linestyle='None', label='Image Analysis')
    plt.show()
    
    ax_inset.plot(count, r2, label = '$R^2$', color=c[2], marker='d', linestyle='None',)

#        ax_inset.plot([np.min(list1[:-2]), np.max(list1[:-2])], [self.straightLine(np.min(list1[:-2]), self.gradient1oQ), self.straightLine(np.max(list1[:-2]), self.gradient1oQ)],  color=c[2], linestyle=':', linewidth=1)
#        labelSmall = 'Fit[:-2], $m_r$=%.2f +/- %.2f with $R^2$ = %.2f' %(m, merr, r2)
#        ax_inset.plot([np.min(list1[:-2]), np.max(list1[:-2])], [self.straightLine(np.min(list1[:-2]), m), self.straightLine(np.max(list1[:-2]), m)], label=labelSmall, color=c[3], linestyle='-.', linewidth=1)
#        ax_inset.legend(fontsize=fs_sp)
#        ax_inset.set_xlim([xmin, xmax])
    ax_inset.tick_params(axis='x', labelsize=fs_sp-2)
    ax_inset.tick_params(axis='y', labelsize=fs_sp-2)
    ax_inset.set_xlabel("Ignored Data Point", fontsize=fs_sp)
    ax_inset.set_ylabel("Goodnes of Fit $R^2$", fontsize=fs_sp)
    ax_inset.legend(loc=2, fontsize=5)
    
#    plt.ylim([0,10])
#    plt.ylim([0,10])
    plt.xlabel('Offset [pixels]')
    plt.ylabel('x-position Centroid [pixels]')
    plt.title('%d pixel diameter sphere, incrimented at 1/%.f pixels to right' %(diameter, increment))
    plt.legend(loc='best')
    
    
    
    pathFile=os.path.join(path, 'Pixelation', 'Plot_Size_%d_Increment_%.2f_Steps=%d.jpg' %(diameter, increment, maxOffset))
    plt.savefig(pathFile, dpi=300)
    
    
    
if __name__ == "__main__":
    plt.close('all')
    runTest(diameter=3, maxOffset=101, increment=10.0)

            