# -*- coding: utf-8 -*-
"""
Created on Fri Mar 07 15:23:59 2014

@author: Edgar
"""
from __future__ import absolute_import, division, print_function
import matplotlib.pyplot as plt
import numpy as np

import track_capsule_TJ_v0p8 as tr

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
    
def findSpeedGradient(path):
    #plt.close("all")
    #path='M:\\EdgarHaener\\Capsules\\Batch060315-001\\Capsule#1-Experiments080315\\Batch060315-001-20mlPmin-3\\'
    fileID=tr.find_batchName(path);
    path_to_file = path+fileID+'_Results.txt'
#    path_to_file = path+'Results.txt'
    
    print('path_to_file :  ' +path_to_file )
#    
#    FPS=60
    
    numOfLines=file_len(path_to_file)
    
    #This opens a handle to your file, in 'r' read mode
    file_handle = open(path_to_file, 'r')
    
    # Read in all the lines of your file into a list of lines
    lines_list = file_handle.readlines()
    
    centroid_x=np.zeros((numOfLines,1), dtype=float)
    centroid_y=np.zeros((numOfLines,1), dtype=float)
    size_x=np.zeros((numOfLines,1), dtype=float) #(7, 8)
    size_y=np.zeros((numOfLines,1), dtype=float)
    
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
                centroid_x[indexC]=float(entries[5])
                centroid_y[indexC]=float(entries[6])
                indexC += 1
            continue
        
        centroid_x[indexC]=float(entries[5])
        centroid_y[indexC]=float(entries[6])
        indexC += 1
        size_x[index]=float(entries[7])
        size_y[index]=float(entries[8])
    #    print('v_x = ' + str(v_x[index])+'\t v_y = ' + str(v_y[index]))    
        index=index+1        
    
#    #eliminate zero zero positions
#    for i in range(len(centroid_x)):
#        if     centroid_x[i] == 0  or centroid_y[i] == 0:
#            centroid_x=np.delete(centroid_x, i)
#            centroid_y=np.delete(centroid_y, i)
            
    
    #Running average
    aveWindow=4
        
    
    disp_x=np.zeros((numOfLines-1,1), dtype=float)
    disp_y=np.zeros((numOfLines-1,1), dtype=float)  

    
    for i in range(1,numOfLines-1):
        if centroid_x[i] == -1  or centroid_y[i] == -1 or centroid_x[i-1] == -1  or centroid_y[i-1] == -1:
            disp_x[i]= 0
            disp_y[i]= 0
        else:
            disp_x[i]= centroid_x[i] - centroid_x[i-1] 
            disp_y[i]= centroid_y[i] - centroid_y[i-1] 
        
        dispCutOff=50.0
        if abs(disp_x[i]) > dispCutOff:
            print('disp_x[i] > %f: disp_x[%d]=%e' %(dispCutOff, i,disp_x[i]))
            disp_x[i]=0
        
        if abs(disp_y[i]) > dispCutOff:
            print('disp_y[i] > %f: disp_y[%d]=%e' %(dispCutOff, i,disp_y[i]))
            disp_y[i]=0
                    
    
    
    
    displacment = np.sqrt( np.power( disp_x ,2) + np.power(disp_y ,2) )
    displacment_ave = np.sqrt( np.power( tr.runningMean(disp_x, aveWindow) ,2) + np.power(tr.runningMean(disp_y, aveWindow) ,2) )
    displacment_ave =  tr.runningMean(displacment_ave, aveWindow)  
    displacment_ave =  tr.runningMean(displacment_ave, aveWindow) 
    displacment_ave =  tr.runningMean(displacment_ave, aveWindow) 
    displacment_ave =  tr.runningMean(displacment_ave, aveWindow) 
    displacment_ave =  tr.runningMean(displacment_ave, aveWindow) 

    xaxis=np.arange(len(displacment))
    #displacment
    fig = plt.figure(figsize=(8, 6), dpi=200,)
    ax = fig.add_subplot(111)
    plt.plot(xaxis, displacment, 'oc',label='Displacement', markersize=5)
    plt.plot(xaxis, displacment_ave, 'sr',label='Average Displacemenet', markersize=5)

#    s = "Time in T-Junction = %.2e s" %timeInTJunction
#    s1= "Threshold for decrease = %.2f" % (startThres)
#    s2= "Threshold for increase = %.2f" % (endThres)
#    
#    ax.text(l_dx/2.2, min_dx[0]/2, s, fontsize=15)
#    ax.text(l_dx/2.2, min_dx[0]/1.4, s1, fontsize=12)
#    ax.text(l_dx/2.2, min_dx[0]/1.05, s2, fontsize=12)
    
#    plt.ylim([-50,50])
    
    plt.title("Displacement" +" " + fileID)
    plt.xlabel("Image")
    plt.ylabel("Pixels")
    plt.legend(loc=2, fontsize=6)
    plt.savefig(path+fileID+"_Displacment_Graph.jpg")
    
    
    indexStatic = []    
    for i in range(len(displacment)):
        if displacment_ave[i] < 0.4 and i < 0.95*len(displacment):
            indexStatic.append(i)
            
    size_x_static=[size_x[x] for x in indexStatic]
    size_y_static=[size_y[x] for x in indexStatic]
    xpos_static = [centroid_x[x] for x in indexStatic]
    ypos_static = [centroid_y[x] for x in indexStatic]
    xaxis_static=[xaxis[x] for x in indexStatic]
    
    #Plot Satic Size
    
    fig = plt.figure(figsize=(8, 6), dpi=200,)
    ax = fig.add_subplot(111)
    plt.plot(xaxis_static, size_x_static, 'oc',label='Size X', markersize=5)
    plt.plot(xaxis_static, size_y_static, 'sr',label='Size Y', markersize=5)
    
    plt.title("Static Size" +" " + fileID)
    plt.xlabel("Image")
    plt.ylabel("Pixels")
    plt.legend(loc=2, fontsize=6)
    plt.savefig(path+fileID+"_StaticSize_Graph.jpg")
    
    #Size versus Position
    fig = plt.figure(figsize=(8, 6), dpi=200,)
    ax = fig.add_subplot(111)
    plt.plot(xpos_static, size_x_static, 'oc',label='Size X', markersize=5)
    plt.plot(xpos_static, size_y_static, 'sr',label='Size Y', markersize=5)
    
    plt.title("Static Size" +" " + fileID)
    plt.xlabel("X-Position [pixels]")
    plt.ylabel("Pixels")
    plt.legend(loc=2, fontsize=6)
    plt.savefig(path+fileID+"_StaticSizevsXpos_Graph.jpg")
    
    fig = plt.figure(figsize=(8, 6), dpi=200,)
    ax = fig.add_subplot(111)
    plt.plot(ypos_static, size_x_static, 'oc',label='Size X', markersize=5)
    plt.plot(ypos_static, size_y_static, 'sr',label='Size Y', markersize=5)
    
    plt.title("Static Size" +" " + fileID)
    plt.xlabel("Y-Position [pixels]")
    plt.ylabel("Pixels")
    plt.legend(loc=2, fontsize=6)
    plt.savefig(path+fileID+"_StaticSizevsYpos_Graph.jpg")
            


if __name__ == '__main__':
    plt.close("all")
    path='M:\\EdgarHaener\\Capsules\\RigidParticle-3.5mm\\07042015\\Rigid3p5mm-07042015-StaticTest-1\\'
    
    findSpeedGradient(path)