from __future__ import absolute_import, division, print_function
import numpy as np
import track_capsule_TJ as tr
import os

#import sys
#sys.path.append('C:\\Users\\Edgar\\Dropbox\\PhD\\Python') #Machine Schuster G.21


#To run script on a file, change path and run     
#FPS=50
#directory = 'M:\\EdgarHaener\\Capsules\\Batch120615-004\\T-Junction\\'
#folder =  'Batch120615-001-#4-%dFPS-25mlPmin-1\\' %FPS
#path = directory + folder #Test2\\'

#FPS=30
#directory = 'M:\\EdgarHaener\\Capsules\\Batch120615-004\\T-Junction\\'
#folder =  'Batch040615-002-#1-1S-5kcSt-%dFPS-5mlPmin-1\\' %FPS
#path = directory + folder #Test2\\'



FPS=10
directory = 'M:\\EdgarHaener\\Capsules\\Batch170615-002\\T-Junction\\2015-06-20\\Batch170615-002_#5\\'
folder =  'Batch170615-002_#5_10FPS_5mlPmin-1\\' 
path = directory + folder #Test2\\'

#directory = '/home/magda/Edgar/Caspules/Batch260615--001/T-Junction/#17/'
#folder = 'Batch260615-001-#17-100FPS-50mlPmin-1/Test/'
#path = directory + folder #Test2\\'
#d = path[:-1].rfind(os.path.sep)
#backPath = directory +'Background100FPS.png'
#a = tr.userInputClass(directory, folder, 3.8, 22.3, -0.3, 10, 25, 114, 559, 733, backPath)



#directory = 'C:\\Users\\Edgar\\Desktop\\Experiments\\2015-07-22\\GelBead150715-1-#4\\'
#folder = 'GelBead150715-1-#4-10FPS-5mlPmin-1\\' #test\\'
##folder = 'GelBead150715-1-#4-10FPS-Static-1\\'  
#path=directory + folder

#print(os.path.exists('M:\\EdgarHaener\\Capsules\\Batch120615-004\\T-Junction\\Background30FPS.png'))

backPath = directory +'Background%dFPS.png' %FPS
#backPath = path[:d]+'\\BackgroundStatic.png'

#a = tr.userInputClass(directory, folder, 3.9, 22.3, -0.3, FPS, 37, 121, 535, 709, backPath) #GelBeads150715-1 #4
#a = tr.userInputClass(directory, folder, 2.7, 22.4, -0.3, FPS, 32, 119, 537, 712, backPath) #GelBeads150730-1 #2
#a = tr.userInputClass(directory, folder, 3.8, 22.4, -0.3, FPS, 35, 118, 549,  724, backPath) #Batch120615-004-#5 All excepte 15ml/min
#a = tr.userInputClass(directory, folder, 3.8, 22.2, -0.3, 30, 72, 160, 550, 725, backPath) #Batch120615-004-#5 15ml/min
#a = tr.userInputClass(directory, folder, 3.9, 22.2, -0.3, FPS, 38, 122, 549, 722, backPath) #Batch040615-002-#1
#a = tr.userInputClass(directory, folder, 4.5, 22.5, -0.3, FPS, 35, 120, 535, 711, backPath) #Batch270715-001-#5
#a = tr.userInputClass(directory, folder, 3.7, 22.6, -0.3, FPS, 33, 119, 540, 716, backPath) #Batch100815-001-#8
#a = tr.userInputClass(directory, folder, 3.7, 20.2, -0.3, FPS, 23, 105, 550, 716, backPath) #Batch100815-001-#6-7
#a = tr.userInputClass(directory, folder, 3.8, 22.3, -0.3, FPS, 28, 114, 559, 733, backPath) #Batch260615-001-#17
#a = tr.userInputClass(directory, folder, 3.2, 22.4, -0.3, FPS, 34, 120, 544, 719, backPath) #Batch170615-002-#5 all but 5ml/min
a = tr.userInputClass(directory, folder, 3.2, 22.4, -0.3, 10, 73, 160, 544, 719, backPath) #Batch170615-002-#5 5ml/min
 
#tr.find_max_extend(path, d0=3.7, pPmm=22.3, background=backPath, rotate=-0.3, plot=False, threshold=130, printDebugInfo=False, denoising = False, geomTJ=[25, 121, 535, 709])
#tr.runOneFPS(directory, d0=3.7,  pPmm=22.3, FPS=70, rotateImages=-0.3, threshold=130, background=backPath)
#tr.runScript(parameterClass=a, plot=False, debugInfo=False, twoCapsules=False, OpenCV3=False)
tr.runOneFPS(parameters=a, FPS=10, twoCapsules=False, OpenCV3=False)


#fpss=[40, 60, 70, 100, 120, 140]
#problems1=[]
#for fps in fpss:
#    try:
#        backPath = directory +'Background'+str(fps)+'FPS.png'
#        a = tr.userInputClass(directory, folder, 3.8, 22.3, -0.3, fps, 25, 114, 559, 733, backPath)
#        tr.runOneFPS(parameters=a, FPS=fps)
#    except:
#        problems1.append("%d didn't complete" %fps)
#
#print(problems1)


#import cv2
#from matplotlib import pyplot as plt
#plt.close('all')
#
#img = cv2.imread(path+'Check\\imgForCanny1-38.jpg',0)
##img = cv2.imread(path+'Check\\test.png',0)
##img = cv2.imread('test.jpg',0)
#print(img)
#
#plt.figure()
#plt.imshow(img, cmap='gray')
#
#im = img.copy()
#plt.figure()
#plt.hist(im.ravel(),256,[0,256]); plt.show()
#
#minV = np.float64(np.min(im))
#maxV = np.float64(np.max(im))
#print(type(maxV))
#print('minV = ' +str(minV))
#print('maxV = ' +str(maxV))
#threshold = 2*(minV + maxV)/3.0
#print('threshold = ' +str(threshold))
##threshold=150
#otsu, _ = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#print(otsu)
#print('%d, %d' %(threshold, otsu))
#ret, thresh = cv2.threshold(img, otsu, 255, cv2.THRESH_BINARY) #THRESH_BINARY_INV #THRESH_BINARY
#print(thresh)
#
#edges = cv2.Canny(img,otsu*4/3,otsu*1/3)
#
#plt.figure()
#plt.imshow(thresh, cmap='gray')
#
#plt.figure()
#plt.imshow(edges, cmap='gray')
#
#th=thresh.copy()
#imgR,contours, hierarchy = cv2.findContours(th, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#
#width, height = im.shape
#blank_image = np.zeros((width, height), np.uint8)
#cv2.drawContours(blank_image , contours, -1, 255)
##
#plt.figure()
#plt.imshow(blank_image, cmap='gray')

#hist = cv2.calcHist([img],[0],None,[256],[0,256])
#hist,bins = np.histogram(img.ravel(),256,[0,256])
#edges = cv2.Canny(img,100,200)
#print(edges)
#
#plt.subplot(121),plt.imshow(img,cmap = 'gray')
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
#plt.show()



#if platform.system() == 'Linux':
#    d = path[:-1].rfind('/')
#elif platform.system() == 'Windows': 







def plotVelocityProfile():
    width = 8e-3
    height = 4e-3
    step=width/100.0
    
    v=[]
    ypos=np.arange(-width/2.0, width/2.0+step, step)
    
    for y in ypos:
        v.append(tr.velocityRectPoiseuille(P=None, Q=50, y=y, z=height/2.0, w=width, h=height, nmax=100, rho=1000, nu = 5000))
    
    v= np.array(v)
    v=v*1e3
    ypos=ypos*1e3
    from matplotlib import pylab as plt
    plt.close('all')
    plt.figure()
    plt.plot(ypos, v , 'o', markersize=1)
    plt.xlim([-4, 4])
    plt.ylim([0, np.max(v)*1.1])
    plt.xlabel('y- Position [mm]')
    plt.ylabel('Fluid Velocity [mm/s]' )
    
#plotVelocityProfile()



#
#directory = 'M:\\EdgarHaener\\Capsules\\Batch260615-001\\T-Junction\\2015-07-01\\Batch260615-001_#13\\'
#
#fpss=[10, 40, 60, 70, 100, 120, 140]
#problems2=[]
#for fps in fpss:
#    try:
#        tr.runOneFPS(directory, d0=3.6,  pPmm=22.3, FPS=fps, rotateImages=-0.3, threshold=145)
#    except:
#        problems2.append("%d didn't complete" %fps)
#
#
#print('\n\n\n ')
#print(problems1)
#print(problems2)
        

#path2=path+'Batch260615-001-#17-10FPS-5mlPmin-1-0000.png'
#lon.chancellery@eda.admin.ch
#import cv2
#from matplotlib import pyplot as plt
#blockSize=25
#c=5
#img = cv2.imread(path2,0)
#img = cv2.medianBlur(img,5)
#
#ret,th1 = cv2.threshold(img,145,255,cv2.THRESH_BINARY)
#th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#            cv2.THRESH_BINARY,blockSize,c)
#th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#            cv2.THRESH_BINARY,blockSize,c)
#
#titles = ['Original Image', 'Global Thresholding (v = 127)',
#            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
#images = [img, th1, th2, th3]
#
#for i in xrange(4):
#    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#    plt.title(titles[i])
#    plt.xticks([]),plt.yticks([])
#plt.show()

#directory = 'M:\\EdgarHaener\\Capsules\\Batch260615-001\\T-Junction\\2015-07-01\\Batch260615-001_#13\\'
#path = directory + 'Batch260615-001-#13-70FPS-35mlPmin-1\\Test\\'

def subBackground(path, i=0):
        import cv2
        img = cv2.imread(path+'Batch260615-001-#13-70FPS-35mlPmin-1-%04d.png'  %(i), 0)
        cv2.imshow('Origninal', img)
        back = cv2.imread(path+'Background.png',0)
        cv2.imshow('Background', back)
        newImg = img - back
#        newImg = back - img
        cv2.imshow('Rslt', newImg)
        
        newImg2 = cv2.absdiff(img, back)
        cv2.imshow('Rslt 2', newImg2)
        
#subBackground(path, i=35)
        
def medianFilter(path, i=0):
        import cv2
        spath = path+'Batch260615-001-#17-100FPS-50mlPmin-2-%04d.png'  %i
#        spath = path+'Check\\imgSubbed-%d.jpg'  %i
        if os.path.exists(spath):   
            print("File found!")
        else:
            print("File not found!")
            print(os.listdir(path))
        img = cv2.imread(spath,0)
        im1 =img.copy()
        im2 = img.copy()
        
        for ii in range(40):
            im1 = cv2.medianBlur(im1, ksize=5)
            if ii%2 == 0:
                im2 = cv2.medianBlur(im2, ksize=1+ii)
        cv2.imshow('im1', im1)
        cv2.imshow('im2', im2)
#        cv2.waitKey(5)
        


#        img = cv2.imread('die.png')
        print('Denoising')
        dst = cv2.fastNlMeansDenoising(img,None,10,7,21)
        cv2.imshow('img', img)
        cv2.imshow('dst', dst)
        cv2.imwrite(path + 'img.jpg', img)
        cv2.imwrite(path + 'dst.jpg', dst)
        cv2.waitKey(5)
        print('finished')


#medianFilter(path, i=71)

def tryOutAdpativeThresholding(path, d0, pPmm, i=0):
        import cv2
        A0=np.pi*np.power(d0/2,2)
#        print(path)
#        spath = path+'Batch260615-001-#17-100FPS-50mlPmin-2-%04d.png'  %i
        spath = path+'Check\\imgSubbed-%d.jpg'  %i
        if os.path.exists(spath):   
            print("File found!")
        else:
            print("File not found!")
            print(os.listdir(path))
        img = cv2.imread(spath,0)
            #Get size of image
        yImg,xImg = img.shape
        
#        #Add a rectanlge over areas of image not of intrest, to prevent 
#        #interference from these areas        
#        
#        borderSize=10
#        
#        #add a border of black pixels around image in case capsule touches edge    
#        img=cv2.copyMakeBorder(img,borderSize,borderSize,borderSize,borderSize,
#                               cv2.BORDER_CONSTANT,value=(255, 255, 255)) 
#        
#        paddingOffset=5        
#        
#        topCropLevel=25+borderSize #where to cut the top of the image
##        topCropLevel=66+borderSize #where to cut the top of the image
#        
##        dex=125  # daugther channel bottom edge        
#        dex=114  # daugther channel bottom edge    
#        leftEdge=559
#        rightEdge=733
#        
##        #PCO SETUp
##        cv2.rectangle(img, (0, dex+borderSize+paddingOffset), (540+borderSize-paddingOffset, yImg), 255,
##                      thickness=-1)   
##        cv2.rectangle(img, (725+borderSize+paddingOffset, dex+borderSize+paddingOffset), (xImg, yImg),  255,
##                      thickness=-1)
##        #Block out timestamp from pco camera
##        cv2.rectangle(img, (0+borderSize, 0+borderSize), (xImg+borderSize, topCropLevel), 255,
##                      thickness=-1)
#                      
#        #PCO SETUp
#        cv2.rectangle(img, (0, dex+borderSize+paddingOffset), (leftEdge+borderSize-paddingOffset, yImg), 255,
#                      thickness=-1)   
#        cv2.rectangle(img, (rightEdge+borderSize+paddingOffset, dex+borderSize+paddingOffset), (xImg, yImg),  255,
#                      thickness=-1)
#        #Block out timestamp from pco camera
#        cv2.rectangle(img, (0+borderSize, 0+borderSize), (xImg+borderSize, topCropLevel), 255,
#                      thickness=-1)
                      
        im =img.copy()
        cnt, thresh, xBT,yBT,w,h = tr.findContoursByAdpativeThresholding(img,  plot=True, counter=i, path=path, expectedArea=A0*np.power(pPmm,2), printDebugInfo=True)
        
        print(type(cnt))
#        print((cnt))
        if cnt != None:
            x, y =thresh.shape
            size = (w, h, channels) = (x, y, 1)
            canvas = np.zeros(size, np.uint8)
            cv2.drawContours(canvas, cnt, -1, 255)
            cv2.imshow('Contour', canvas)
            
            cv2.drawContours(im, cnt, -1, 0)
            cv2.imshow('Imag + Contour', im)
            
            cv2.imshow('Thres', thresh)
        cv2.waitKey(5000)

#tryOutAdpativeThresholding(path,d0=3.6, pPmm=22.3, i=0)


#tr.track_bubble(path, d0=10, pPmm=6.8, constantFrequency=False, rotate=0.0, plot=False, threshold=120, printDebugInfo=False)


#tr.testThresholds(path, rotate=0, thresholds=[20, 60, 120, 150, 180, 210], tiff=False)
#
def minimalExample(path):
    import cv2
    import matplotlib.pyplot as plt

    img = cv2.imread(path+'Check\\Img_0.jpg',0)
    print(img)
    #plt.imshow(img, cmap='Greys')
#    cv2.imshow('Original', img)
    
    edges = cv2.Canny(img,50,150) 
    cv2.imshow('Canny', edges)
    cv2.imwrite(path+'Check\\Img_0_Cannied_50-150.jpg', edges)
    
    contours, hierarchy = cv2.findContours(edges,cv2.cv.CV_RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_NONE)
    contours = tr.selectContour(contours)
    
    counter=-1
    for cnt in contours:
        counter += 1
        measureCuravture = tr.findMaxCurvatureInContour(img, cnt)
        measureCuravture = tr.smooth(measureCuravture)
        print('%d: max Curvature = %f \t' %(counter, max(measureCuravture)), end="")
        
        M = cv2.moments(cnt) 
        print('Area = %f \t' %M['m00'], end="")
    
        cntHull = cv2.convexHull(cnt, returnPoints=True)
        cntPoly=cv2.approxPolyDP(cnt, epsilon=1, closed=True)
        MHull = cv2.moments(cntHull)
        MPoly = cv2.moments(cntPoly)
        print('Area after Convec Hull = %f \t Area after apporxPoly = %f \t' %(MHull['m00'], MPoly['m00']), end="")
    
    x, y =img.shape
    size = (w, h, channels) = (x, y, 1)
    canvas = np.zeros(size, np.uint8)
    cv2.drawContours(canvas, cnt, -1, 255)
    cv2.imwrite(path+'Check\\Img_0_ContoursCnt.jpg', canvas)
    
    canvas = np.zeros(size, np.uint8)
    cv2.drawContours(canvas, cntHull, -1, 255)
    cv2.imwrite(path+'Check\\Img_0_ContoursCntHull.jpg', canvas)
    canvas = np.zeros(size, np.uint8)
    cv2.drawContours(canvas, cntPoly, -1, 255)
    cv2.imwrite(path+'Check\\Img_0_ContoursCntPoly.jpg', canvas)
    
def minimalExample2(path):
    import cv2
    img = cv2.imread(path+'Check\\Img_0.jpg',0)
    cv2.imshow('Original', img)
    
    edges = cv2.Canny(img,50,150) 
    cv2.imshow('Canny', edges)
    
    contours, hierarchy = cv2.findContours(edges,cv2.cv.CV_RETR_EXTERNAL,cv2.cv.CV_CHAIN_APPROX_NONE)
    
    cnt = contours[0] #I have a function to do this but for simplicity here by hand
    
    M = cv2.moments(cnt) 
    print('Area = %f \t' %M['m00'], end="")

    cntHull = cv2.convexHull(cnt, returnPoints=True)
    cntPoly=cv2.approxPolyDP(cnt, epsilon=0, closed=True)
    MHull = cv2.moments(cntHull)
    MPoly = cv2.moments(cntPoly)
    print('Area after Convec Hull = %f \t Area after apporxPoly = %f \n' %(MHull['m00'], MPoly['m00']), end="")
    
    x, y =img.shape
    size = (w, h, channels) = (x, y, 1)
    canvas = np.zeros(size, np.uint8)
    cv2.drawContours(canvas, cnt, -1, 255)
    cv2.imshow('Contour', canvas)
    
    canvas = np.zeros(size, np.uint8)
    cv2.drawContours(canvas, cntHull, -1, 255)
    cv2.imshow('Hull', canvas)

    canvas = np.zeros(size, np.uint8)
    cv2.drawContours(canvas, cntPoly, -1, 255)
    cv2.imshow('Poly', canvas)
    



    
    
#minimalExample2(path)