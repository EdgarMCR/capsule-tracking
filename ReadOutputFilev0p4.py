# -*- coding: utf-8 -*-
"""
Created on Fri Mar 07 15:23:59 2014

@author: Edgar
"""
from __future__ import absolute_import, division, print_function
import matplotlib
#matplotlib.use('Qt4Agg')
#matplotlib.use("agg") 
import matplotlib.pyplot as plt
import numpy as np
import platform
import track_capsule_TJ_v0p12 as tr
import cv2
import os
import sys
import shutil
import gc


#==============================================================================
# Measuring Relaxation Time of Capsule after T-Junction
#==============================================================================

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

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# The class and sortPhotos functions are copied from  track_capsules_TJ and adapted
#TODO: use only one version
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
    filenameList=[]
    
    i=-1
    for fname in dirs:
        if (fname[-4:len(fname)] == fileType):
            try:
                d=fname.rfind('\\', 1, -1)
                if fname[d+1:d+3] == '._':
                    continue
                i+=1            
                name=fname[:-4]
                d1=name.find(sperator,-5,-1)
                
                temp=filenameClass()
                temp.fn = fname
                temp.number=abs(int(float(name[d1+1:])))
                temp.fps=-1
                   
                filenameList.append(temp)
                numberOfJPG += 1
            except:
                print('\t Not inluding %s' %fname)
    
    newlist = sorted(filenameList, key=lambda filenameClass: filenameClass.number) 
    return newlist, numberOfJPG

def centralDifferenc(x, FPS=1):
    dx=np.zeros(len(x-2), dtype=float)
    for jj in range(0, len(x)-2):
        dx[jj] = (x[jj+2] - x[jj])/((2.0/FPS))
    
    count = np.arange(1, len(x)-1, 1)
    
    return dx, count
    
def findSymmetryByCentreline(path, geoTJ, centroidAndWidth=None, plot=False, show=False, show2 = False, ignorlast=None):
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
                    
    centroidAndWidth = [centroid_x,     centroid_y,     width ]  - will be loaded from file if not provided
    
    plot        plot results
    show        show plots
    
    -Output-
    framesToSS      number of frames from max width to steady state
    distanceToSS    distance (in pixelse) from max width to steady state
    frameMaxWidth   Frame on which max width was reached
    frameSS         Frame on which steady state was reached

    '''
    #Constants
    SMOOTHING_WINDOW=11
    
    #how many points at the end to ignore
    if ignorlast == None:
        IGNORELAST = SMOOTHING_WINDOW 
    else:
        IGNORELAST = ignorlast
    CUTOFF_LEFT = 0.2
    CUTOFF_RIGHT = 0.8
    #look a differential and define threshold above which capsule is not in Steady state
    THRESH_SS_LOST=0.1 #TODO: adjust this to take into account units?
    
    daugtherChannelMiddel = (geoTJ[0]+ geoTJ[1]+ 0.0)/2.0
    if not centroidAndWidth:
        centroid_x_fromFile, centroid_y_fromFile, _, _, _, width1, _, _ = readResultsFile(path) 
    else:
        centroid_x_fromFile, centroid_y_fromFile, width1 = centroidAndWidth
        
        
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

    endIndex=np.where(smooth_centdx2[:-IGNORELAST] > THRESH_SS_LOST)
    if not endIndex: #if condition is never satisfied
        endIndex = ERROR_CODE-1
    
    steadyStateReachedOnFrame =endIndex[0][-1] +1
    s = "Steady state reached on frame %d" %(steadyStateReachedOnFrame)
    if steadyStateReachedOnFrame - 2 == index[-1]-IGNORELAST:
        import warnings
        warnings.warn("Steady state reached on last point. This is indicative of an error")
        
    
    #distance traveled to reach SS
    distanceToSS = np.sqrt( (centroid_x[steadyStateReachedOnFrame] - centroid_x[indexMaxWidth])**2 + (centroid_y[steadyStateReachedOnFrame] - centroid_y[indexMaxWidth])**2 )
#    print('Distance moved is %.2f pixels  from (%d, %d) to (%d, %d) and time is %d frames' %(distanceToSS, centroid_x[steadyStateReachedOnFrame], centroid_y[steadyStateReachedOnFrame], centroid_x[indexMaxWidth], centroid_y[indexMaxWidth], steadyStateReachedOnFrame - indexMaxWidth +0.0))    
    
    if plot:  #mainly for testing purposes
        xarr = range(len(centroid_y))
        fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
        plt.plot(xarr, centroid_y - daugtherChannelMiddel, 'or', linestyle='None')
        smooth_cent = tr.smooth(np.array(centroid_y - daugtherChannelMiddel).flatten(),window_len=11,window='hanning')
        plt.plot(xarr, smooth_cent[:-1], 'b', linestyle='--')
        plt.xlabel('Picture #')
        plt.ylabel('Difference Centreline and y-centroid')
        plt.grid()
        if show2:
            plt.show()
        else:
            d1 = path[:-1].rfind(os.sep)
            plt.savefig(path+path[d1+1:-1] +'_Ypos_DaugtherChannel.jpg', dpi=600)
            plt.close(fig)
        
        fig = plt.figure(figsize=(8, 6), dpi=200,); ax = fig.add_subplot(111)
        plt.plot(xarr, dx2, 'sb', linestyle='None', label='Result Central Difference')
        plt.plot(xarr, smooth_centdx2[:-1], 'r',linewidth=3, linestyle='--', label = 'Smoothed Central Difference')        
        
        plt.ylim([-20.0*THRESH_SS_LOST, 20.0*THRESH_SS_LOST])
        ymin, ymax = plt.ylim()
        plt.plot([steadyStateReachedOnFrame, steadyStateReachedOnFrame], [ymin, ymax], 'y',linewidth=2, linestyle='-', label = 'SS reached (on # %d)' %steadyStateReachedOnFrame)
        plt.plot([index[-1]-IGNORELAST+2, index[-1]-IGNORELAST+2], [ymin, ymax], 'g',linewidth=2, linestyle='-')
        
        plt.xlabel('Picture #')
        plt.ylabel('Gradient of Difference Centreline and y-centroid')
        plt.legend(loc='best')
        plt.grid()
        ax.text(0.05, 0.2, s, fontsize=12, horizontalalignment='left', verticalalignment='center', transform = ax.transAxes)
        
        d1 = path[:-1].rfind(os.sep)
        plt.savefig(path+path[d1+1:-1] +'_dYposdt_DaugtherChannel.jpg', dpi=600)
        
        #temporary Check 
        d2 = path[:d1-1].rfind(os.sep)
        ndir = path[:d2] + os.sep + 'Symmetry' + os.sep
        if not os.path.exists(ndir): os.makedirs(ndir)
        plt.savefig(ndir+path[d1+1:-1] +'_dYposdt_DaugtherChannel.jpg', dpi=600)
        
        if show:
            plt.show()
        else:
            plt.close(fig)
    #framesToSS, distanceToSS, frameMaxWidth, frameSS         
    return steadyStateReachedOnFrame - indexMaxWidth +0.0, distanceToSS, indexMaxWidth, steadyStateReachedOnFrame
    
   
    
    
def runOnDirectorySym(directory, geoTJ, geoTJ2=None, fpsSpecial=[], plot=False):
    '''
    Run findSymmetryByCentreline on a whole directory
    '''
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
#            path=directory + f + '\\Outlines\\'
            path=directory + f +'\\'
            timeInFramesToSS, distanceToSS, indexMaxWidth, ssIndex = findSymmetryByCentreline(path = path, geoTJ = geo, plot= plot, show=False)
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


    return framesToSS, disToSS, q, ss, maxWidthAt, fps, relaxationTime

# Ende  - Measuring Relaxation Time of Capsule after T-Junction
#==============================================================================




def runTwoCapsulesForDirectory(directory, rerun = False, centerline=None, width=None, pPmm=None, geoTJ=None): 
    if platform.system() == 'Linux':
        dSlash='/'
    elif platform.system() == 'Windows': 
        dSlash='\\'
    else:
        print('Unknow Oporating System -  failed')
        
    if rerun:
        ss1=directory.rfind(dSlash, 1,-1)
    #    print('ss1 = %s \t %s' %(ss1, directory[:ss1]))
        ss2=directory.rfind(dSlash, 1,ss1)
    #    print('ss2 = %s \t %s' %(ss2, directory[:ss2]))
        ss3=directory.rfind(dSlash, 1,ss2)
        
        pathData= directory +directory[ss2+1:ss1]+'-'+directory[ss1+1:-1]+'_ResultsTwoCapsules.txt'
        pathDataSave = directory +directory[ss2+1:ss1]+'-'+directory[ss1+1:-1]+'_ResultsTwoCapsules_ORG.txt'
        
        pathParameters= directory +directory[ss2+1:ss1]+ '_ParametersTwoCapsules.txt'
        pathParametersSave= directory +directory[ss2+1:ss1]+ '_ParametersTwoCapsules_ORG.txt'
        pathParametersSave2= directory +directory[ss2+1:ss1]+ '_ParametersTwoCapsules_ORG2.txt'
        
        try:
            fileParameters = open(pathParameters, 'r')
        except:
            print("Could not open file. \nFile name = %s \n Function will returns" %pathParameters)
            return
        print('pathParameters = %s' %pathParameters)
        print('pathData = %s' %pathData)
        lines = fileParameters.readlines()
        fileParameters.close()       
        print(lines)
        
        #safty copy of results
        if  not os.path.isfile(pathDataSave) and os.path.isfile(pathData):
            shutil.copyfile(pathData, pathDataSave)    
        
        #safty copy of parameters
        if os.path.isfile(pathParametersSave):
            shutil.copyfile(pathParameters, pathParametersSave2)
            os.remove(pathParameters)
        else:
            shutil.copyfile(pathParameters, pathParametersSave)
            os.remove(pathParameters)
    
        for line in lines:
            entriesLine=line.split('\t')
            if entriesLine[0].strip() != 'fileID':         
                entriesLine[-1] = entriesLine[-1][:-2]
                print('')
                print(entriesLine)
                

                #find FPS info
                sp1=entriesLine[0].find('FPS')
                sp2=entriesLine[0][:sp1].rfind('_')
                if sp2 == -1 or (len(entriesLine[0][:sp1]) - sp2) >5:
                    sp2=entriesLine[0][:sp1].rfind('-')
    #            print('entriesLine[0][sp2+1:sp1] = %s ' %entriesLine[0][sp2+1:sp1])
                FPS=int(entriesLine[0][sp2+1:sp1])
    #            print('FPS=%d' %FPS)
                
                pathFolder=directory  + entriesLine[0].strip() + dSlash
          
                #find index information
                if entriesLine[1].strip() == '-1':
                    Index=None
                else:
                    Index=[int(entriesLine[1]),int(entriesLine[2]),int(entriesLine[3]),int(entriesLine[4]), int(entriesLine[5]),int(entriesLine[6]),int(entriesLine[7]),int(entriesLine[8])]
                
                if centerline == None and len((entriesLine)) >=9:
                    centerline = float(entriesLine[9].strip())
                    width = float(entriesLine[10].strip())
                    pPmm = float(entriesLine[11].strip())
                    geoTJ = [float(entriesLine[12].strip()), float(entriesLine[13].strip()), float(entriesLine[14].strip())]
                analyisTwoCapsules(pathFolder,centerline=centerline, widthChannel=width, pPmm=pPmm, FPS=FPS, Index=Index, borderSize=10, debugInfo=False, closeAfterPlotting=True, geoCutOff=geoTJ, plot=False)   
                plt.close('all')
                gc.collect()
    else: #Not a re-run, running for the first time
        assert(centerline != None) 
        listFolders=os.listdir(directory)
        indexDelet=[]
        for i in range(len(listFolders)):
            if os.path.isfile(directory+listFolders[i]):
                indexDelet.append(i)
    
        for i in range(len(indexDelet)-1, -1, -1):
            del listFolders[indexDelet[i]]
            
        foldersThatWorked=[]
        for f in listFolders:
            sp1=f.find('FPS')
            sp2=f[:sp1].rfind('_')
            if sp2 == -1 or (len(f[:sp1]) - sp2 ) > 5:
                sp2=f[:sp1].rfind('-')
    #            print('entriesLine[0][sp2+1:sp1] = %s ' %entriesLine[0][sp2+1:sp1])
            FPSString=int(f[sp2+1:sp1])  
            FPS = float(FPSString)
            
#            try:
            print('\n Starting \t %s with FPS = %.f \n' %(f, FPS))
            try:
                pathFolder = directory +  f + '\\'
                analyisTwoCapsules(pathFolder,centerline=centerline, widthChannel=width, pPmm=pPmm, FPS=FPS, Index=None, borderSize=10, debugInfo=False, closeAfterPlotting=True, geoCutOff=geoTJ, plot=True)   
                foldersThatWorked.append(f)
    #            find_max_extend(directory+f)
            except Exception, err:
                print('Didnt work for \t %s err = %s' %(f, err))
        
        print('\nWorked in :')
        for f in foldersThatWorked:
            print(f)
    
def rerunWithOldParameters(directory,centerline=None, width=None, pPmm=None, geoTJ=None):    
    #TODO: use os module instead
    if platform.system() == 'Linux':
        dSlash='/'
    elif platform.system() == 'Windows': 
        dSlash='\\'
    else:
        print('Unknow Oporating System -  failed')
        
#    ss1=path.rfind(dSlash, 1,-1)
#    ss2=path.rfind(dSlash, 1,ss1)
#    ss3=path.rfind(dSlash, 1,ss2)
#    pathData= path[0:ss1] + dSlash + path[ss3+1:ss2]+'-'+path[ss2+1:ss1]+'_Results.txt'
#    pathParameters= path[0:ss1] + dSlash + path[ss3+1:ss2]+'_Parameters.txt'
#    print('directory = %s ' %(directory))
    ss1=directory.rfind(dSlash, 1,-1)
#    print('ss1 = %s \t %s' %(ss1, directory[:ss1]))
    ss2=directory.rfind(dSlash, 1,ss1)
#    print('ss2 = %s \t %s' %(ss2, directory[:ss2]))
    ss3=directory.rfind(dSlash, 1,ss2)
    
    pathData= directory +directory[ss2+1:ss1]+'-'+directory[ss1+1:-1]+'_Results.txt'
    pathDataSave = directory +directory[ss2+1:ss1]+'-'+directory[ss1+1:-1]+'_Results_ORG.txt'
    
    pathParameters= directory +directory[ss2+1:ss1]+ '_Parameters.txt'
    pathParametersSave= directory +directory[ss2+1:ss1]+ '_Parameters_ORG.txt'
    pathParametersSave2= directory +directory[ss2+1:ss1]+ '_Parameters_ORG2.txt'

    
    try:
        fileParameters = open(pathParameters, 'r')
    except:
        print("Could not open file. \nFile name = %s \n Function will returns" %pathParameters)
        return
    print('pathParameters = %s' %pathParameters)
    print('pathData = %s' %pathData)
    lines = fileParameters.readlines()
    fileParameters.close()       
    print(lines)
    
    #safty copy of results
    if  not os.path.isfile(pathDataSave) and os.path.isfile(pathData):
        shutil.copyfile(pathData, pathDataSave) 
        os.remove(pathData)
    
    #safty copy of parameters
    if os.path.isfile(pathParametersSave):
        shutil.copyfile(pathParameters, pathParametersSave2)
        os.remove(pathParameters)
    else:
        shutil.copyfile(pathParameters, pathParametersSave)
        os.remove(pathParameters)
        
    if centerline == None:
        readP=True
    else:
        readP=False
        
    for line in lines:
        entriesLine=line.split('\t')
        if entriesLine[0].strip() != 'fileID': #check its not the header         
            entriesLine[-1] = entriesLine[-1][:-2].strip() #what am I doing here?
            while '' in entriesLine:
                entriesLine.remove('')
            print('')
            print(entriesLine)
            
            
            #find FPS info
            sp1=entriesLine[0].find('FPS')
            sp2=entriesLine[0][:sp1].rfind('_')
            if sp2 == -1 or (len(entriesLine[0][:sp1]) - sp2) >5: #sometimes used underscore, sometimes dash when naming folders
                sp2=entriesLine[0][:sp1].rfind('-')
#            print('entriesLine[0][sp2+1:sp1] = %s ' %entriesLine[0][sp2+1:sp1])
            FPS=float(entriesLine[0][sp2+1:sp1])
#            print('FPS=%d' %FPS)
            
            pathFolder=directory  + entriesLine[0].strip() + dSlash
      
            #find index information
            if entriesLine[5].strip() == '-1':
                Index=None
            else:
                Index=[int(entriesLine[4]),int(entriesLine[5]),int(entriesLine[6]),int(entriesLine[7])]
            
            if readP and len((entriesLine)) ==14: #old parameter file with only three entries in geoTJ object
                centerline = float(entriesLine[8].strip())
                width = float(entriesLine[9].strip())
                pPmm = float(entriesLine[10].strip())
                geoTJr = [geoTJ[0], float(entriesLine[11].strip()), float(entriesLine[12].strip()), float(entriesLine[13].strip())]
                geoTJ = geoTJr
                ignorelast=None
            elif readP and len((entriesLine)) >14:
                centerline = float(entriesLine[8].strip())
                width = float(entriesLine[9].strip())
                pPmm = float(entriesLine[10].strip())
                geoTJ = [float(entriesLine[11].strip()), float(entriesLine[12].strip()), float(entriesLine[13].strip()), float(entriesLine[14].strip())]
                
                if len((entriesLine)) == 15:
                    ignorelast=None
                else:
                    if float(entriesLine[15].strip()) == 0 :
                        ignorelast=None
                    else:
                        ignorelast=float(entriesLine[15].strip())
            
#            analyisTwoCapsules(path,centerline, width, pPmm, FPS=64, Index=None, borderSize=10, debugInfo=True, closeAfterPlotting=False, geoCutOff=[0,0,0], plot=True)
            findSpeedGradient(pathFolder,centerline=centerline, widthChannel=width, pPmm=pPmm, FPS=FPS, Index=Index, UseEverySecond=False, borderSize=10, closeAfterPlotting=True, geoCutOff=geoTJ, plot=False, ignorlastSym=ignorelast)
            plt.close('all')

           
            
def readResultsFile(path, second=False):
    fileID=tr.find_batchName(path);
    if second:
        path_to_file = path+fileID+'_Results_2nd.txt'
    else:
        path_to_file = path+fileID+'_Results.txt'

    numOfLines=file_len(path_to_file)
    
    #This opens a handle to your file, in 'r' read mode
    file_handle = open(path_to_file, 'r')
    
    # Read in all the lines of your file into a list of lines
    lines_list = file_handle.readlines()
    
    centroid_x=np.zeros((numOfLines), dtype=float)
    centroid_y=np.zeros((numOfLines), dtype=float)
    area=np.zeros((numOfLines,1), dtype=float)
    width =np.zeros((numOfLines), dtype=float)
    height =np.zeros((numOfLines,1), dtype=float)
    d12 =np.zeros((numOfLines,1), dtype=float)
    v_x=np.zeros((numOfLines-1,1), dtype=float)
    v_y=np.zeros((numOfLines-1,1), dtype=float)
    
    
    indexC=0
    index=0
    linecounter=-1
    
    for line in lines_list:
        linecounter=linecounter+1
        if linecounter==0 :
            continue
        
        entries=line.split()
    #    print(entries)
    #    print(' \t len(entries) = '+str(len(entries)))
        
        # # 	 Ver Dist 	 Hor Dist 	 Perimeter 	 Area 	 centroid_x 	 centroid_y 	 width[i] 	 heigth[i] 	 D 	 angle 	 time (s) 	vel_x (mm/s)	 vel_y (mm/s)	  
        if len(entries)<14:
            if len(entries)>6:
                area[indexC]=float(entries[4])
                centroid_x[indexC]=float(entries[5])
                centroid_y[indexC]=float(entries[6])
                indexC += 1
            continue
        
        centroid_x[indexC]=float(entries[5])
        centroid_y[indexC]=float(entries[6])
        width[indexC]=float(entries[7])
        height[indexC]=float(entries[8])
        d12[indexC]=float(entries[9])
        indexC += 1
        v_x[index]=float(entries[12])
        v_y[index]=float(entries[13])
    #    print('v_x = ' + str(v_x[index])+'\t v_y = ' + str(v_y[index]))    
        index=index+1  
        
    return centroid_x, centroid_y, v_x, v_y, area, width, d12, height
    
def plotCentorid(path, numberToPlot=3, borderSize=10, rotate=0, show=False):
    
    centroid_x, centroid_y, _, _, _, _, _, _ = readResultsFile(path) 
    
    #Check centering of capusle - assume first half is in main channel
    cutOff=0.1 #cut of 10% either side
    leng=len(centroid_x)
    imageNumber = np.arange(leng)
    imageNumber = imageNumber[cutOff*leng:(0.5-cutOff)*leng]
    x_mainC= centroid_x[cutOff*leng:(0.5-cutOff)*leng]
    y_mainC= centroid_y[cutOff*leng:(0.5-cutOff)*leng]
    
    if numberToPlot == 3:
        imgNum=[imageNumber[0], imageNumber[int(len(imageNumber)/2)], imageNumber[-1]]
        x=[x_mainC[0], x_mainC[int(len(imageNumber)/2)], x_mainC[-1]]
        y=[y_mainC[0], y_mainC[int(len(imageNumber)/2)], y_mainC[-1]]
    else:
        increment=int((len(imageNumber)-1)/numberToPlot)
        index=np.arange(0, len(imageNumber), increment)
        imgNum=[imageNumber[jj] for jj in index]
        x =[x_mainC[jj] for jj in index]
        y =[y_mainC[jj] for jj in index]
    
    fileList, leng =tr.sortPhotosPCO(path)
    
    if platform.system() == 'Linux':
        savepath=path+'CentroidCheck/'
    elif platform.system() == 'Windows': 
        savepath=path+'CentroidCheck\\'
    if not os.path.exists(savepath): os.makedirs(savepath)

    for i in range(len(imgNum)):     
        
        if imgNum[i] < 10:
            readPath=path+fileList[i].fn[:-5]+str(imgNum[i])+'.png'
            print('readpath: %s' %readPath)
        elif  imgNum[i] < 100:
            readPath=path+fileList[i].fn[:-6]+str(imgNum[i])+'.png'
            print('readpath: %s' %readPath)
        elif  imgNum[i] < 1000:
            readPath=path+fileList[i].fn[:-7]+str(imgNum[i])+'.png'
            print('readpath: %s' %readPath)
                
#        print("readPath: %s" %readPath)
        img =cv2.imread(readPath,0)
        
        if rotate != 0:
            img=tr.rotateImage(img, rotate)
        
        cv2.circle(img,(x[i]-borderSize, y[i]-borderSize), 5, (255,255,255), -1)
        
        cv2.imwrite(savepath+'ImagewCentroid_'+str(imgNum[i])+'.jpg', img)
                
        if show:
            titlestring='%s'%imgNum[i]
            cv2.imshow(titlestring, img)
            
def forwardDifferenc(vel_x, vel_y, imageCounter, FPS):
    acceleration_x=np.zeros((len(vel_x-1),1), dtype=float)
    acceleration_y=np.zeros((len(vel_x-1),1), dtype=float)
    acceleration_mag=np.zeros((len(vel_x-1)), dtype=float)
    
    for jj in range(len(vel_x)-1):
        acceleration_x[jj] = (vel_x[jj+1] - vel_x[jj])/((1/FPS)*(imageCounter[jj+1] - imageCounter[jj]))
        acceleration_y[jj] = (vel_y[jj+1] - vel_y[jj])/((1/FPS)*(imageCounter[jj+1] - imageCounter[jj]))
        acceleration_mag[jj] = np.sqrt((acceleration_x[jj])**2 + (acceleration_y[jj])**2)
    
    return acceleration_x, acceleration_y, acceleration_mag
    

def findAccelerationFromPosition(centroid_x, centroid_y, FPS):
    numOfLines= len(centroid_x)
    disp_x=np.zeros((numOfLines-1), dtype=float)
    disp_y=np.zeros((numOfLines-1), dtype=float)  
    vel_x=np.zeros((numOfLines-1), dtype=float)
    vel_y=np.zeros((numOfLines-1), dtype=float)
    
    for i in range(1,numOfLines-1):
        if centroid_x[i] == -1  or centroid_y[i] == -1 or centroid_x[i-1] == -1  or centroid_y[i-1] == -1 or centroid_x[i] == 0  or centroid_y[i] == 0 or centroid_x[i-1] == 0  or centroid_y[i-1] == 0:
            disp_x[i]= ERROR_CONST
            disp_y[i]= ERROR_CONST
        else:
            disp_x[i]= centroid_x[i] - centroid_x[i-1] 
            disp_y[i]= centroid_y[i] - centroid_y[i-1] 
        
        dispCutOff=20.0
        if abs(disp_x[i]) > dispCutOff:
            print('disp_x[i] > %f: disp_x[%d]=%e' %(dispCutOff, i,disp_x[i]))
            disp_x[i]=ERROR_CONST
        
        if abs(disp_y[i]) > dispCutOff:
            print('disp_y[i] > %f: disp_y[%d]=%e' %(dispCutOff, i,disp_y[i]))
            disp_y[i]=ERROR_CONST
                    
        
        deltaT=1.0/FPS
        if disp_x[i] == ERROR_CONST or disp_y[i] == ERROR_CONST:
            vel_x[i] = ERROR_CONST
            vel_y[i] = ERROR_CONST
        else:
            vel_x[i] = (disp_x[i])/deltaT
            vel_y[i] = (disp_y[i])/deltaT            

        
        velocityCutOff=2000.0 #approx 60 mm /s
        if abs(vel_x[i]) > velocityCutOff:
            print('vel_x[i] > %f: vel_x[%d]=%e' %(velocityCutOff, i,vel_x[i]))
            vel_x[i]=ERROR_CONST
        
        if abs(vel_y[i]) > velocityCutOff:
            print('vel_y[i] > %f: vel_y[%d]=%e' %(velocityCutOff, i,vel_y[i]))
            vel_y[i]=ERROR_CONST
    #delete invalid entries
    imageCounter=np.arange(len(vel_x))
#    print('len(imageCounter) = %d, len(vel_x) = %d' %(len(imageCounter), len(vel_x)))
    for i in range(len(vel_x)-1, 0, -1):
        if vel_x[i] == ERROR_CONST or vel_y[i] == ERROR_CONST:
            vel_x=np.delete(vel_x, i)
            vel_y=np.delete(vel_y, i)
            imageCounter=np.delete(imageCounter, i)
    
    acceleration_x, acceleration_y, acceleration_mag = forwardDifferenc(vel_x, vel_y, imageCounter, FPS)
    
    speed=np.zeros((len(vel_x),1), dtype=float)
    speed_ave=np.zeros((len(vel_x),1), dtype=float)
    
    speed = np.sqrt( np.power( vel_x ,2) + np.power(vel_y ,2) )
#    speed = np.abs( vel_x ) + np.abs(vel_y) 
    speed_ave = tr.runningMean(speed, AVERAGINGWINDOW)
    speed_ave = np.array(speed_ave)
    
#    print('len(speed) = %d \t len(speed_ave) = %d' %(len(speed), len(speed_ave)))
    
    for i in range(AVERAGINGREPEATS):
        speed_ave=tr.runningMean(speed_ave, AVERAGINGWINDOW)
    
    return     disp_x, disp_y, vel_x, vel_y, speed, speed_ave, imageCounter, acceleration_x, acceleration_y, acceleration_mag

#==============================================================================   
#==============================================================================
#Constants
#==============================================================================
AVERAGINGWINDOW = 6
AVERAGINGREPEATS = 1
ERROR_CONST = -1

def analyisTwoCapsules(path,centerline, widthChannel, pPmm, FPS=64, Index=None, borderSize=10, debugInfo=True, closeAfterPlotting=False, geoCutOff=[0,0,0], plot=True):
    '''
    Read the centroid position of two capsules going through a T-Junction and
    measure their average distance between the capsules
    
    TODO: check way of calculating acceleration
    '''    
    if debugInfo:
        print('Running for %s' %(path[path[:-3].rfind('\\'):]))
        
    c1= '#253494'
    c2= '#2c7fb8'
    c3= '#41b6c4'
    c4= '#a1dab4'
            
    centerline += borderSize
    
    fileID=tr.find_batchName(path);
    centroid_x1, centroid_y1, v_x1, v_y1, area1, width1, d12_1, _ = readResultsFile(path) 
    centroid_x2, centroid_y2, v_x2, v_y2, area2, width2, d12_2, _ = readResultsFile(path, second=True) 
    
    numOfLines = len(centroid_x1)
    disp_x1, disp_y1, vel_x1, vel_y1 , speed1, speed_ave1, imageCounter1, acceleration_x1, acceleration_y1, acceleration_mag1 = findAccelerationFromPosition(centroid_x1, centroid_y1, FPS)
    disp_x2, disp_y2, vel_x2, vel_y2 , speed2, speed_ave2, imageCounter2, acceleration_x2, acceleration_y2, acceleration_mag2 = findAccelerationFromPosition(centroid_x2, centroid_y2, FPS)
    
    ave_acceleration_mag1=tr.runningMean(acceleration_mag1, AVERAGINGWINDOW)
    ave_acceleration_mag2=tr.runningMean(acceleration_mag2, AVERAGINGWINDOW) 
    
    for kk in range(4):
        ave_acceleration_mag1=tr.runningMean(ave_acceleration_mag1, AVERAGINGWINDOW)
        ave_acceleration_mag2=tr.runningMean(ave_acceleration_mag2, AVERAGINGWINDOW)
        speed_ave1=tr.runningMean(speed_ave1, AVERAGINGWINDOW)
        speed_ave2=tr.runningMean(speed_ave2, AVERAGINGWINDOW)
        
    ave_acceleration_mag1_v2, _, _=forwardDifferenc(speed_ave1, speed_ave1, imageCounter1, FPS)
    ave_acceleration_mag2_v2, _, _=forwardDifferenc(speed_ave2, speed_ave2, imageCounter2, FPS)
    
    #==========================================================================
    #==========================================================================
    #Find the distance between capsules
    #==========================================================================
    
    distance=np.zeros((numOfLines), dtype=float)

    for hh in range(numOfLines):
        if centroid_x1[hh] != ERROR_CONST and centroid_x2[hh] != ERROR_CONST:
            distance[hh] = np.sqrt((centroid_x1[hh] - centroid_x2[hh])**2 + (centroid_y1[hh] - centroid_y2[hh])**2)
        else:
            distance[hh] = ERROR_CONST
            
    dDdt, _, _=forwardDifferenc(distance, distance, np.arange(numOfLines), 1.0)
    
    distanceSteady=[]
    steadyNum=[]
    for hh in range(numOfLines):
        if abs(dDdt[hh]) <= 0.1 and distance[hh]>0:
            distanceSteady.append(distance[hh])
            steadyNum.append(hh)
    distanceSteady=np.array(distanceSteady); steadyNum = np.array(steadyNum)
    #ASSUMPTION: the first steady state is in the main chanel, the last in the 
    #daugther channel
    imagesDifference=40
    uniqueSteadyDistancesRounded=[]
    steadyNumR=[]
    for nn in range(len(distanceSteady)):
        tempRoundedValue = np.round(distanceSteady[nn])
#        print('nn = %d \t value = %f, in array = %s' %(nn, tempRoundedValue, tempRoundedValue in uniqueSteadyDistancesRounded))
        if tempRoundedValue in uniqueSteadyDistancesRounded:
            index = uniqueSteadyDistancesRounded.index(tempRoundedValue)
            if abs(steadyNum[nn] - steadyNum[index]) > imagesDifference:
                uniqueSteadyDistancesRounded.append(tempRoundedValue)
                steadyNumR.append(steadyNum[nn])
        else:
            uniqueSteadyDistancesRounded.append(tempRoundedValue)
            steadyNumR.append(steadyNum[nn])
            
            
#    print(uniqueSteadyDistancesRounded)
#    print(steadyNumR)
    #merge those that are close together
    oneFound = True
    while oneFound:
        oneFound=False
        for tt in range(len(uniqueSteadyDistancesRounded)-1, 0, -1): 
#            print('tt = %d' %tt, end="")
            if abs(uniqueSteadyDistancesRounded[tt]-uniqueSteadyDistancesRounded[tt-1]) <= 4.0 and  abs(steadyNumR[tt] - steadyNumR[tt-1]) <=imagesDifference:
#                print('\t %.0f and %.0f' %(uniqueSteadyDistancesRounded[tt],uniqueSteadyDistancesRounded[tt-1]))
                tempValue = (uniqueSteadyDistancesRounded[tt]+uniqueSteadyDistancesRounded[tt-1])/2
                uniqueSteadyDistancesRounded[tt-1] = (tempValue)
                steadyNumR[tt-1] = (steadyNumR[tt] + steadyNumR[tt-1])/2.0
                del uniqueSteadyDistancesRounded[tt]
                del steadyNumR[tt]
    print(uniqueSteadyDistancesRounded)
    
    if len(uniqueSteadyDistancesRounded) >= 2:
        distanceMainChannel = uniqueSteadyDistancesRounded[0]
        distanceDaugtherChannel = uniqueSteadyDistancesRounded[-1]
        print('distanceMainChannel = %.0f \t distanceDaugtherChannel = %.0f' %(distanceMainChannel, distanceDaugtherChannel ))
    elif len(uniqueSteadyDistancesRounded) == 1:
        distanceMainChannel = uniqueSteadyDistancesRounded[0]
        distanceDaugtherChannel = ERROR_CONST
        print('distanceMainChannel = %.0f \t distanceDaugtherChannel = %.0f' %(distanceMainChannel, distanceDaugtherChannel ))
    else:
        distanceMainChannel = ERROR_CONST
        distanceDaugtherChannel = ERROR_CONST
        print('No steady state distance found!' )
        
    #==========================================================================
    #==========================================================================
    #Find whether capsules went right or left and centering
    #==========================================================================
    
    #Select Non-Zero parts
    in1=[]; cx1=[]; cy1=[];  in2=[]; cx2=[]; cy2=[]; 
    
    for kk in range(numOfLines):
        if centroid_x1[kk] != ERROR_CONST:
            cx1.append(centroid_x1[kk])
            cy1.append(centroid_y1[kk])
            in1.append(kk)
        if centroid_x2[kk] != ERROR_CONST:
            cx2.append(centroid_x2[kk])
            cy2.append(centroid_y2[kk])
            in2.append(kk)
    print('inital length %d now %d and %d' %(numOfLines, len(cx1), len(cx2)))
    
    #take the region between 5 and 15% to be in the main channel and 85-95% in 
    # the daugther channel

    mStart = 0.05
    mEnd = 0.15
    dStart = 0.88
    dEnd = 0.98
    if Index == None:
        x_mainC1= cx1[int(mStart*len(cx1)):int(mEnd*len(cx1))]
        y_mainC1= cy1[int(mStart*len(cx1)):int(mEnd*len(cx1))]
        x_mainC2= cx2[int(mStart*len(cx2)):int(mEnd*len(cx2))]
        y_mainC2= cy2[int(mStart*len(cx2)):int(mEnd*len(cx2))]
        inm1= in1[int(mStart*len(cx2)):int(mEnd*len(cx2))]
        inm2= in2[int(mStart*len(cx2)):int(mEnd*len(cx2))]
        
        x_dC1= cx1[int(dStart*len(cx1)):int(dEnd*len(cx1))]
        y_dC1= cy1[int(dStart*len(cx1)):int(dEnd*len(cx1))]
        x_dC2= cx2[int(dStart*len(cx2)):int(dEnd*len(cx2))]
        y_dC2= cy2[int(dStart*len(cx2)):int(dEnd*len(cx2))]
        ind1= in1[int(dStart*len(cx1)):int(dEnd*len(cx1))]
        ind2= in2[int(dStart*len(cx2)):int(dEnd*len(cx2))]
    else:
        assert(len(Index == 8))
        x_mainC1= cx1[Index[0]:Index[1]]
        y_mainC1= cy1[Index[0]:Index[1]]
        x_mainC2= cx2[Index[4]:Index[5]]
        y_mainC2= cy2[Index[4]:Index[5]]
        
        x_dC1= cx1[Index[2]:Index[3]]
        y_dC1= cy1[Index[2]:Index[3]]
        x_dC2= cx2[Index[6]:Index[7]]
        y_dC2= cy2[Index[6]:Index[7]]
#    
    centering1 = centerline - np.average(np.array(x_mainC1))
    centering2 = centerline -np.average(np.array(x_mainC2))
    d1=np.average(np.array(x_dC1))
    d2=np.average(np.array(x_dC2))
    
    if  d1> centerline:
        turned1='right'
    else:
        turned1='left'
        
    if d2 > centerline:
        turned2='right'
    else:
        turned2='left'
    
    if turned1 != turned2 and debugInfo:
        print('Capsule went opposite ways!')
    if debugInfo:
        print('d1 = %f, d2 = %f and centerline = %f ' %(d1, d2, centerline))
         
    imageCounter1
    speed_ave_M1=[]
    inM1=[]
    for i in inm1:
        if i in imageCounter1:
            ind = np.where(imageCounter1==i)[0][0]
            if ind != -1:
                speed_ave_M1.append(speed_ave1[ind])
                inM1.append(i)
            
    speed_ave_D1=[]
    inD1=[]
    for i in ind1:
        if i in imageCounter1:
            ind = np.where(imageCounter1==i)[0][0]
            if ind != -1:
                speed_ave_D1.append(speed_ave1[ind])
                inD1.append(i)
    speed_ave_M2=[]
    inM2=[]
    for i in inm2:
        if i in imageCounter2:
            ind = np.where(imageCounter2==i)[0][0]
            if ind != -1:
                speed_ave_M2.append(speed_ave2[ind])
                inM2.append(i)
    speed_ave_D2=[]
    inD2=[]
    for i in ind2:
        if i in imageCounter2:
            ind = np.where(imageCounter2==i)[0][0]
            if ind != -1:
                speed_ave_D2.append(speed_ave2[ind])
                inD2.append(i)

    speed_ave_M1= np.array(speed_ave_M1); speed_ave_D1= np.array(speed_ave_D1); speed_ave_M2= np.array(speed_ave_M2); speed_ave_D2= np.array(speed_ave_D2);
    speedMain1 =np.average(speed_ave_M1)
    speedDaugther1 =np.average(speed_ave_D1)
    speedMain2 =np.average(speed_ave_M2)
    speedDaugther2 =np.average(speed_ave_D2)

    #==========================================================================
    #Find the maximal extend and the maximal Taylor deformation parameter
    #Find max Taylor deformation parameter and read Taylor deformation parameter     
    #==========================================================================
    if Index == None:
        d12Short1=d12_1[inm1[-1]:ind1[0]]
        widthShort1=width1[inm1[-1]:ind1[0]]
        d12Short2=d12_2[inm2[-1]:ind2[0]]
        widthShort2=width2[inm2[-1]:ind2[0]]
    else:
        d12Short1=d12_1[Index[1]:Index[2]]
        widthShort1=width1[Index[1]:Index[2]]
        d12Short2=d12_2[Index[5]:Index[6]]
        widthShort2=width2[Index[5]:Index[6]]
        
    maxd12_1=np.max(d12Short1)
    maxwidth1=np.max(widthShort1)
    maxd12_2=np.max(d12Short2)
    maxwidth2=np.max(widthShort2)
    
    
        
    #==========================================================================
    #==========================================================================
    #Plot results
    #==========================================================================
    if plot:
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax = fig.add_subplot(111)
#        plt.plot(imageCounter1, ave_acceleration_mag1/pPmm, 's', color =c1,label='Acceleration Capsule 1', markersize=4)
#        plt.plot(imageCounter2, ave_acceleration_mag2/pPmm, 'o', color =c3,label='Acceleration Capsule 2', markersize=4)
        
        plt.plot(imageCounter1, ave_acceleration_mag1_v2/pPmm, 's', color =c2,label='Acceleration Capsule 1 mk.2', markersize=4)
        plt.plot(imageCounter2, ave_acceleration_mag2_v2/pPmm, 'o', color =c4,label='Acceleration Capsule 2 mk.2', markersize=4)

        plt.title("Acceleration" +" " + fileID)
        plt.ylabel("Acceleration [$mm/s^2$]")
        plt.xlabel("Picture Number [FPS = %d]" %FPS)
        plt.legend(loc=2, fontsize=6)
        plt.savefig(path+fileID+"_Acceleration_Graph.jpg")
        
        if closeAfterPlotting:
             plt.clf(); plt.close(fig); 
             
    if plot:
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax = fig.add_subplot(111)
        plt.plot(imageCounter1, speed_ave1/pPmm, 's', color =c1,label='Speed Capsule 1', markersize=4)
        plt.plot(imageCounter2, speed_ave2/pPmm, 'o', color =c3,label='Speed Capsule 2', markersize=4)
        
        plt.plot(inM1, speed_ave_M1/pPmm, '^', color ='y',label='Speed Capsule 1', markersize=3)
        plt.plot(inD1, speed_ave_D1/pPmm, '^', color ='y',label='Speed Capsule 1', markersize=3)
        
        plt.plot(inM2, speed_ave_M2/pPmm, '<', color ='g',label='Speed Capsule 2', markersize=3)
        plt.plot(inD2, speed_ave_D2/pPmm, '<', color ='g',label='Speed Capsule 2', markersize=3)
 

        plt.title("Speed" +" " + fileID)
        plt.ylabel("Speed [$mm/s$]")
        plt.xlabel("Picture Number [FPS = %d]" %FPS)
        plt.legend(loc='best', fontsize=6)
        plt.savefig(path+fileID+"_Speed_Graph.jpg")
        
        if closeAfterPlotting:
             plt.clf(); plt.close(fig);
    
    if plot:
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax = fig.add_subplot(111)
        plt.plot(np.arange(numOfLines), distance/pPmm, 's', color =c1,label='Distance', markersize=4)
        plt.plot(np.arange(numOfLines), dDdt/pPmm, 'o', color =c4,label='d Distance/ dt', markersize=4)
        plt.plot(steadyNum, distanceSteady/pPmm, 's', color =c2,label='Steady Distance', markersize=4)

        plt.title("Seperation Distance" +" " + fileID)
        plt.ylabel("Distance[$mm$]")
        plt.xlabel("Picture Number [FPS = %d]" %FPS)
        plt.legend(loc=2, fontsize=6)
        plt.savefig(path+fileID+"_Distance_Graph.jpg")
        
        if closeAfterPlotting:
             plt.clf(); plt.close(fig);
             
    if plot:
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax3 = fig.add_subplot(111)
        plt.plot(x_mainC1, y_mainC1, 's', color=c1,label='Capsule1: Centroid Poisition', markersize=5)
        plt.plot(x_mainC2, y_mainC2, 'o', color=c3,label='Capsule2: Centroid Poisition', markersize=5)

        plt.plot([centerline, centerline], [0, np.max(y_mainC1)], '-m',label='Centre', linewidth=4, markersize=5)
        plt.plot([centerline-centering1, centerline-centering1], [0, np.max(y_mainC1)], '-.', color=c2, label='Capsule1: Average Position',linewidth=2,  markersize=5)
        plt.plot([centerline-centering2, centerline-centering2], [0, np.max(y_mainC2)], '-.', color=c4, label='Capsule2: Average Position',linewidth=2,  markersize=5)
        
        s = "Centreline at = %.1f \n" \
            "Capsule 1: Average x= %.1f, Difference = %.1f, turned %s \n" \
            "Capsule 2: Average x= %.1f, Difference = %.1f, turned %s" %(centerline, centerline - centering1, centering1,  turned1, centerline - centering2,centering2,  turned2)
        
        ax3.text(centerline-2*pPmm, np.max(y_mainC1)*0.4, s, fontsize=12)
            
        plt.xlim(centerline-2*pPmm, centerline+2*pPmm)
        plt.title("Centering of "+" " + fileID)
        plt.xlabel("X-Position [pixels]")
        plt.ylabel("Y-Position [pixels]")
        plt.legend(loc=2, fontsize=6)
        plt.show()
        plt.savefig(path+fileID+"_Centering_Graph.jpg")
        if closeAfterPlotting:
             plt.clf(); plt.close(fig);
             
             
    #==========================================================================
    #Find volumn Flux
#    print(path)
    name=path[:-2]
    d1=name.find('mlPmin')
    d2=name[:d1].rfind('_')
#    print('d1=%d d2 = %d' %(d1, d2))
    if d2 ==-1 or (d1-d2)>20:
        d2 = name[:d1].rfind('-')
    d3=name[d2:d1].find('m')
    if d3==-1:
        volFlux=name[d2+1:d1]
    else:
#        print('d3= %d' %d3)
#        print(name[d2+1:d2+d3])
        volFlux=name[d2+1:d2+d3]
#    print('Name: %s \nVolumn Flux = %s' %(name, volFlux))
    volFlux = volFlux.replace("p", ".")
#    print('volFlux = %s' %volFlux)
    volFlux=float(volFlux)
    print('volFlux = %f' %volFlux)
  
    #==========================================================================
    # Writting output to file in a recovarable way    
    #==========================================================================
    if platform.system() == 'Linux':
        dSlash='/'
    elif platform.system() == 'Windows': 
        dSlash='\\'
    else:
        print('Unknow Oporating System - find_batchName(path) - failed')
    ss1=path.rfind(dSlash, 1,-1)
    ss2=path.rfind(dSlash, 1,ss1)
    ss3=path.rfind(dSlash, 1,ss2)
    pathData= path[0:ss1] + dSlash + path[ss3+1:ss2]+'-'+path[ss2+1:ss1]+'_ResultsTwoCapsules.txt'
    pathParameters= path[0:ss1] + dSlash + path[ss3+1:ss2]+'_ParametersTwoCapsules.txt'

    #File 1: Data
    import os.path
    if not os.path.isfile(pathData): #check whether the file for this run has been started
        fileData = open(pathData, 'w')
        fileData.write('Vol Flux \tname \t\t\t\t\t\t distance Main \t distance Daugther \t\t Capsule 1: Speed Main \t Speed Daugther \t Off-centre \t turned \t max width \t max d12 \t\t Capsule 2: Speed Main \t Speed Daugther \t Off-centre \t turned \t max width \t max d12\n')
        fileData.close()
    if not os.path.isfile(pathParameters):
        fileParameters = open(pathParameters, 'w')
        fileParameters.write('fileID \t\t\t\t\t\t\tcenterline \tIndex \twidth \tpPmm \tgeometryTJ\n')
        fileParameters.close()
        
    s1 = '%.1f \t %s \t  %.2e \t %.2e' %(volFlux, fileID, distanceMainChannel,  distanceDaugtherChannel) 
    s2 = '\t %.3f \t %.3f \t %.3f \t%s \t%d \t%.3f' %(speedMain1,speedDaugther1,  centering1, turned1,maxwidth1, maxd12_1)
    s3 = '\t %.3f \t %.3f \t %.3f \t%s \t%d \t%.3f ' %(speedMain2, speedDaugther2, centering2, turned2, maxwidth2, maxd12_2)
    results = s1+s2+s3+'\n'
    #check whether there is alread a value for this fileID
    if fileID in open(pathData).read():
         #File 1: Data
        f = open(pathData,"r")
        lines = f.readlines()
        f.close()
        
        fileData = open(pathData, 'w')
        for line in lines:
            if fileID in line:
                fileData.write(results)
            else:
                fileData.write(line)        
                
    else: #if this hasn't been written to file before, simple append it to the end
         #File 1: Data
        fileData = open(pathData, 'a')
        fileData.write(results)
        fileData.close()
    
    if Index == None:
        parameters = '%s \t %d \t %d \t %d \t %d \t %d \t %d \t %d \t %d \t %f \t %f \t %f \t %d \t %d \t %d \n' %(fileID, -1, -1, -1, -1, -1, -1, -1, -1, centerline, widthChannel, pPmm, geoCutOff[0], geoCutOff[1], geoCutOff[2])
    else:
        parameters = '%s \t %d \t %d \t %d \t %d \t %d \t %d \t %d \t %d \t %f \t %f \t %f \t %d \t %d \t %d \n' %(fileID, Index[0], Index[1], Index[2], Index[3], Index[4], Index[5], Index[6], Index[7], centerline, widthChannel, pPmm, geoCutOff[0], geoCutOff[1], geoCutOff[2])
        
    if fileID in open(pathParameters).read():
        #File 2: Parameters
        f2 = open(pathParameters,"r")
        lines = f2.readlines()
        f2.close()       

        fileParameters = open(pathParameters, 'w')
        for line in lines:
            if fileID in line:
                fileParameters.write(parameters)
            else:
                fileParameters.write(line) 
    else:
        #File 2: Parameters
        fileParameters = open(pathParameters, 'a')
        fileParameters.write(parameters)
        fileParameters.close()
    
#==============================================================================
#============================================================================== 
def findSpeedGradient(path,centerline, widthChannel, pPmm, FPS=64, Index=None, UseEverySecond=False, borderSize=10, debugInfo=True, closeAfterPlotting=False, geoCutOff=[], plot=True, ignorlastSym=None):
    '''
    geoCutOff = [Top Daugther Channel, Bottom Daugther Channel, left side Main Channel, right side Main Channel]
    '''
    if debugInfo:
        print(Index)
    
    fileID=tr.find_batchName(path);
    centroid_x, centroid_y, v_x, v_y, area, width, d12, _ = readResultsFile(path)  
    numOfLines=len(centroid_x)           
    
    #Running average
    aveWindow=AVERAGINGWINDOW
    repeatAveraging=AVERAGINGREPEATS

    #geometric 
    #find time in Junction from Centroid position
    print(geoCutOff)
    ylimit=geoCutOff[1]+borderSize
    xlimitLeft=geoCutOff[2]+borderSize
    xlimitRight=geoCutOff[3]+borderSize
    
    enterTJGeometric=0    
    leaveTJGeomtric=0
    count=0
    for ii in range(0,numOfLines):
        if centroid_y[ii] < ylimit and centroid_y[ii] >5 and centroid_x[ii] > xlimitLeft and centroid_x[ii] < xlimitRight:
            if count == 0:
                enterTJGeometric=ii
            count += 1
            leaveTJGeomtric=ii
    timeTJ=count/FPS+0.0
    
    
    disp_x, disp_y, vel_x, vel_y , speed, speed_ave, imageCounter, acceleration_x, acceleration_y, acceleration_mag = findAccelerationFromPosition(centroid_x, centroid_y, FPS)
    ave_acceleration_mag=tr.runningMean(acceleration_mag, aveWindow)
    
    if UseEverySecond:
        #select every second entry
        speed=speed[::2]
        speed_ave=speed_ave[::2]
        v_x=v_x[::2]
        v_y=v_y[::2]
        FPS=FPS/2
    
#    dx=dx[::2]
#    ave_dx=ave_dx[::2]
#    zx=zx[::2]
    
    #identify different regions
    dx = tr.gradient(speed_ave, h=1/FPS)
    zx=imageCounter[2:-2]
    if debugInfo:
        print('len(zx) = %f \t len(dx) = %f ' %(len(zx), len(dx)))
    
    ave_dx=tr.runningMean(dx, aveWindow) 
    for i in range(repeatAveraging):
        ave_dx=tr.runningMean(ave_dx, aveWindow)
    
    l_dx=len(ave_dx)
    if Index == None:
        #ignore first short and last short
        ignorBeginning=0.15
        short=ignorBeginning
        ignorEnd=0.20
        ave_dxs=ave_dx[round(l_dx*ignorBeginning):-round(l_dx*ignorEnd)]
        zx2=zx[round(l_dx*ignorBeginning):-round(l_dx*ignorEnd)]
    else:
        short=-1
        ave_dxs=ave_dx[Index[1]:Index[2]]
        zx2=zx[Index[1]:Index[2]]

    #find maximum and minimum
    max_dx=np.zeros((len(dx),1), dtype=float)
    max_dx.fill(np.max(ave_dxs))
    
    min_dx=np.zeros((len(dx),1), dtype=float)
    min_dx.fill(np.min(ave_dxs))
    
    startThres=0.2
    endThres=0.2
    startIndex=np.where(ave_dxs < np.min(ave_dxs) * startThres)
    endIndex=np.where(ave_dxs > np.max(ave_dxs) * endThres)
    
    steadyStateLostOnFrame = zx2[startIndex[0][0]]
    steadyStateReachedOnFrame = zx2[endIndex[0][-1]] 
    timeInTJunction=(zx2[endIndex[0][-1]]-zx2[startIndex[0][0]])*(1/FPS)
    
    differenceTimeStart = (steadyStateLostOnFrame - enterTJGeometric)/FPS
    differenceTimeEnd = (steadyStateReachedOnFrame - leaveTJGeomtric)/FPS
    print("Time in T-Junction = " +str(timeInTJunction)+" s  with differenceTimeStart = " 
        +str(differenceTimeStart) + ' differenceTimeEnd: ' + str(differenceTimeEnd ) 
        )
    
    if plot:
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax = fig.add_subplot(111)
        plt.plot(zx, dx, 'oc',label='Gradient Speed', markersize=5)
        plt.plot(zx, ave_dx, 'sr',label='Average Gradient Speed', markersize=5)
        plt.plot(zx2, ave_dxs, '^y',label='Average Gradient Speed Short', markersize=5)
#        print(str(len(imageCounter)) + ' ' + str(len(acceleration_mag)))
        plt.plot(imageCounter, ave_acceleration_mag, 'hg',label='Acceleration Mk. 2', markersize=3)
        
        plt.plot(zx, max_dx, '-k')
        plt.plot(zx, min_dx, '-k')
        
        plt.plot([zx2[startIndex[0][0]], zx2[startIndex[0][0]]], [ min_dx[0], max_dx[0]],  '-r', linewidth=2)
        plt.plot([zx2[endIndex[0][-1]], zx2[endIndex[0][-1]]], [ min_dx[0], max_dx[0]],  '-r', linewidth=2)
        
        s = "Time in T-Junction = %.2e s" %timeInTJunction
        s1= "Threshold for decrease = %.2f" % (startThres)
        s2= "Threshold for increase = %.2f" % (endThres)
        
        ax.text(l_dx/2.2, min_dx[0]/2, s, fontsize=15)
        ax.text(l_dx/2.2, min_dx[0]/1.4, s1, fontsize=12)
        ax.text(l_dx/2.2, min_dx[0]/1.05, s2, fontsize=12)
        
    #    plt.ylim([-50,50])
        
        plt.title("Gradient of the Speed" +" " + fileID)
        plt.xlabel("dx")
        plt.xlabel("Picture Number [FPS = %d]" %FPS)
        plt.legend(loc=2, fontsize=6)
        plt.savefig(path+fileID+"_GradientSpeed_Graph.jpg")
        
        if closeAfterPlotting:
             plt.clf(); plt.close(fig); 
    
    x1=np.arange(len(speed_ave))
    #timescale in the junction velocity minimum, etc. 
    
    minSpeed=np.min(speed_ave[int(0.1*len(speed_ave)):int(0.8*len(speed_ave))])
    maxSpeed=np.max(speed_ave[int(0.1*len(speed_ave)):int(0.8*len(speed_ave))])
    
    imagesdispx=np.arange(len(speed_ave))
    if Index==None:
        speed_MainChannel=speed_ave[round(len(x1)*ignorBeginning):startIndex[0][0]]
        speed_DaugtherChannel = speed_ave[endIndex[0][-1]+round(l_dx*short)*2:-round(len(x1)*ignorEnd)]        
        xMain = imagesdispx[round(len(x1)*ignorBeginning):startIndex[0][0]]
        xDaugther = imagesdispx[endIndex[0][-1]+round(l_dx*short)*2:-round(len(x1)*ignorEnd)]   

    else:
        speed_MainChannel=speed_ave[Index[0]:Index[1]]
        speed_DaugtherChannel = speed_ave[Index[2]:Index[3]]  
        xMain = imagesdispx[Index[0]:Index[1]]
        xDaugther  = imagesdispx[Index[2]:Index[3]]
                
    firstSpeed=np.average(speed_MainChannel)
    secondSpeed=np.average(speed_DaugtherChannel)
#    print('index 1 = ' + str(endIndex[0][-1]+round(l_dx*short)*2) + ' \t index 2 = ' + str(-round(len(x1)*short)))
    
    if Index == None:
        centreing=np.average(centroid_x[round(len(x1)*short):startIndex[0][0]])
    else:
        centreing=np.average(centroid_x[Index[0]:Index[1]])
        
    if debugInfo:
        print('Centering = %f' %centreing)     
    if plot:
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        plt.plot(imagesdispx, speed_ave, 'sb',label='Speed Averaged', markersize=5)
        plt.plot(imagesdispx, speed, 'or',label='Speed', markersize=5)
        
        plt.plot(xMain, speed_MainChannel, '<y',label='Main Channel', markersize=4)
        plt.plot(xDaugther, speed_DaugtherChannel, '>g',label='Daugther Channel', markersize=4)
        
        plt.plot([ 0, len(speed_ave)], [firstSpeed,firstSpeed], '--k', linewidth=1)
        plt.plot( [ 0, len(speed_ave)], [secondSpeed,secondSpeed], '-.k', linewidth=1)
        
        s = "min Speed= %.2e pixels/s" %minSpeed
        s1= "ave main channel = %.2e pixels/s" % (firstSpeed)
        s2= "ave main daugther = %.2e pixels/s" % (secondSpeed)
        
        ax2.text(len(x1)/1.8, maxSpeed/2, s, fontsize=15)
        ax2.text(len(x1)/1.8, maxSpeed/3, s1, fontsize=12)
        ax2.text(len(x1)/1.8, maxSpeed/4, s2, fontsize=12)
        
        
        plt.title("Speed"+" " + fileID)
        plt.xlabel("# ")
        plt.ylabel("Speed[pixels/s]")
        plt.legend(loc=1, fontsize=6)
        plt.ylim([0,np.max(speed_ave)*1.2])
        plt.savefig(path+fileID+"_SpeedWImageNumber_Graph.jpg")
        if closeAfterPlotting:
             plt.clf(); plt.close(fig);

    
    xv_x=np.arange(len(v_x))

    #Check centering of capusle - assume first half is in main channel
    cutOff=0.1 #cut of 10% either side
    leng=len(centroid_x)
    
    if Index == None:
        x_mainC= centroid_x[cutOff*leng:(0.5-cutOff)*leng]
        y_mainC= centroid_y[cutOff*leng:(0.5-cutOff)*leng]
    else:
        x_mainC= centroid_x[Index[0]:Index[1]]
        y_mainC= centroid_y[Index[0]:Index[1]]
        
    #eliminate zero zero positionsignorlastSym
    for i in range(len(x_mainC)-1,-1,-1):
        if     x_mainC[i] == -1.0  or y_mainC[i] == -1.0 or x_mainC[i] == -1  or y_mainC[i] == -1:
            lenBefore=len(x_mainC)
            x_mainC=np.delete(x_mainC, i)
            y_mainC=np.delete(y_mainC, i)
            lenAfter=len(x_mainC)

    for kk in range(len(x_mainC)-1, -1, -1):
        if x_mainC[kk] <1:
            x_mainC =np.delete(x_mainC , kk)
            y_mainC =np.delete(y_mainC , kk)
            

    aveX=np.average(x_mainC)  
    differenceX=aveX-centerline
    
    #check whether it goes left or right
    cx=centroid_x.copy()
    cx[cx != -1]
    aveXdaugtherChannel=np.average(cx[(0.5+cutOff)*leng: (1-cutOff)*leng])
               #[a != 0]
    
    if aveXdaugtherChannel > centerline:
        turn='right'
    else:
        turn='left'
        
        
    if plot:
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax3 = fig.add_subplot(111)
        plt.plot(x_mainC, y_mainC, 'sb',label='Centroid Poisition', markersize=5)
        plt.plot([centerline, centerline], [0, np.max(y_mainC)], '-m',label='Centre', linewidth=4, markersize=5)
        plt.plot([aveX, aveX], [0, np.max(y_mainC)], '-.c',label='Average Position',linewidth=4,  markersize=5)
        
        s = "Centreline at = %.1f \n  Average x-position = %.1f  \n Difference = %.1f \n turned %s" %(centerline, aveX, differenceX, turn)
        
        ax3.text(centerline + differenceX*0.1, np.max(y_mainC)*0.4, s, fontsize=12)
            
        plt.xlim(centerline-2*pPmm, centerline+2*pPmm)
        plt.title("Centering of "+" " + fileID)
        plt.xlabel("X-Position [pixels]")
        plt.ylabel("Y-Position [pixels]")
        plt.legend(loc=2, fontsize=6)
        plt.show()
        plt.savefig(path+fileID+"_Centering_Graph.jpg")
        if closeAfterPlotting:
             plt.clf(); plt.close(fig);
        
    
    
    
    #==========================================================================
    #Find the maximal extend and the maximal Taylor deformation parameter
    #Find max Taylor deformation parameter and read Taylor deformation parameter     
    #==========================================================================
    if Index == None:
        d12Short=d12[ignorBeginning*len(d12):(1-ignorEnd)*len(d12)]
        widthShort=width[ignorBeginning*len(d12):(1-ignorEnd)*len(d12)]
    else:
        d12Short=d12[Index[1]:Index[2]]
        widthShort=width[Index[1]:Index[2]]
    maxd12=np.max(d12Short)
    maxwidth=np.max(widthShort)
        
    #find deformation in main and daugthe channel
    if Index==None:
        d12Main=(d12[round(len(x1)*ignorBeginning):startIndex[0][0]])
        d12Daugther = (d12[endIndex[0][-1]+round(l_dx*short)*2:-round(len(x1)*ignorEnd)] )       
    else:
        d12Main=(d12[Index[0]:Index[1]])
        d12Daugther = (d12[Index[2]:Index[3]] )  
        
    for hh in range(len(d12Main)-1,-1, -1):
        if d12Main[hh] == ERROR_CONST:
            d12Main = np.delete(d12Main, hh)
    for gg in range(len(d12Daugther)-1,-1, -1):
        if d12Daugther[gg] == ERROR_CONST:
            d12Daugther = np.delete(d12Daugther, gg)
    d12Main = np.average(d12Main); d12Daugther = np.average(d12Daugther);
    
    
    #==========================================================================
    #Measure Relaxation Time of Capsule after T-Junction    
    #==========================================================================
    framesToSS, distanceToSSPixels, _, _ =  findSymmetryByCentreline(path=path, geoTJ=geoCutOff, centroidAndWidth=[centroid_x, centroid_y, width], plot=True, show=True, show2=False, ignorlast=ignorlastSym)
    timeToSS = framesToSS / (FPS+0.0)
    distanceToSS = distanceToSSPixels / (pPmm+0.0)        
    
    #==========================================================================
    #Find volumn Flux
#    print(path)
    name=path[:-2]
    d1=name.find('mlPmin')
    d2=name[:d1].rfind('_')
#    print('d1=%d d2 = %d' %(d1, d2))
    if d2 ==-1 or (d1-d2)>20:
        d2 = name[:d1].rfind('-')
    d3=name[d2:d1].find('m')
    if d3==-1:
        volFlux=name[d2+1:d1]
    else:
#        print('d3= %d' %d3)
#        print(name[d2+1:d2+d3])
        volFlux=name[d2+1:d2+d3]
#    print('Name: %s \nVolumn Flux = %s' %(name, volFlux))
    volFlux = volFlux.replace("p", ".")
    print('volFlux = %s' %volFlux)
    volFlux=float(volFlux)
    print('volFlux = %f' %volFlux)
    
    print('Vol Flux \tname \t min speed \t ave speed 1 \t ave speed 2 \t time \t short \t threshold 1 \t threshold 2 \t Off-centre \t turned \t max width \t max d12 \t differenceTimeStart \t differenceTimeEnd \td12 Main \t d12 Daugther' )
    print('%.0f \t %s \t %.2e \t %.2e \t %.2e \t %.2e \t %.2f \t %.2f \t %.2f \t %.2f \t %s \t %.3e \t %d \t %.3f \t %.3e \t%.3e \t%.3f \t %.3f' %(volFlux, fileID, minSpeed, firstSpeed,  secondSpeed, timeInTJunction, short, startThres, endThres, differenceX, turn, timeTJ, maxwidth, maxd12, differenceTimeStart, differenceTimeEnd,d12Main, d12Daugther ))           
    
    #==========================================================================
    # Writting output to file in a recovarable way    
    #==========================================================================
    #TODO: use os module instead
    if platform.system() == 'Linux':
        dSlash='/'
    elif platform.system() == 'Windows': 
        dSlash='\\'
    else:
        print('Unknow Oporating System - find_batchName(path) - failed')
        
    #TODO: check why the same line gets written to file multiple times?
    ss1=path.rfind(dSlash, 1,-1)
    ss2=path.rfind(dSlash, 1,ss1)
    ss3=path.rfind(dSlash, 1,ss2)
    pathData= path[0:ss1] + dSlash + path[ss3+1:ss2]+'-'+path[ss2+1:ss1]+'_Results.txt';    dirData = path[0:ss1] + dSlash; nameData = path[ss3+1:ss2]+'-'+path[ss2+1:ss1]+'_Results.txt'
    pathParameters= path[0:ss1] + dSlash + path[ss3+1:ss2]+'_Parameters.txt'
    
#    print(pathData)
#    print('M:\\EdgarHaener\\Capsules\\RigidParticle-3.5mm\\31032015\\Rigid3p5mm-310315-30fps-10mlPmin-1\\workfile.txt')   
    
    #File 1: Data
    import os.path
    if not os.path.isfile(pathData): #check whether the file for this run has been started
        fileData = open(pathData, 'w')
        fileData.write('Vol Flux \t\t\t\t\t\tname \t min speed \t ave speed 1 \t ave speed 2 \t time acceleration  \ \t Off-centre \t turned \t time geometric \t max width \t max d12 \tdifferenceTimeStart \tdifferenceTimeEnd \td12 Main \t d12 Daugther \ttime to Steady State (seconds) \tdistance to Steady State(pixels)\n')
        fileData.close()
    if not os.path.isfile(pathParameters):
        fileParameters = open(pathParameters, 'w')
        fileParameters.write('fileID \t\t\t\t\t\tshort \t threshold 1 \t threshold 2 \t Pos \tcenterline \twidth \tpPmm \tgeometryTJ \t\tSymmetry-Ignore last points\n')
        fileParameters.close()
    
    #check whether there is alread a value for this fileID   
    stringWRslt = '%.1f \t %s \t \t \t %.2e \t %.2e \t %.2e  \t %.2f \t %.2f \t %s \t %.3e \t %d \t %.3f \t%.3e \t%.3e \t%.3f \t%.3f \t%.3f \t%.3f\n' %(volFlux, fileID, minSpeed, firstSpeed,  secondSpeed, timeInTJunction, differenceX, turn, timeTJ, maxwidth, maxd12, differenceTimeStart, differenceTimeEnd, d12Main, d12Daugther, timeToSS, distanceToSSPixels)
    if fileID in open(pathData).read():
         #File 1: Data
        f = open(pathData,"r")
        lines = f.readlines()
        f.close()
        
        fileData = open(pathData, 'w')
        for line in lines:
            if fileID in line:
                fileData.write( stringWRslt)
            else:
                fileData.write(line)      
        fileData.close()
                
    else: #if this hasn't been written to file before, simple append it to the end
         #File 1: Data
        fileData = open(pathData, 'a')
        fileData.write(stringWRslt)
        fileData.close()
    
    if ignorlastSym == None: ils=0
    else: ils = ignorlastSym
            

    if fileID in open(pathParameters).read():
        #File 2: Parameters
        f2 = open(pathParameters,"r")
        lines = f2.readlines()
        f2.close()       

        fileParameters = open(pathParameters, 'w')
        for line in lines:
            if fileID in line:
                if Index ==None:
                    fileParameters.write('%s \t  %.2e  \t %.2f \t %.2f \t %d \t %d \t %d \t %d \t %f \t %f \t %f \t %d \t %d \t %d \t %d \t %d\n' %(fileID, short, startThres, endThres, -1, -1, -1, -1, centerline, widthChannel, pPmm, geoCutOff[0], geoCutOff[1], geoCutOff[2], geoCutOff[3], ils))
                else:
                    fileParameters.write('%s \t  %.2e  \t %.2f \t %.2f \t %d \t %d \t %d \t %d \t %f \t %f \t %f \t %d \t %d \t %d \t %d \t %d\n' %(fileID, short, startThres, endThres, Index[0], Index[1], Index[2], Index[3], centerline, widthChannel, pPmm, geoCutOff[0], geoCutOff[1], geoCutOff[2], geoCutOff[3], ils))

            else:
                fileParameters.write(line) 
        fileParameters.close()
    else:
        #File 2: Parameters
        fileParameters = open(pathParameters, 'a')
        if Index ==None:
            fileParameters.write('%s \t  %.2e  \t %.2f \t %.2f \t %d \t %d \t %d \t %d \t %f \t %f \t %f \t %d \t %d \t %d \t %d \t %d\n' %(fileID, short, startThres, endThres, -1, -1, -1, -1, centerline, widthChannel, pPmm, geoCutOff[0], geoCutOff[1], geoCutOff[2], geoCutOff[3], ils))
        else:
            fileParameters.write('%s \t %.2e  \t %.2f \t %.2f \t %d \t %d \t %d \t %d \t %f \t %f \t %f \t %d \t %d \t %d \t %d \t %d\n' %(fileID, short, startThres, endThres, Index[0], Index[1], Index[2], Index[3], centerline, widthChannel, pPmm, geoCutOff[0], geoCutOff[1], geoCutOff[2], geoCutOff[3], ils))
        fileParameters.close()
        
    removeDuplicateLines(dirData, nameData)
    
    
def plotExtend(path):
    centroid_x, centroid_y, v_x, v_y, area, width, d12, height = readResultsFile(path, second=False)     
    plt.figure()
    x = np.arange(len(width))      
    plt.plot(x, width, 'bs', linestyle='None', label= ' Width')
    plt.plot(x, height, 'ro', linestyle='None',label= ' Height')
    plt.xlabel('Image Number')
    plt.ylabel('Extend [pixels]')
    plt.show()

def removeDuplicateLines(directory, filename):
    ''' For results files only '''
    #create backup
    backup = directory + 'tempBackup_RemoveDuplicateLines.txt'
    shutil.copyfile(directory + filename, backup)
    
    
    f = open(directory + filename,"r")
    lines = f.readlines()
    f.close()
    
    os.remove(directory + filename) #delete backup copy
    
    listOfNames=[]
    duplicates=0
    fileD = open(directory + filename, 'w')
    
    for line in lines:
        entriesLine=line.split('\t')     
        entriesLine[-1] = entriesLine[-1][:-2] #what am I doing here?
        name = entriesLine[1].strip() # 2nd entry is the name
        
        if not name in listOfNames:
            listOfNames.append(name)
            fileD.write(line) 
        else:
            duplicates += 1
            
    fileD.close()            
    os.remove(backup) #delete backup copy
    print('%d duplicates removed' %duplicates)
                

def wholeRun(directory, centerline, width, pPmm, Index=None, UseEverySecond=False, geometryTJ=None):
    """ Run the script for finding measurments on several folders"""
    import os
    import traceback
    import time
    listFolders=os.listdir(directory)
    indexDelet=[]
    for i in range(len(listFolders)):
        if os.path.isfile(directory+listFolders[i]):
            indexDelet.append(i)

    for i in range(len(indexDelet)-1, -1, -1):
        del listFolders[indexDelet[i]]

    for f in listFolders:
        plt.close('all')
        try:
            print('\n Starting \t %s \n' %f)
            indexfps=f.rfind('fps', 0, -1)
            indexfps=f.rfind('FPS', 0, -1)
            indexdash=f.rfind('-', 0, indexfps)
            FPS=float(f[indexdash+1:indexfps])
            if geometryTJ != None:
                findSpeedGradient(directory+f+'\\',centerline=centerline, width=width, pPmm=pPmm, FPS=FPS, Index=None, UseEverySecond=False, borderSize=10, debugInfo=True, closeAfterPlotting=True, geoCutOff=geometryTJ)
            else:
                findSpeedGradient(directory+f+'\\',centerline=centerline, width=width, pPmm=pPmm, FPS=FPS, Index=None, UseEverySecond=False, borderSize=10, debugInfo=True, closeAfterPlotting=True)
        except Exception:
            print('Didnt work for \t %s' %f)
            print(traceback.format_exc())
            
def dirWalk(topdir, copyDest, string, filetype):
    
    for dirName, subdirList, fileList in os.walk(topdir):
#        print('Found directory: %s' % dirName)
        for fname in fileList:
            if string in fname and filetype in fname:
                print(fname)
                fileLoc = dirName + os.sep +  fname
                shutil.copyfile(fileLoc, os.path.join(copyDest, fname))
                
#    for root, dirs, files in os.walk(".", topdown=True):
#        for name in files:
#            if string in name and filetype in name:
#                print(name)
#        for folders in dirs:
#            dirWalk(folders, copyDest, string, filetype)

            
#    os.path.walk(topdir, step, exten)


    
def runFunction():
    plt.close("all")

    
#    directory = 'M:\\EdgarHaener\\Capsules\\Batch170615-002\\T-Junction\\2015-06-22\\Batch170615-002_#2\\'
#    path=directory + 'Batch170615-002-#2-100FPS-50mlPmin-4\\'
    
    FPS=10
    
#    directory = 'M:\\EdgarHaener\\Capsules\\Batch270715-001\\T-Junction\\2015-08-04\\Batch270715-001-#5\\'
#    folder =  'Batch270715-001-#5-%dFPS-15mlPmin-4\\' %FPS
#    directory = 'M:\\EdgarHaener\\Capsules\\Batch040615-002\\T-Junction\\'

#    directory = 'M:\\EdgarHaener\\Capsules\\Batch040615-002\\T-Junction\\Capsule#1\\'
#    folder =  'Batch040615-002-#1-1S-5kcSt-%dFPS-35mlPmin-8\\' %FPS

    directory = 'M:\\EdgarHaener\\Capsules\\Batch120615-004\\T-Junction\\'
    folder =  'Batch120615-001-#4-%dFPS-5mlPmin-9\\' %FPS

    path = directory + folder

#    centerline, width, pPmm, geometryTJ = None, None, None, None
#    directory = 'M:\\EdgarHaener\\Capsules\\GelBeads150715-1\\T-Junction\\2015-07-22\\GelBead150715-1-#4\\'; geometryTJ=[121, 535, 709] #GelBeads150715-1 
#    directory = 'M:\\EdgarHaener\\Capsules\\GelBeads150730-1\\T-Junction\\2015-08-04\\GelBead150730-1-#1\\'; centerline, width, pPmm = 624.5, 175, 22.4; geometryTJ=[119, 537, 712] #GelBeads150730-1 #1
#    centerline, width, pPmm = 646, 174, 22.3; geometryTJ=[114, 559,  733] #Batch260615-001 #17
#    centerline, width, pPmm = 635.5, 173, 22.2; geometryTJ=[38, 122, 549,  722] #Batch040615-002
#    centerline, width, pPmm = 637, 175, 22.4; geometryTJ=[72, 159, 550,  725] #Batch120615-004 #4 15ml/min
    centerline, width, pPmm = 637, 175, 22.4; geometryTJ=[35, 118, 549,  724] #Batch120615-004 #4 Other Runs
#    centerline, width, pPmm = 631.5, 175, 22.4; geometryTJ=[158, 544,  719] #Batch170615-002 #5 5ml/min
#    centerline, width, pPmm = 632, 176, 22.4; geometryTJ=[120, 543,  719] #Batch170615-002 #5 Other
#    geometryTJ=[125, 544, 717] #Batch170615-002 #2
#    centerline, width, pPmm = 623, 176, 22.5; geometryTJ=[120, 535, 711] #Batch270715-001 #5

#    centerline, width, pPmm = 628, 176, 22.6; geometryTJ=[119, 540, 716] #Batch100815-001-#8
#    centerline, width, pPmm = 633, 166, 20.2; geometryTJ=[105, 550, 716] #Batch100815-001 #6 & #7
#    centerline, width, pPmm = 634.5, 165, 20.2; geometryTJ=[105, 552, 717] #Batch100815-001 #3 & #4
    
    ignoreLast=None
#    ignoreLast=25
    pos=None
#    centerline, width, pPmm, geometryTJ = None, None, None, None
    centerline, width, pPmm = None, None, None
#    wholeRun(directory, centerline, width, pPmm, Index=None, UseEverySecond=False, geometryTJ=[160, 542, 718])
#    pos=[5,45, 110, 140]
#    pos=[10, 60, 150, 170]
#    removeDuplicateLines(directory, 'T-Junction-Capsule#1_Results.txt')
#    runOnDirectorySym(directory=directory, geoTJ=geometryTJ, plot=True)
#    findSpeedGradient(path, centerline=centerline, widthChannel=width, pPmm=pPmm, FPS=FPS, Index=pos, UseEverySecond=False, borderSize=10, debugInfo=True, closeAfterPlotting=False,  geoCutOff=geometryTJ, ignorlastSym=ignoreLast)
#    plotCentorid(path, borderSize=0, rotate=-0.3, numberToPlot=10)
    rerunWithOldParameters(directory,centerline, width, pPmm, geoTJ=geometryTJ)
#    analyisTwoCapsules(path, centerline=centerline, widthChannel=width, pPmm=pPmm, FPS=FPS, Index=pos, borderSize=10, debugInfo=True, closeAfterPlotting=False,  geoCutOff=geometryTJ)
#    runTwoCapsulesForDirectory(directory, rerun = False, centerline=centerline, width=width, pPmm=pPmm, geoTJ=geometryTJ)
#    plotExtend(path)
#    dirWalk(topdir=directory, copyDest='M:\EdgarHaener\Capsules\Batch120615-004\Symmetry_T-J', string='Ypos_DaugtherChannel', filetype='.jpg')
    
    geoTJ040615d002nr1 = [38, 122, 549, 722]
    path="M:\\EdgarHaener\\Capsules\\Batch040615-002\\T-Junction\\Capsule#1\\Batch040615-002-#1-1S-5kcSt-10FPS-5mlPmin-1\\"
#    findSymmetryByCentreline(path, geoTJ=geoTJ040615d002nr1, plot=True, show=True)
    directory="M:\\EdgarHaener\\Capsules\\Batch040615-002\\T-Junction\\Capsule#1\\"
#    runOnDirectorySym(directory, geoTJ=geoTJ040615d002nr1, geoTJ2=None, fpsSpecial=[])
    
if __name__ == '__main__':
    runFunction()
    
#    for cc in range(1,6):
#        paht=path='M:\\EdgarHaener\\Capsules\\Batch120415-002\\Capsule#1\\Experiments13042015\\Batch120415-002-#1-130415-0p2mlPmin-'+str(cc)+'\\'
#        findSpeedGradient(path, centerline, width, pPmm, FPS, pos, False)
#    wholeRun(directory, centerline, width, pPmm, Index=None, UseEverySecond=False)
    
#    ss1=path.rfind('\\', 1,-1)
#    print(path)
#    print(path[0:ss1])
#    print(path[ss1+1:-1])
#    
#    ss2=path.rfind('\\', 1,ss1)
#    print(path[0:ss2])
#    ss3=path.rfind('\\', 1,ss2)
#    print(path[0:ss3])
#    print(path[ss3+1:ss2])
#    pathData= path[0:ss1-1] + '\\' + path[ss1+1:-1]+'_Results.txt'
#    pathParameters= path[0:ss1-1] + '\\' + path[ss1+1:-1]+'_Parameters.txt'    
    
#    f = open('M:\\EdgarHaener\\Capsules\\RigidParticle-3.5mm\\31032015\\workfile.txt', 'w')
#    f.write('Test')
#    f.close()
#    
#    f = open('M:\\EdgarHaener\\Capsules\\RigidParticle-3.5mm\\31032015\\workfile.txt', 'r')
#    print(f.read())
#    f.close()
#    
     
    
    
