# -*- coding: utf-8 -*-
"""
Created on Sun Jul 05 15:17:56 2015

@author: mbbxkeh2
"""

def find_max_extend(path, d0, pPmm, constantFrequency=False, rotate=0.0, plot=False, threshold=150, printDebugInfo=False, equialize=False):
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
            
#        if equialize:
#            img = cv2.equalizeHist(img) 
#            kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
#            close = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel1)
#            div = np.float32(img)/(close)
#            img = np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX))

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
    find_max_extend
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
    plt.xlabel("Picture # ")find_max_extend
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
    plt.plot(x,centroid_y, 'or',lafind_max_extendbel='Centroid y ', markersize=5)
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