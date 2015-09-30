# -*- coding: utf-8 -*-
"""
Program to creat a list of photos in a folder, threshold them and measure 
various quanitities such as the area, perimeter and extension in the y ans x 
direction. 

To start, look at the bottom of the file in the 'if __name__ == '__main__':'
Statment

Created on Wed Sep 18 12:44:18 2013

@author: Edgar Haener
edgar.haener@gmail.com

"""
from __future__ import absolute_import, division, print_function
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
#memory related imports
import gc

import shutil

 

def wholeRun(directory, rotateImages=0.0):
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
            find_max_extend(directory+f+'\\', constantFrequency=True, rotate=rotateImages)
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
    fileType='.jpg'
    dash='-'

    dirs = os.listdir(path)
    j=0
    for fname in dirs:
        if (fname[-4:len(fname)] == fileType):
            j+=1
    numberOfJPG=j
#    filenameList = [ filenameClass() for i in range(numberOfJPG)]
    filenameList=[]
    
    i=-1
    for fname in dirs:
        if (fname[-4:len(fname)] == fileType):
            i+=1            
            name=fname[:-4]
            #find first dash (day)
#            d1=name.find(dash,-6,-1)
            d1=name.find('_',-5,-1)
#            print('number = ' + name[d1+1:])

            
            temp=filenameClass()
            temp.fn = fname
            temp.number=abs(int(float(name[d1+1:])))
            temp.fps=60
               
            filenameList.append(temp)
    
    #sort by milliseconds
    newlist = sorted(filenameList, key=lambda filenameClass: filenameClass.number) 
    
    
#    for obj in newlist:
#        obj.printOut()
#        
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
    dSlash='\\'
    d1=path.rfind(dSlash,1,-3)
    reslt=path[d1+1:-1]
    
    d2=reslt.find('\\', 0, -1)
    if d2!=-1 :
        reslt="notfound"
        
    print(reslt)
    
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

def find_max_extend(path, constantFrequency=False, rotate=0.0):
    """Goes though all the pictures in directory, thresholds them and finds 
    several measurments for the resulting object, which should be a capsule if 
    the threshold has been chossen correctly
    """
    fileID=find_batchName(path);
    ERROR_CONST=-1
    #d0 is the diameter of the capsule at zero flow rate
    
    #d0=5.2 #r0 for Batch 141113-002 #1
    #d0=4.16  #r0 for Batch 141113-003 #4
    #r0=2.2 #r0 for Batch 100114-002 #1
    #r0=2.0 #r0 for Batch 100114-001 #1
    #d0=4.3  #diameter  for Batch 100114-003 #1
    #d0=4.4 #diameter for Batch 270114-001 #1
    #d0=5.1 #diameter for Batch 300114-002 #1
    #d0=5.7 #diameter for Batch 310114-001 #3
    #d0=4.1 #diameter for Batch 060214-001 #1
    #d0=4.45 #diameter for Batch 270214-001 #1
    #d0=4.29 #diameter for Batch 270214-001 #2
    #-------------------------------------------
    d0=3.48 #diameter for rigid particle
#    d0=4.11
    
    #initial 2D projected area
    A0=np.pi*np.power(d0/2,2)
    #initial perimeter
    p0=2.0*np.pi*(d0/2)
    
    #pixels per milimeter in the image
    pPmm=30.1

    #close all graphs
    plt.close("all")
        
    # 'plot' is a boolean variable that controls whether the outline is plotted 
    # and saved to file in foder 'Check'. This is used to check that the 
    # code works correctly.
    plot=True
    plot=False
    
    #'forShow is a boolean variable that governs whether plot is displayed 
    #during program run. 
    forShow=False
#    forShow=True
    
    
    #This sets the threshold what is counted as black in grayscale image and 
    #should be between 0-255
    #A threshold of 110 worked robustly over a wide range
    threshold=60
    
    #get sorted list of filenames
    if constantFrequency:
        fileList, leng =sortPhotosPCO(path)
        print('Using sortPhotosPCO')
    else:
        fileList, leng =sortPhotos2(path)
        print('Using sortPhotos2')
    
    
    
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
            F=plt.figure(num='Initial', facecolor='w', edgecolor='k', figsize=(24, 8), dpi=600)
            a1=plt.subplot(131)
            plt.imshow(img, cmap='Greys')
        
        #Crop image to area of intrest - adjust as nessecary        
#        img = img[90:900, 600:1100]
        
#        if(plot):
#            a1=plt.subplot(142)
#            plt.imshow(img, cmap='Greys')
            
    #    img = cv2.equalizeHist(img)    
    #    img=cv2.multiply(img, np.array([1.25]))
            
        #add a border of black pixels around image in case capsule touches edge    
        img=cv2.copyMakeBorder(img,borderSize,borderSize,borderSize,borderSize,
                               cv2.BORDER_CONSTANT,value=(255, 255, 255))    
        
        #Get size of image
        y,x = img.shape
        
        #Add a rectanlge over areas of image not of intrest, to prevent 
        #interference from these areas
        
#        #Genie Cam
#        cv2.rectangle(img, (0, 0), (585+borderSize, 725+borderSize), 255,
#                      thickness=-1)   
#        cv2.rectangle(img, (765+borderSize, 0), (x, 725+borderSize),  255,
#                      thickness=-1)
#        cv2.rectangle(img, (0, 840+borderSize), (x, y), 255,
#                      thickness=-1)
        
        
        #PCO SETUp
        cv2.rectangle(img, (0, 140+borderSize), (514+borderSize, y), 255,
                      thickness=-1)   
        cv2.rectangle(img, (755+borderSize, 140+borderSize), (x, y),  255,
                      thickness=-1)
        #Block out timestamp from pco camera
        cv2.rectangle(img, (0+borderSize, 0+borderSize), (x+borderSize, 9+borderSize), 255,
                      thickness=-1)
                     
        #convert the image to B&W with the given threshold. 'thresh' is the 
        # the B&W image
        ret, thresh = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY) #192    
       
        
        #make a copy, to ensure we are not changing the image
        temp=thresh.copy()
        
        if(plot):
            a1=plt.subplot(132)
            plt.imshow(thresh, cmap='Greys')
            
            
        
#        del thresh    
        
        #find the contours in the image
        # Details under: http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#findcontours
        #Good tutorial: http://opencvpython.blogspot.co.uk/2012/06/hi-this-article-is-tutorial-which-try.html
        contours, hierarchy = cv2.findContours(temp,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        #Select longest contour as this should be the capsule
        lengthC=0
        ID=-1
        idCounter=-1
        for x in contours:
            idCounter=idCounter+1
            if len(x) > lengthC:
                lengthC=len(x)
                ID=idCounter
        im=img.copy()
        
        #if longest contour was found, then ID is the index of it
        if ID != -1:
            cnt = contours[ID]
            
            #find bounding rectangle of countour
            x,y,w,h = cv2.boundingRect(cnt)
            
            #draw bounding box and countour
            cv2.rectangle(im,(x,y),(x+w,y+h),(255,255,255),2)    
            cv2.drawContours(im, contours,ID,(255,255,255),2)
    
            
            #fit ellipse
            if len(cnt) <= 5:
                print('length1 less than 5 for i = %d' %(i));
                if i==37:
#                    cv2.imshow('With Contours '+str(i)s,im)
                    plt.imshow(im)
                    
                                #find are of contour and perimeter
                area[counterL] = ERROR_CONST
                perimeter[counterL] = ERROR_CONST
                
                #getting pixel position at min/max x and y extend
                leftmost = ERROR_CONST
                rightmost = ERROR_CONST
                topmost = ERROR_CONST
                bottommost = ERROR_CONST
                
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
                area[counterL] = cv2.contourArea(cnt)
                perimeter[counterL] = cv2.arcLength(cnt,True)
                
                #getting pixel position at min/max x and y extend
                leftmost = x
                rightmost = x+w
                topmost = y+h
                bottommost = y
                print('(x,y) = (%d, %d) - width = %d height = %d' %(x, y, w, h))
                
                width[counterL]=w
                heigth[counterL]=h
                verticalDistance[counterL] = (h+0.0)/(pPmm+0.0)
                horizontalDistance[counterL] = (w+0.0)/(pPmm+0.0)      
                
                #fit ellipse
                ellipse = cv2.fitEllipse(cnt)
                (x,y),(ma, MA),angle[counterL] = cv2.fitEllipse(cnt)
                cv2.ellipse(im,ellipse,(0,255,255),2)
            
                #Taylor parameter
                D[counterL]=(MA-ma)/(MA+ma)

                #find centroid
                M = cv2.moments(cnt)
                centroid_x[counterL] = int(M['m10']/M['m00'])
                centroid_y[counterL] = int(M['m01']/M['m00'])
            
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
                filesavepath=savepath+'Junction_'+str(i)+'.png'
                plt.savefig(filesavepath, dpi=900)

                fig = plt.figure(dpi=300,)
                ax3 = fig.add_subplot(111)
                plt.imshow(thresh, cmap='Greys')
                filesavepath=savepath+'Junction_Big_'+str(i)+'.png'
                plt.savefig(filesavepath, dpi=900)
                
                
                if(forShow==False):
                    plt.clf()
                    plt.close("all")
                    
        else:
            #savepath=path+'Check\\'
            if(plot):
                savepath=path+'Check\\'
                if not os.path.exists(savepath): os.makedirs(savepath)
                filesavepath=savepath+'Junction_'+str(i)+'.png'
                plt.savefig(filesavepath, dpi=900)
                if(forShow==False):
                    plt.clf()
                    plt.close("all")
            print("No contour!")
        
        del img, temp
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
    plt.savefig(path+fileID+"_GradientSpeed_Graph.png")
    
    
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
    plt.savefig(path+fileID+"_Extend_Graph.png")
    
    area=area/(np.power(pPmm,2))
    area=area/A0
    
    plt.figure(3)
    plt.plot(x, area, 'or',label='Area', markersize=5)
    plt.title("Area"+" " + fileID)
    plt.xlabel("Picture # ")
    plt.ylabel("Area / Initial Area")
    plt.savefig(path+fileID+"_Area_Graph.png")
    
    perimeter=perimeter/pPmm
    perimeter=perimeter/p0
    
    plt.figure(4)
    plt.plot(x, perimeter, 'sb',label='Perimeter', markersize=5)
    plt.title("Perimeter"+" " + fileID)
    plt.xlabel("Picture # ")
    plt.ylabel("Perimeter/ Initial Perimeter")
    plt.savefig(path+fileID+"_Perimeter_Graph.png")
    
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
    plt.savefig(path+fileID+"_CentroidPosition_Graph.png")        

    
    x1=np.arange(leng-1)
        
    plt.figure(6)
    plt.plot(x1, vel_x, 'sb',label='v_x', markersize=5)
    plt.plot(x1, vel_y, 'or',label='v_y', markersize=5)
    plt.title("Velocity"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Velocity [mm/s]")
    plt.legend()
    plt.savefig(path+fileID+"_Velocity_Graph.png")
    
    plt.figure(7)
    plt.plot(x1, disp_x, 'sb',label='disp_x', markersize=5)
    plt.plot(x1, disp_y, 'or',label='disp_y', markersize=5)
    plt.title("Displacment"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Displacment [pixels]")
    plt.legend()
    plt.savefig(path+fileID+"_Displacment_Graph.png")
    
    plt.figure(8)
    plt.plot(x, time, 'sb',label='Time (s)', markersize=5)
    plt.title("Time [s]"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Time [s] ")
    plt.legend()
    plt.savefig(path+fileID+"_Time_Graph.png")
    
    plt.figure(9)
    plt.plot(x1, speed_ave, 'sb',label='Speed Averaged', markersize=5)
    plt.title("SpeedAveraged"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Speed[mm/s]")
    plt.legend()
    plt.savefig(path+fileID+"_SpeedAve_Graph.png")
    
    plt.figure(10)
    plt.plot(x1, runningMean(disp_x, 6), 'sb',label='running mean disp_x', markersize=5)
    plt.plot(x1, runningMean(disp_y, 6), 'or',label='running mean disp_y', markersize=5)
    plt.title("Displacment Runnung Average"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Displacment [pixels]")
    plt.legend()
    plt.savefig(path+fileID+"_DisplacmentRunnungAverage_Graph.png")
    
    plt.figure(9)
    plt.plot(x1, speed, 'or',label='Speed', markersize=5)
    plt.title("Speed"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Speed[mm/s]")
    plt.legend()
    plt.savefig(path+fileID+"_Speed_Graph.png")
    
    plt.figure(11)
    plt.plot(x,centroid_x, 'sb',label='Centroid x ', markersize=5)
    plt.plot(x,centroid_y, 'or',label='Centroid y ', markersize=5)
    plt.title("Centroid Position"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Centroid Position [pixels]")
    plt.legend()
    plt.savefig(path+fileID+"_CentroidPosition2_Graph.png") 
    
    plt.figure(12)
    plt.plot(x,width, 'sb',label='Width ', markersize=5)
    plt.plot(x,heigth, 'or',label='Heigth', markersize=5)
    plt.title("Size of Particle"+" " + fileID)
    plt.xlabel("Picture # [FPS = 64]")
    plt.ylabel("Width / Hiegth [pixels]")
#    plt.ylim((70,82))
    plt.legend(loc=2)
    plt.savefig(path+fileID+"_width-heigth_Graph.png") 
    
    #measuring offset
    centerline=632.5
    
        
    return r
    


        

    
    
