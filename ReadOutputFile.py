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
import track_capsule_TJ_v0p10 as tr
import cv2
import os
import sys
import shutil
import gc

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
def rerunWithOldParameters(directory,centerline, width, pPmm):    
    if platform.system() == 'Linux':
        dSlash='/'
    elif platform.system() == 'Windows': 
        dSlash='\\'
    else:
        print('Unknow Oporating System -  failed')
        
#    print('directory = %s ' %(directory))
    ss1=directory.rfind(dSlash, 1,-1)
#    print('ss1 = %s \t %s' %(ss1, directory[:ss1]))
    ss2=directory.rfind(dSlash, 1,ss1)
#    print('ss2 = %s \t %s' %(ss2, directory[:ss2]))

    pathParameters= directory +directory[ss2+1:ss1]+ '_Parameters.txt'
    pathParametersSave= directory +directory[ss2+1:ss1]+ '_Parameters_ORG.txt'
    pathParametersSave2= directory +directory[ss2+1:ss1]+ '_Parameters_ORG2.txt'
    print('%s' %(pathParameters))
    
    try:
        fileParameters = open(pathParameters, 'r')
    except:
        print("Could not open file. \nFile name = %s \n Function will returns" %pathParameters)
        return
    print('pathParameters = %s' %pathParameters)
    lines = fileParameters.readlines()
    fileParameters.close()       
    print(lines)
    
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
            pathFolder=directory  + entriesLine[0].strip() + dSlash
            
            #find FPS info
            sp1=entriesLine[0].find('FPS')
            sp2=entriesLine[0][:sp1].rfind('_')
            if sp2 == -1:
                sp2=entriesLine[0][:sp1].rfind('-')
#            print('entriesLine[0][sp2+1:sp1] = %s ' %entriesLine[0][sp2+1:sp1])
            FPS=int(entriesLine[0][sp2+1:sp1])
#            print('FPS=%d' %FPS)
                        
            
            #find index information
            if entriesLine[5].strip() == '-1':
                Index=None
            else:
                Index=[int(entriesLine[4]),int(entriesLine[5]),int(entriesLine[6]),int(entriesLine[7])]
            
#            try:
            findSpeedGradient(pathFolder,centerline=centerline, width=width, pPmm=pPmm, FPS=FPS, Index=Index, UseEverySecond=False, borderSize=10, closeAfterPlotting=True)
            plt.close('all')
            gc.collect()
#            except:
#                print('Failed for %s \nwith %s' %(pathFolder, sys.exc_info()[0]))
            
            
def readResultsFile(path):
    fileID=tr.find_batchName(path);
    path_to_file = path+fileID+'_Results.txt'

    numOfLines=file_len(path_to_file)
    
    #This opens a handle to your file, in 'r' read mode
    file_handle = open(path_to_file, 'r')
    
    # Read in all the lines of your file into a list of lines
    lines_list = file_handle.readlines()
    
    centroid_x=np.zeros((numOfLines,1), dtype=float)
    centroid_y=np.zeros((numOfLines,1), dtype=float)
    area=np.zeros((numOfLines,1), dtype=float)
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
        indexC += 1
        v_x[index]=float(entries[12])
        v_y[index]=float(entries[13])
    #    print('v_x = ' + str(v_x[index])+'\t v_y = ' + str(v_y[index]))    
        index=index+1  
        
    return centroid_x, centroid_y, v_x, v_y, area
    
def plotCentorid(path, numberToPlot=3, borderSize=10, rotate=0, show=False):
    
    centroid_x, centroid_y, _, _, _ = readResultsFile(path) 
    
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
    
def findSpeedGradient(path,centerline, width, pPmm, FPS=64, Index=None, UseEverySecond=False, borderSize=10, debugInfo=True, closeAfterPlotting=False, geoCutOff=[161, 540, 720]):
    if debugInfo:
        print(Index)
    centerline += borderSize
    ERROR_CONST=-1
    
    fileID=tr.find_batchName(path);
    centroid_x, centroid_y, v_x, v_y, area = readResultsFile(path)  
    numOfLines=len(centroid_x)           
    
    #Running average
    aveWindow=6
    repeatAveraging=1
        
    
    disp_x=np.zeros((numOfLines-1), dtype=float)
    disp_y=np.zeros((numOfLines-1), dtype=float)  
    vel_x=np.zeros((numOfLines-1), dtype=float)
    vel_y=np.zeros((numOfLines-1), dtype=float)

    
    #find time in Junction from Centroid position
    ylimit=geoCutOff[0]+borderSize
    xlimitLeft=geoCutOff[1]+borderSize
    xlimitRight=geoCutOff[2]+borderSize
    
    count=0
    for ii in range(0,numOfLines):
        if centroid_y[ii] < ylimit and centroid_y[ii] >5 and centroid_x[ii] > xlimitLeft and centroid_x[ii] < xlimitRight:
            count += 1
    timeTJ=count/FPS+0.0
    
    
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
    for i in range(len(vel_x)-1, 0, -1):
        if vel_x[i] == ERROR_CONST or vel_y[i] == ERROR_CONST:
            vel_x=np.delete(vel_x, i)
            vel_y=np.delete(vel_y, i)
            imageCounter=np.delete(imageCounter, i)
    
    speed=np.zeros((len(vel_x),1), dtype=float)
    speed_ave=np.zeros((len(vel_x),1), dtype=float)
    
    speed = np.sqrt( np.power( vel_x ,2) + np.power(vel_y ,2) )
#    speed = np.abs( vel_x ) + np.abs(vel_y) 
    speed_ave = tr.runningMean(speed, aveWindow)
    
#    print('len(speed) = %d \t len(speed_ave) = %d' %(len(speed), len(speed_ave)))
    
    for i in range(repeatAveraging):
        speed_ave=tr.runningMean(speed_ave, aveWindow)
    
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

    #find start and finish of slow-down
    #itemindex = numpy.where(array==item)
    #array[itemindex[0][0]][itemindex[1][0]]
    
    startThres=0.2
    endThres=0.2
    startIndex=np.where(ave_dxs < np.min(ave_dxs) * startThres)
    endIndex=np.where(ave_dxs > np.max(ave_dxs) * endThres)

    
    timeInTJunction=(zx2[endIndex[0][-1]]-zx2[startIndex[0][0]])*(1/FPS)
    print("Time in T-Junction = " +str(timeInTJunction)+" s ")
    
    fig = plt.figure(figsize=(8, 6), dpi=200,)
    ax = fig.add_subplot(111)
    plt.plot(zx, dx, 'oc',label='Gradient Speed', markersize=5)
    plt.plot(zx, ave_dx, 'sr',label='Average Gradient Speed', markersize=5)
    plt.plot(zx2, ave_dxs, '^y',label='Average Gradient Speed Short', markersize=5)
    
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
    
    
    
    images=np.arange(len(centroid_x))
#    fig=plt.figure()
#    plt.plot(images, centroid_x, 'sb',label='Centroid X', markersize=5)
#    plt.plot(images, centroid_y, 'or',label='Centroid Y', markersize=5)
#    plt.title("Centroid "+" " + fileID)
#    plt.xlabel("Picture # [FPS = %d]" %FPS)
#    plt.ylabel("Centroid [pixels]")
#    plt.legend(fontsize=6)
#    plt.savefig(path+fileID+"_Centroid_Graph.jpg")      
#    if closeAfterPlotting:
#         plt.clf(); plt.close(fig);    
#    
#    avedisp_x =  tr.runningMean(disp_x, aveWindow  )
#    avedisp_y =  tr.runningMean(disp_y, aveWindow )  
#    
#    imagesdispx2=np.arange(len(disp_x))    
#    fig=plt.figure()
#    plt.plot(imagesdispx2, disp_x, 'sb',label='Displacement X', markersize=5)
#    plt.plot(imagesdispx2, disp_y, 'or',label='Displacement Y', markersize=5)
##    print('len(imagesdispx) = %d len(avedisp_x) = %d' %(len(imagesdispx), len(avedisp_x)))
#    plt.plot(imagesdispx2, avedisp_x, 'hy',label='Displacement X Averaged', markersize=5)
#    plt.plot(imagesdispx2, avedisp_y, 'Dg',label='Displacement Y Averaged', markersize=5)
#    plt.title("Displacement "+" " + fileID)
#    plt.xlabel("Picture # [FPS = %d]" %FPS)
#    plt.ylabel("Displacement[pixels]")
#    plt.legend(fontsize=6)
#    plt.savefig(path+fileID+"_Displacement_Graph.jpg")
#    if closeAfterPlotting:
#         plt.clf(); plt.close(fig);
    
    
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

#    fig = plt.figure(figsize=(8, 6), dpi=200,)
#    ax2 = fig.add_subplot(111)
#    plt.plot(imageCounter, speed_ave, 'sb',label='Speed Averaged', markersize=5)
#    plt.plot(imageCounter, speed, 'or',label='Speed', markersize=5)
#    
#    plt.plot([ 0, len(speed_ave)], [firstSpeed,firstSpeed], '--k', linewidth=1)
#    plt.plot( [ 0, len(speed_ave)], [secondSpeed,secondSpeed], '-.k', linewidth=1)
#    
#    s = "min Speed= %.2e pixels/s" %minSpeed
#    s1= "ave main channel = %.2e pixels/s" % (firstSpeed)
#    s2= "ave main daugther = %.2e pixels/s" % (secondSpeed)
#    
#    ax2.text(len(x1)/1.8, maxSpeed/2, s, fontsize=15)
#    ax2.text(len(x1)/1.8, maxSpeed/3, s1, fontsize=12)
#    ax2.text(len(x1)/1.8, maxSpeed/4, s2, fontsize=12)
#    
#    
#    plt.title("Speed"+" " + fileID)
#    plt.xlabel("Picture # ")
#    plt.ylabel("Speed[pixels/s]")
#    plt.legend(loc=1, fontsize=6)
#    plt.ylim([0,np.max(speed_ave)*1.2])
#    plt.show()
#    plt.savefig(path+fileID+"_Speed_Graph.jpg")
#    if closeAfterPlotting:
#         plt.clf(); plt.close(fig);
    
    xv_x=np.arange(len(v_x))
#    if not closeAfterPlotting:
#        plt.figure()
#        plt.plot(xv_x, v_x, 'sb',label='v_x', markersize=5)
#        plt.plot(xv_x, v_y, 'or',label='v_y', markersize=5)
#        plt.title("Velocity"+" " + fileID)
#        plt.xlabel("Picture # [FPS = 64]")
#        plt.ylabel("Velocity [pixels/s]")
#        plt.legend(fontsize=6)
#        #plt.savefig(path+fileID+"_Velocity_Graph.jpg")
    
    #Check centering of capusle - assume first half is in main channel
    cutOff=0.1 #cut of 10% either side
    leng=len(centroid_x)
    
    if Index == None:
        x_mainC= centroid_x[cutOff*leng:(0.5-cutOff)*leng]
        y_mainC= centroid_y[cutOff*leng:(0.5-cutOff)*leng]
    else:
        x_mainC= centroid_x[Index[0]:Index[1]]
        y_mainC= centroid_y[Index[0]:Index[1]]
    
    
    
#    print('Before, minimum of x = ' + str(np.min(x_mainC)))
    #eliminate zero zero positions
    for i in range(len(x_mainC)-1,-1,-1):
        if     x_mainC[i] == -1.0  or y_mainC[i] == -1.0 or x_mainC[i] == -1  or y_mainC[i] == -1:
            lenBefore=len(x_mainC)
            x_mainC=np.delete(x_mainC, i)
            y_mainC=np.delete(y_mainC, i)
            lenAfter=len(x_mainC)
#            print('Deleting exicuted for index %d (beofre =%d and after = %d)' %(i, lenBefore,lenAfter ) )
#    print('After, minimum of x = ' + str(np.min(x_mainC)))



    for kk in range(len(x_mainC)-1, -1, -1):
        if x_mainC[kk] <1:
            x_mainC =np.delete(x_mainC , kk)
            y_mainC =np.delete(y_mainC , kk)
            

    aveX=np.average(x_mainC)  
    differenceX=aveX-centerline
    
    #check whether it goes left or right
    centroid_x[centroid_x != -1]
    aveXdaugtherChannel=np.average(centroid_x[(0.5+cutOff)*leng: (1-cutOff)*leng])
               #[a != 0]
    
    if aveXdaugtherChannel > centerline:
        turn='right'
    else:
        turn='left'
        
        
    
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
    
    name=path[:-4]
    d1=name.find('mlPmin')
    d2=name[:d1].rfind('_')
    if d2 ==-1:
        d2 = name[:d1].rfind('-')
    d3=name[d2:d1].find('m')
    if d3==-1:
        volFlux=name[d2+1:d1]
    else:
#        print('d3= %d' %d3)
#        print(name[d2+1:d2+d3])
        volFlux=name[d2+1:d2+d3]
#    print('Name: %s \nVolumn Flux = %s' %(name, volFlux))
    volFlux=float(volFlux)
    
    print('Vol Flux \tname \t min speed \t ave speed 1 \t ave speed 2 \t time \t short \t threshold 1 \t threshold 2 \t Off-centre \t turned' )
    print('%.0f \t %s \t %.2e \t %.2e \t %.2e \t %.2e \t %.2f \t %.2f \t %.2f \t %.2f \t %s \t %.3e' %(volFlux, fileID, minSpeed, firstSpeed,  secondSpeed, timeInTJunction, short, startThres, endThres, differenceX, turn, timeTJ ))           
    
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
    pathData= path[0:ss1] + dSlash + path[ss3+1:ss2]+'-'+path[ss2+1:ss1]+'_Results.txt'
    pathParameters= path[0:ss1] + dSlash + path[ss3+1:ss2]+'_Parameters.txt'
    
#    print(pathData)
#    print('M:\\EdgarHaener\\Capsules\\RigidParticle-3.5mm\\31032015\\Rigid3p5mm-310315-30fps-10mlPmin-1\\workfile.txt')   
    
    #File 1: Data
    import os.path
    if not os.path.isfile(pathData): #check whether the file for this run has been started
        fileData = open(pathData, 'w')
        fileData.write('Vol Flux \t\t\t\t\t\tname \t min speed \t ave speed 1 \t ave speed 2 \t time acceleration  \ \t Off-centre \t turned \t time geometric \n')
        fileData.close()
    if not os.path.isfile(pathParameters):
        fileParameters = open(pathParameters, 'w')
        fileParameters.write('fileID \t\t\t\t\t\tshort \t threshold 1 \t threshold 2 \t Pos \n')
        fileParameters.close()
    
    #check whether there is alread a value for this fileID
    if fileID in open(pathData).read():
         #File 1: Data
        f = open(pathData,"r")
        lines = f.readlines()
        f.close()
        
        fileData = open(pathData, 'w')
        for line in lines:
            if fileID in line:
                fileData.write('%.0f \t %s \t \t \t %.2e \t %.2e \t %.2e  \t %.2f \t %.2f \t %s \t %.3e \n' %(volFlux, fileID, minSpeed, firstSpeed,  secondSpeed, timeInTJunction, differenceX, turn, timeTJ ))
            else:
                fileData.write(line)        
                
    else: #if this hasn't been written to file before, simple append it to the end
         #File 1: Data
        fileData = open(pathData, 'a')
        fileData.write('%.0f \t %s \t  %.2e \t %.2e \t %.2e  \t %.2f \t %.2f \t %s \t %.3e \n' %(volFlux, fileID, minSpeed, firstSpeed,  secondSpeed, timeInTJunction, differenceX, turn, timeTJ ))
        fileData.close()
    
    if fileID in open(pathParameters).read():
        #File 2: Parameters
        f2 = open(pathParameters,"r")
        lines = f2.readlines()
        f2.close()       

        fileParameters = open(pathParameters, 'w')
        for line in lines:
            if fileID in line:
                if Index ==None:
                    fileParameters.write('%s \t  %.2e  \t %.2f \t %.2f \t %d \t %d \t %d \t %d \n' %(fileID, short, startThres, endThres, -1, -1, -1, -1))
                else:
                    fileParameters.write('%s \t  %.2e  \t %.2f \t %.2f \t %d \t %d \t %d \t %d \n' %(fileID, short, startThres, endThres, Index[0], Index[1], Index[2], Index[3]))
            else:
                fileParameters.write(line) 
    else:
        #File 2: Parameters
        fileParameters = open(pathParameters, 'a')
        if Index ==None:
            fileParameters.write('%s \t  %.2e  \t %.2f \t %.2f \t %d \t %d \t %d \t %d \n' %(fileID, short, startThres, endThres, -1, -1, -1, -1))
        else:
            fileParameters.write('%s \t %.2e  \t %.2f \t %.2f \t %d \t %d \t %d \t %d \n' %(fileID, short, startThres, endThres, Index[0], Index[1], Index[2], Index[3]))
        fileParameters.close()
    
    
            
            

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

def runFunction():
    plt.close("all")

    
    directory='M:\\EdgarHaener\\Capsules\\Batch040615-002\\T-Junction\\Capsule#1\\'
    path =directory + 'Batch040615-002-#1-1S-5kcSt-140FPS-70mlPmin-12\\'
    FPS=140
    centerline=635.5 #629
    width=173
    pPmm=22.2
#    print('\npPmm = %f' %pPmm)
    pos=None
    
#    wholeRun(directory, centerline, width, pPmm, Index=None, UseEverySecond=False, geometryTJ=[160, 542, 718])
#
#    pos=[20, 60, 146, 152]
#    pos=[15, 90, 150, 180]
    findSpeedGradient(path, centerline=centerline, width=width, pPmm=pPmm, FPS=FPS, Index=pos, UseEverySecond=False, borderSize=10, debugInfo=True, closeAfterPlotting=False, geoCutOff=[122, 549, 722])
#    plotCentorid(path, borderSize=0, rotate=-0.3, numberToPlot=10)
#    rerunWithOldParameters(directory,centerline, width, pPmm)
    
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
     
    
    
