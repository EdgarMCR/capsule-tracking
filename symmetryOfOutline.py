# -*- coding: utf-8 -*-
"""
Evaluate the symmetry of an outline and find the point at which it has become symmetric

Created on Mon Sep 14 11:43:04 2015

@author: mbbxkeh2
"""

from __future__ import absolute_import, division, print_function
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

import track_capsule_TJ_v0p12 as tr
import ReadOutputFilev0p3 as rof

SYM_ERROR_NR = 99999
ERROR_CODE = -1


def findCentroidFromOutline(pathToFolder):
    ''' Load stored capsule outlines and find centroid position.
    
    -Input=
    pathToFolder    Path to folder where pictures are stored. The program in 
                    track_capsule_TJ should have created an directory called
                    "Outlines" where the outlines of the capsules are saved.
        
    -Output-
    centroid_y      y-position of outline in pixels
    number          number of image from which outline was taken
    
    '''
    path = pathToFolder+'Outlines\\'
    filenames, leng = sortPhotosPCO(path, prefixleng=10)
    
    centroid_x = np.zeros(leng, dtype=float)
    centroid_y = np.zeros(leng, dtype=float)
    number = np.zeros(leng, dtype=int)

    for ii in range(leng):
        readPath=path+filenames[ii].fn
        cnt = np.load(readPath)
        M = cv2.moments(cnt)
        centroid_x[ii] = (M['m10']/M['m00'])
        centroid_y[ii] = (M['m01']/M['m00'])
        number[ii] = filenames[ii].number

    return centroid_x, centroid_y, number
    
    
def symmetryOfOutline(pathToOutline, plot=False):
#    otl = np.loadtxt(pathToOutline)
#    cnt=[]
#    for col in otl:
#        cnt.append([[col[0], col[1]]])
#    cnt = np.array(cnt, dtype =np.uint8)
#    print(cnt)    
    cnt = np.load(pathToOutline)
    x,y,w,h = cv2.boundingRect(cnt)
    M = cv2.moments(cnt)
    centroid_x = (M['m10']/M['m00'])
    centroid_y = (M['m01']/M['m00'])
#    print('(%f, %f)' %(centroid_x, centroid_y))
    
    arr=np.zeros((len(cnt), 2), dtype = np.int32)
    counter=0
    for col in cnt:
        arr[counter, 0] = int(float(col[0][0])- float(centroid_x))
        arr[counter, 1] = int(float(col[0][1])- float(centroid_y))
        counter +=1
#    print(arr)
    
    if plot:
        plt.close('all')
        fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
        plt.plot(arr[:,0], arr[:,1], 's', linestyle='None')
        plt.plot(0,0, 'or')
        ax.invert_yaxis()
    
    xmin = np.min(arr[:,0]); xmax = np.max(arr[:,0])
    xRange =np.arange(xmin, xmax, 1)
    
    symmetry=[]
    for x in xRange:
        top=[]; bottom=[]
        for col in arr:
            if x == col[0]:
                if col[1] >0:
                    top.append(np.array(col))
                elif col[1] < 0:
                    bottom.append(np.array(col))
        top=np.array(top); bottom = np.array(bottom)

        if len(top) >0:
            meanYTop = np.mean(top[:,1])  
        if len(bottom) >0:
            meanYBottom = np.mean(bottom[:,1]) 
        if len(top) >0 and len(bottom) >0:
#            print('top and bottom : %d, %d, mean = %f' %(meanYTop, meanYBottom, (meanYTop+0.0+ meanYBottom)))
            symmetry.append((meanYTop+0.0+ meanYBottom))
        else:
            symmetry.append(SYM_ERROR_NR)
    
    xarr = range(xmin, xmax, 1)
    for ii in range(len(symmetry)-1, -1, -1 ):
        if symmetry[ii] == SYM_ERROR_NR:
            del symmetry[ii]
            del xarr[ii]
    if plot:
        plt.plot(xarr, symmetry, '<g', linestyle='None')
        plt.plot([xmin, xmax], [np.mean(symmetry), np.mean(symmetry)], 'y', linestyle='-')
    
    return np.mean(symmetry), centroid_y
    
    
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

        
def sortPhotosPCO(path, prefixleng=10):
    """
    Return list of filename ordered
    Typical filename :     OutlineBinary_Batch040615-002-#1-1S-5kcSt-10FPS-5mlPmin-1_117.npy
    """
    fileType='.npy' #'.jpg'
    sperator='_' #'-'

    dirs = os.listdir(path)
    numberOfJPG=0

#    filenameList = [ filenameClass() for i in range(numberOfJPG)]
    filenameList=[]
    
    i=-1
    for fname in dirs:
        if (fname[-4:len(fname)] == fileType):
            try:
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
            except:
                print('\t Not inluding %s' %fname)
    
    #sort by milliseconds
    newlist = sorted(filenameList, key=lambda filenameClass: filenameClass.number) 
#    for obj in newlist:
#        obj.printOut()
    return newlist, numberOfJPG
    
def forwardDifferenc(x, FPS=1):
    dx=np.zeros(len(x-1), dtype=float)
    for jj in range(len(x)-1):
        dx[jj] = (x[jj+1] - x[jj])/((1/FPS))
    
    count = np.arange(0.5, len(x), 1)
    
    return dx, count
    
def centralDifferenc(x, FPS=1):
    dx=np.zeros(len(x-2), dtype=float)
    for jj in range(0, len(x)-2):
        dx[jj] = (x[jj+2] - x[jj])/((2.0/FPS))
    
    count = np.arange(1, len(x)-1, 1)
    
    return dx, count
    
def findSymmetryByCentreline(path, geoTJ, plot=False, show=False):
    '''
    Evaluate the point when capsule has reached a steady state from distance of
    centroid from centreline of daugther channel.
    
    The centreline is found from top and bottom of daugther channel, stored in 
    geoTJ. 
    
    -Input-
    path        path to folder with result file from run (folder that stores images)
    geoTJ       4 int values in pixels, related to the geometry: 
                    -top daugther channel
                    -bottom daugther channel
                    -left side of main channel
                    -right side of main channel
    
    plot        plot results
    show        show plots
    
    -Output-
    framesToSS      number of frames from max width to steady state
    distanceToSS    distance (in pixelse) from max width to steady state
    frameMaxWidth   Frame on which max width was reached
    frameSS         Frame on which steady state was reached
    
    
    TODO: This still assumes that there are no gaps in capsules tracking. This
    can be checked using the array "number". 
    
    '''
    #Constants
    SMOOTHING_WINDOW=11
    CUTOFF_LEFT = 0.2
    CUTOFF_RIGHT = 0.8
    #look a differential and define threshold above which capsule is not in Steady state
    THRESH_SS_LOST=0.1 #TODO: adjust this to take into account units?
    
    
    daugtherChannelMiddel = (geoTJ[0]+ geoTJ[1]+ 0.0)/2.0
    
    
    
    centroid_x_fromFile, centroid_y_fromFile, _, _, _, width1, _, _ = rof.readResultsFile(path) 
    
    readCentroidsFromOutlines = True
    #check whether file centroid positions contains only whole numbers
    for ii in range(len(centroid_x_fromFile)):
        if not np.equal(np.mod(centroid_x_fromFile[ii], 1), 0) or not np.equal(np.mod(centroid_y_fromFile[ii], 1), 0):
            readCentroidsFromOutlines=False
            centroid_x, centroid_y = centroid_x_fromFile, centroid_y_fromFile
            break;
            
    if readCentroidsFromOutlines:
        #Older versions of the script analysising the images (track_capsule_TJ)
        #rounded centroid positions to an integer, so need to find centroid position from
        #re-anaylising contour. For new result files, this is unnessecary and centroid 
        #position can be read from the results file
        centroid_x,centroid_y, number = findCentroidFromOutline(path)
            
    #find the point of maximum widht of capsule
    index=np.arange(len(width1))
    widthShort1=width1[int(CUTOFF_LEFT*len(width1)):int(CUTOFF_RIGHT*len(width1))]
    indexShort=index[int(CUTOFF_LEFT*len(width1)):int(CUTOFF_RIGHT*len(width1))]
    #TODO: ensure its that last index where max width is reached!
    maxwidth1=np.max(widthShort1)            
    indS = np.argmax(widthShort1)
    indexMaxWidth = indexShort[indS]    
    
    dx2, count = centralDifferenc(centroid_y - daugtherChannelMiddel)

    smooth_centdx2 = tr.smooth((dx2),window_len=SMOOTHING_WINDOW,window='hanning')

    endIndex=np.where(smooth_centdx2[:-SMOOTHING_WINDOW] > THRESH_SS_LOST)
    if not endIndex: #if condition is never satisfied
        endIndex = ERROR_CODE-1
    
    steadyStateReachedOnFrame =endIndex[0][-1] +1
    s = "Steady state reached on frame %d" %(steadyStateReachedOnFrame)
    
    #distance traveled to reach SS
    distanceToSS = np.sqrt( (centroid_x[steadyStateReachedOnFrame] - centroid_x[indexMaxWidth])**2 + (centroid_y[steadyStateReachedOnFrame] - centroid_y[indexMaxWidth])**2 )
    
    if plot:  #mainly for testing purposes
        xarr = range(len(centroid_y))
        fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
        plt.plot(xarr, centroid_y - daugtherChannelMiddel, 'or', linestyle='None')
        smooth_cent = tr.smooth(np.array(centroid_y - daugtherChannelMiddel).flatten(),window_len=11,window='hanning')
        plt.plot(xarr, smooth_cent[:-1], 'b', linestyle='--')
        plt.xlabel('Picture #')
        plt.ylabel('Difference Centreline and y-centroid')
        plt.xlim([0, 220])
        
        fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
        plt.plot(xarr, dx2, 'sb', linestyle='None', label='Result Central Difference')
        plt.plot(xarr, smooth_centdx2[:-1], 'r',linewidth=3, linestyle='--', label = 'Smoothed Central Difference')
    
#        xmin, xmax = plt.xlim(); dif = xmax - steadyStateReachedOnFrame; plt.xlim([int(xmax - 2.5* dif), xmax])
        plt.xlim([0, 220])
        
        ymin, ymax = plt.ylim()
    #    plt.ylim([-0.2, ymax])
        plt.plot([steadyStateReachedOnFrame, steadyStateReachedOnFrame], [-0.2, ymax], 'y',linewidth=2, linestyle='-', label = 'SS reached (on # %d)' %steadyStateReachedOnFrame)
        
        plt.xlabel('Picture #')
        plt.ylabel('Gradient of Difference Centreline and y-centroid')
        plt.legend(loc='best')
        
        ax.text(0.05, 0.2, s, fontsize=12, horizontalalignment='left', verticalalignment='center', transform = ax.transAxes)
        
        if show:
            plt.show()
        else:
            plt.close(fig)
    #framesToSS, distanceToSS, frameMaxWidth, frameSS         
    return steadyStateReachedOnFrame - indexMaxWidth +0.0, distanceToSS, indexMaxWidth, steadyStateReachedOnFrame
    
    
    
    
def runSym(path, geoTJ, plot=False, show=False):
    SMOOTHING_WINDOW=11
    daugtherChannelMiddel = (geoTJ[0]+ geoTJ[1]+ 0.0)/2.0
    filenames, leng = sortPhotosPCO(path, prefixleng=10)
    
    symmetry = np.zeros(leng, dtype=float)
    symmetry.fill(SYM_ERROR_NR)
    centroid_y = np.zeros(leng, dtype=float)
    
    for ii in range(leng):
        readPath=path+filenames[ii].fn
        symmetry[ii], centroid_y[ii] = symmetryOfOutline(readPath, plot=False)
    
    xarr = range(leng)
    for ii in range(len(symmetry)-1, -1, -1 ):
        if symmetry[ii] == SYM_ERROR_NR:
            del symmetry[ii]
            del xarr[ii]
            
    if plot:
        fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
        plt.plot(xarr, np.abs(symmetry), 's', linestyle='None')
        smooth_sym = tr.smooth(np.abs(symmetry),window_len=11,window='hanning')
        plt.plot(xarr, smooth_sym[:-1], 'r', linestyle='--')
        
        fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
        plt.plot(xarr, centroid_y - daugtherChannelMiddel, 'or', linestyle='None')
        smooth_cent = tr.smooth((centroid_y - daugtherChannelMiddel),window_len=11,window='hanning')
        plt.plot(xarr, smooth_cent[:-1], 'b', linestyle='--')
        plt.xlabel('Picture #')
        plt.ylabel('Difference Centreline and y-centroid')
        plt.xlim([100, 220])
        
    print('length actual = %d and images %d' %(len(centroid_y), leng))
#    dx1, count = forwardDifferenc(centroid_y - daugtherChannelMiddel)
    dx2, count = centralDifferenc(centroid_y - daugtherChannelMiddel)
    
    
#    smooth_centdx1 = tr.smooth((dx1),window_len=11,window='hanning')
    smooth_centdx2 = tr.smooth((dx2),window_len=SMOOTHING_WINDOW,window='hanning')

    
    #look a differential and define threshold above which it is not in SS
    threshSSLost=0.1 #TODO: adjust this to take into account units?
    endIndex=np.where(smooth_centdx2[:-SMOOTHING_WINDOW] > threshSSLost)
    if not endIndex: #if condition is never satisfied
        endIndex = ERROR_CODE-1
    
    steadyStateReachedOnFrame =endIndex[0][-1] +1
    s = "Steady state reached on frame %d" %steadyStateReachedOnFrame
    
    fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
#    plt.plot(xarr, dx1, 'or', linestyle='None', label='Result Forward Difference')
    plt.plot(xarr, dx2, 'sb', linestyle='None', label='Result Central Difference')
#    plt.plot(xarr, smooth_centdx1[:-1], 'r', linestyle='--', label = 'Smoothed Forward Difference')
    plt.plot(xarr, smooth_centdx2[:-1], 'r',linewidth=3, linestyle='--', label = 'Smoothed Central Difference')

    xmin, xmax = plt.xlim()
    dif = xmax - steadyStateReachedOnFrame
#    plt.xlim([int(xmax - 2.5* dif),len(width1) xmax])
    plt.xlim([100, 220])
    
    ymin, ymax = plt.ylim()
#    plt.ylim([-0.2, ymax])
    plt.plot([steadyStateReachedOnFrame, steadyStateReachedOnFrame], [-0.2, ymax], 'y',linewidth=2, linestyle='-', label = 'SS reached (on # %d)' %steadyStateReachedOnFrame)
    
    plt.xlabel('Picture #')
    plt.ylabel('Gradient of Difference Centreline and y-centroid')
    plt.legend(loc='best')
    
    ax.text(0.05, 0.2, s, fontsize=12, horizontalalignment='left', verticalalignment='center', transform = ax.transAxes)
    
    sp1=path.rfind('\\')
    sp2=path[:sp1].rfind('\\')
    sp3=path[:sp2].rfind('\\')
    directory=path[:sp2]
#    print(directory)
    fullpath=directory + "\\%s_GradientCentreline.jpg" %path[sp3+1:sp2]
    
    if not os.path.exists(path[:sp3] + "\\Symmetry"): os.makedirs(path[:sp3] + "\\Symmetry")
    fullpath2=path[:sp3] + "\\Symmetry\\%s_GradientCentreline.jpg" %path[sp3+1:sp2]
    
    plt.title(path[sp3+1:sp2] + ' Difference Centreline')
#    print(fullpath)
    plt.savefig(fullpath, dpi=300)
    plt.savefig(fullpath2, dpi=300)
    
    if show:
        plt.show()
    else:
        plt.close(fig)
    
    return steadyStateReachedOnFrame
    
def runOnDirectory(directory, geoTJ, geoTJ2=None, fpsSpecial=[]):
    listFolders=os.listdir(directory)
    indexDelet=[]
    for i in range(len(listFolders)):
        if os.path.isfile(directory+listFolders[i]):
            indexDelet.append(i)

    for i in range(len(indexDelet)-1, -1, -1):
        del listFolders[indexDelet[i]]
    listFolders.sort()
    foldersThatWorked=[]
    foldersDidntWorked=[]
    q=[]
    ss=[]
    fps=[]
    filename=[]
    maxWidthAt=[]
    for f in listFolders:     
        try:
            sp1=f.rfind('mlPmin')
            sp2 = f[:sp1].rfind('-')
            if sp2 == -1:
                sp2 = f[:sp1].rfind('_')
                
            sp3=f.find('FPS')
            sp4=f[:sp1].rfind('_')
            if sp4 == -1 or (len(f[:sp3]) - sp4 ) > 5:
                sp4=f[:sp3].rfind('-')
    
            FPSString=float(f[sp4+1:sp3]) 
    #            print('print sp1 = %d, sp2 = %d, %s' %(sp1, sp2, f[sp2+1:sp1]))
            
            geo = geoTJ
            if geoTJ2 != None:
                if FPSString in fpsSpecial:
                    geo = geoTJ2
                
            
            print('\n Starting \t %s \n' %f)
            path=directory + f + '\\Outlines\\'
            ssIndex = runSym(path = path, geoTJ = geo, plot= False, show=False)
            ss.append(ssIndex)
            q.append(float(f[sp2+1:sp1]))
            fps.append(FPSString)
            filename.append(f)
            foldersThatWorked.append(f)
            
            #get other measurments
            centroid_x, centroid_y, _, _, _, width1, _, _ = rof.readResultsFile(directory + f + '\\') 
            index=np.arange(len(width1))
            widthShort1=width1[int(0.2*len(width1)):int(0.8*len(width1))]
            indexShort=index[int(0.2*len(width1)):int(0.8*len(width1))]
            
            maxwidth1=np.max(widthShort1)            
            indS = np.argmax(widthShort1)
            indexMaxWidth = indexShort[indS]
            maxWidthAt.append(indexMaxWidth)
#            find_max_extend(directory+f)
        except Exception, err:
            print('Didnt work for \t %s (%s)' %(f, err))
            foldersDidntWorked.append(f)
            
    d1 = directory.rfind('\\')
    batchID=directory[d1+1:]

    print('\nWorked in :')
    for f in foldersThatWorked:
        print(f)
    print("\nDidn't Worked in :")
    for f in foldersDidntWorked:
        print(f)
    
#    print(q)
#    print(ss)
#    print('len(q) = %d, len(ss) = %d' %(len(q), len(ss)))
    fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
    ss=np.array(ss)
    maxWidthAt=np.array(maxWidthAt)
    fps=np.array(fps)
    q=np.array(q)
#    print('len q, ss, maxw, fps: %d, %d, %d, %d' %(len(q), len(ss), len(maxWidthAt), len(fps)))
    relaxationTime = (ss-maxWidthAt)/fps
    plt.plot(q, relaxationTime, 'sb', linestyle='None')
    plt.ylabel('Time [s]')
    plt.xlabel('Volum Flux $Q$ [ml/min]')
    plt.title('Relaxation Time (max widht -ss) %s' %(batchID))
    plt.savefig(directory + '\\%s-RelaxationTime.jpg' %batchID)
    
    
    #==========================================================================
    #Write results to file
    #==========================================================================
    
    pathData= directory+'\\%s-RelaxationTime_Results.txt' %batchID

#    if not os.path.isfile(pathData): #check whether the file for this run has been started
    fileData = open(pathData, 'w')
    fileData.write('FPS \tvolumn flux  \tname \t\t\t\t\t image # max width \t image # ss \t relaxation time [s] \n')
    
    for ii in range(len(q)):
        writeString = '%.1f \t%.1f \t%s \t%d \t%d \t%.4e \n' %(fps[ii], q[ii], filename[ii], maxWidthAt[ii], ss[ii], relaxationTime[ii])
        fileData.write(writeString)
    fileData.close()


    return q, ss, maxWidthAt, fps, relaxationTime
    
def runOnDirectorySym(directory, geoTJ, geoTJ2=None, fpsSpecial=[]):
    listFolders=os.listdir(directory)
    indexDelet=[]
    for i in range(len(listFolders)):
        if os.path.isfile(directory+listFolders[i]):
            indexDelet.append(i)

    for i in range(len(indexDelet)-1, -1, -1):
        del listFolders[indexDelet[i]]
    listFolders.sort()
    foldersThatWorked=[]
    foldersDidntWorked=[]
    q=[]
    ss=[]
    framesToSS=[]
    disToSS=[]
    fps=[]
    filename=[]
    maxWidthAt=[]
    for f in listFolders[5:15]:     
        try:
            sp1=f.rfind('mlPmin')
            sp2 = f[:sp1].rfind('-')
            if sp2 == -1:
                sp2 = f[:sp1].rfind('_')
                
            sp3=f.find('FPS')
            sp4=f[:sp1].rfind('_')
            if sp4 == -1 or (len(f[:sp3]) - sp4 ) > 5:
                sp4=f[:sp3].rfind('-')
    
            FPSString=float(f[sp4+1:sp3]) 
    #            print('print sp1 = %d, sp2 = %d, %s' %(sp1, sp2, f[sp2+1:sp1]))
            
            geo = geoTJ
            if geoTJ2 != None:
                if FPSString in fpsSpecial:
                    geo = geoTJ2
                
            
            print('\n Starting \t %s \n' %f)
#            path=directory + f + '\\Outlines\\'
            path=directory + f +'\\'
            timeInFramesToSS, distanceToSS, indexMaxWidth, ssIndex = findSymmetryByCentreline(path = path, geoTJ = geo, plot= False, show=False)
            framesToSS.append(timeInFramesToSS)
            disToSS.append(distanceToSS)
            ss.append(ssIndex)
            maxWidthAt.append(indexMaxWidth)
            q.append(float(f[sp2+1:sp1]))
            fps.append(FPSString)
            filename.append(f)
            foldersThatWorked.append(f)
            
#            find_max_extend(directory+f)
        except Exception, err:
            print('Didnt work for \t %s (%s)' %(f, err))
            foldersDidntWorked.append(f)
            
    d1 = directory.rfind('\\')
    batchID=directory[d1+1:]

    print('\nWorked in :')
    for f in foldersThatWorked:
        print(f)
    print("\nDidn't Worked in :")
    for f in foldersDidntWorked:
        print(f)
    
#    print(q)
#    print(ss)
#    print('len(q) = %d, len(ss) = %d' %(len(q), len(ss)))
    fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
    ss=np.array(ss)
    maxWidthAt=np.array(maxWidthAt)
    fps=np.array(fps)
    q=np.array(q)
#    print('len q, ss, maxw, fps: %d, %d, %d, %d' %(len(q), len(ss), len(maxWidthAt), len(fps)))
    relaxationTime = (ss-maxWidthAt)/fps
    plt.plot(q, relaxationTime, 'sb', linestyle='None')
    plt.ylabel('Time [s]')
    plt.xlabel('Volum Flux $Q$ [ml/min]')
    plt.title('Relaxation Time (max widht -ss) %s' %(batchID))
#    plt.savefig(directory + '\\%s-RelaxationTime.jpg' %batchID)
    
    fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
    disToSS=np.array(disToSS)
#    print('len q, ss, maxw, fps: %d, %d, %d, %d' %(len(q), len(ss), len(maxWidthAt), len(fps)))
    plt.plot(q, disToSS, 'sb', linestyle='None')
    plt.ylabel('Distance to Steady State [pixels]')
    plt.xlabel('Volum Flux $Q$ [ml/min]')
    plt.title('Relaxation Distance %s' %(batchID))
    
    
    #==========================================================================
    #Write results to file
    #==========================================================================
    
    pathData= directory+'\\%s-RelaxationTime_Results.txt' %batchID

#    if not os.path.isfile(pathData): #check whether the file for this run has been started
    fileData = open(pathData, 'w')
    fileData.write('FPS \tvolumn flux  \tname \t\t\t\t\t image # max width \t image # ss \t relaxation time [s] \n')
    
    for ii in range(len(q)):
        writeString = '%.1f \t%.1f \t%s \t%d \t%d \t%.4e \n' %(fps[ii], q[ii], filename[ii], maxWidthAt[ii], ss[ii], relaxationTime[ii])
        fileData.write(writeString)
    fileData.close()


    return q, ss, maxWidthAt, fps, relaxationTime


if __name__ == "__main__":
    plt.close('all')
    geoTJ040615d002nr1 = [38, 122, 549, 722]
    path="M:\\EdgarHaener\\Capsules\\Batch040615-002\\T-Junction\\Capsule#1\\Batch040615-002-#1-1S-5kcSt-10FPS-5mlPmin-1\\"
    findSymmetryByCentreline(path, geoTJ=geoTJ040615d002nr1, plot=True, show=True)
    directory="M:\\EdgarHaener\\Capsules\\Batch040615-002\\T-Junction\\Capsule#1\\"
#    runOnDirectorySym(directory, geoTJ=geoTJ040615d002nr1, geoTJ2=None, fpsSpecial=[])
#    runSym(path = path, geoTJ = geoTJ040615d002nr1, plot= False)
    
    
#    q, ss, maxWidthAt, fps, relaxationTime = runOnDirectory(directory, geoTJ = geoTJ040615d002nr1)
    
    path="M:\\EdgarHaener\\Capsules\\Batch040615-002\\T-Junction\\Capsule#1\\Batch040615-002-#1-1S-5kcSt-140FPS-70mlPmin-7\\Outlines\\"
#    runSym(path=path, geoTJ=geoTJ040615d002nr1, plot=True, show=True)
    
    path="M:\\EdgarHaener\\Capsules\\Batch040615-002\\T-Junction\\Capsule#1\\Batch040615-002-#1-1S-5kcSt-140FPS-70mlPmin-7\\Outlines\\OutlineBinary_Batch040615-002-#1-1S-5kcSt-140FPS-70mlPmin-7_212.npy"
#    symmetryOfOutline(pathToOutline=path, plot=True)
    
#    geoTJ120615d004nr5 = [35, 118, 549,  724]
#    geoTJ120615d004nr5d15mlPmin = [72, 160, 550, 725]
#    directory="M:\\EdgarHaener\\Capsules\\Batch120615-004\\T-Junction\\"
#    q2, ss2, maxWidthAt2, fp2s, relaxationTime2 = runOnDirectory(directory, geoTJ = geoTJ040615d002nr1, geoTJ2 = geoTJ120615d004nr5d15mlPmin, fpsSpecial=[30])
#    
#    fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
#    plt.plot(q, relaxationTime, 'sb', linestyle='None', label='Batch040615-002 #1')
#    plt.plot(q2, relaxationTime2, 'or', linestyle='None', label='Batch120615-004 #5')
#    plt.ylabel('Time [s]')
#    plt.xlabel('Volum Flux $Q$ [ml/min]')
#    plt.title('Relaxation Time (max widht -ss)')
#    plt.legend(loc='best')
#    plt.savefig('M:\\EdgarHaener\\%s-RelaxationTime.jpg')
    
    