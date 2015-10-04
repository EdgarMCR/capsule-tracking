# -*- coding: utf-8 -*-
"""
Reads in the autmoatically generated results file and returns the nessecary
information. 

Created on Wed Apr 01 10:23:00 2015

@author: mbbxkeh2
"""
#
#path='M:\\EdgarHaener\\Capsules\\RigidParticle-3.5mm\\31032015\\RigidParticle-3.5mm-31032015_Results.txt'
from __future__ import absolute_import, division, print_function
import numpy as np
import matplotlib.pylab as plt
import platform
import scipy as sp
import os
from scipy.optimize import curve_fit
from scipy.stats import chisqprob



class ResultsClass:
    """A class to hold and read results from T-Junction experiments"""
    
    def __init__(self, path1):
        self.path = path1
        self.volumFlux =[]
        self.name = []
        self.minSpeed = []
        self.SpeedMain = [] 
        self.SpeedDaugther = []
        self.timeInTJ=[]
        self.timeGeoInTJ=[]
        self.offCentre = []
        self.turned = []
        self.maxWidth = []
        self.maxD12 = []
        self.d12Main = []
        self.d12Daugther = []
        self.relaxationTime = []
        self.relaxationDistance = []
        self.maxAccerleration=[]
        self.minAccerleration=[]
        self.pixelsPmm=-1
        
        #read in the data
        self.readData()
        
        self.texSaveNames = True
            
    def printData(self):
        print('Vol Flux \tname \tmin speed, \tave speed 1, \tave speed 2, \ttime, \tOff-centre, \tturned')
        for i in range(len(self.volumFlux)):
            print('%.2f \t%s \t%.2f  \t%.2f \t%.2f \t%.2f \t%.2f \t%s' %(self.volumFlux[i], self.name[i], self.minSpeed[i], self.SpeedMain[i], self.SpeedDaugther[i], self.timeInTJ[i], self.offCentre[i], self.turned[i] ))
            

        
    def readData(self):
        """ Expecte file with the following entries:
        Vol Flux, name, min speed, ave speed 1, ave speed 2, time, Off-centre, turned 
        """
        #This opens a handle to your file, in 'r' read mode
        file_handle = open(self.path, 'r')
        
        # Read in all the lines of your file into a list of lines
        lines_list = file_handle.readlines()
        
        
        indexC=0
        linecounter=-1
        
        for line in lines_list:
            linecounter=linecounter+1
            if linecounter==0 : #ignore first line as it contains the header
                continue
            
            entries=line.split()
        #    print(entries)
        #    print(' \t len(entries) = '+str(len(entries)))
            if len(entries)>=8:
                self.volumFlux.append(float(entries[0]))
                self.name.append(entries[1])
                self.minSpeed.append(float(entries[2]))
                self.SpeedMain.append(float(entries[3]) )
                self.SpeedDaugther.append(float(entries[4]))
                self.timeInTJ.append(float(entries[5]))
                self.offCentre.append(float(entries[6]))
                self.turned.append(entries[7])  
            if len(entries)>=9:
                self.timeGeoInTJ.append(float(entries[8]))
            if len(entries)>=11:
                self.maxWidth.append(float(entries[9]))
                self.maxD12.append(float(entries[10]))
            if len(entries) >= 15:
                self.d12Main.append(float(entries[13]))
                self.d12Daugther.append(float(entries[14]))
            if len(entries) >= 17:
                self.relaxationTime.append(float(entries[15]))
                self.relaxationDistance.append(float(entries[16]))
            if len(entries) >= 19:
                self.maxAccerleration.append(float(entries[17]))
                self.minAccerleration.append(float(entries[18]))
            indexC=indexC+1        
            
        self.volumFlux=np.array(self.volumFlux)
        self.minSpeed=np.array(self.minSpeed)
        self.SpeedMain=np.array(self.SpeedMain)
        self.SpeedDaugther=np.array(self.SpeedDaugther)
        self.timeInTJ=np.array(self.timeInTJ)
        self.timeGeoInTJ=np.array(self.timeGeoInTJ)
        self.offCentre=np.array(self.offCentre)
        self.maxWidth = np.array(self.maxWidth) 
        self.maxD12 = np.array(self.maxD12)
        self.d12Main = np.array(self.d12Main)
        self.d12Daugther = np.array(self.d12Daugther)
        self.relaxationTime = np.array(self.relaxationTime)
        self.relaxationDistance = np.array(self.relaxationDistance)
        self.maxAccerleration  = np.array(self.maxAccerleration)
        self.minAccerleration  = np.array(self.minAccerleration)

    def averageByQ(self, xInput):
        '''     Average the values for each volumn flux and return average and std     '''
        if not hasattr(self, "volumFluxesList"):
            #get all volumn fluxes
            self.volumFluxesList=[]
            for VF in self.volumFlux:
                isInList=False
                for x in self.volumFluxesList:
                    if VF == x:
                        isInList=True
                
                if not isInList:
                    self.volumFluxesList.append(VF)
        
        lenvfl=len(self.volumFluxesList)

        x=np.zeros((lenvfl))
        xSTD=np.zeros((lenvfl))
        
        counter=0
        for vfl in self.volumFluxesList:
            tempx=[]
#            print('Counter =%d' %counter)
            for i in range(len(self.volumFlux)):
                if self.volumFlux[i] == vfl:
                    tempx.append(xInput[i])
                    
            x[counter]=np.average(tempx)
            xSTD[counter]=np.std(tempx, ddof=1)
            
            counter +=1
            
        return x, xSTD
                
    def averageSpeed(self):
        #sort by volumn fluxes and then average
        self.volumFluxesList=[]
        for VF in self.volumFlux:
            isInList=False
            for x in self.volumFluxesList:
                if VF == x:
                    isInList=True
            
            if not isInList:
                self.volumFluxesList.append(VF)
            
        #self.volumFlux and self.aveSpeed are same length
        lenvfl=len(self.volumFluxesList)
#        print('len(volumFluxesList) = %d' %lenvfl)
        self.aveSpeedMain=np.zeros((lenvfl,1))
        self.aveSpeedMainSTD=np.zeros((lenvfl, 1))
        self.aveSpeedDaugther=np.zeros((lenvfl, 1))
        self.aveSpeedDaugtherSTD=np.zeros((lenvfl, 1))
        self.aveTimeinTJ=np.zeros((lenvfl, 1))
        self.aveTimeinTJSTD=np.zeros((lenvfl, 1))
        self.aveGeoTimeinTJ=np.zeros((lenvfl, 1))
        self.aveGeoTimeinTJSTD=np.zeros((lenvfl, 1))
        
        self.aveMaxWidth=np.zeros((lenvfl, 1))
        self.aveMaxWidthSTD=np.zeros((lenvfl, 1))
        self.aveMaxD12=np.zeros((lenvfl, 1))
        self.aveMaxD12STD=np.zeros((lenvfl, 1))
        
        self.aveD12Main=np.zeros((lenvfl, 1))
        self.aveD12MainSTD=np.zeros((lenvfl, 1))
        self.aveD12Daugther=np.zeros((lenvfl, 1))
        self.aveD12DaugtherSTD=np.zeros((lenvfl, 1))
        
        self.aveRelaxationTime=np.zeros((lenvfl, 1))
        self.aveRelaxationTimeSTD=np.zeros((lenvfl, 1))
        self.aveRelaxationDistance=np.zeros((lenvfl, 1))
        self.aveRelaxationDistanceSTD=np.zeros((lenvfl, 1))
        
        tempsortedSpeeds=[]
        tempsortedSpeedDs=[]
        tempsortedOffsets=[]
        
        offsetByVFt=[[] for i in range(lenvfl)] 
        timeInTJByVFt=[[]for i in range(lenvfl)] 
        timeGeoInTJByVFt=[[]for i in range(lenvfl)]
        
#        print('len(self.d12Main) = %d' %len(self.d12Main))
        counter=0
        for vfl in self.volumFluxesList:
            tempMain=[]
            tempDaugther=[]
            tempTime=[]
            tempGeoTime=[]
            tempMaxWidth=[]
            tempMaxD12 = []
            tempsortedSpeed = [] 
            tempsortedSpeedD = [] 
            tempsortedOffset = [] 
            tempd12Main = []
            tempd12Daugther = []
            temprt = []
            temprd = []
#            print('Counter =%d' %counter)
            for i in range(len(self.volumFlux)):
                if self.volumFlux[i] == vfl:
#                    print('Volumn Flux = %.2f' %vfl)
                    tempMain.append(self.SpeedMain[i])
                    tempDaugther.append(self.SpeedDaugther[i])
                    tempTime.append(self.timeInTJ[i])
                    tempGeoTime.append(self.timeGeoInTJ[i])
                    tempMaxWidth.append(self.maxWidth[i])
                    tempMaxD12.append(self.maxD12[i])
                    tempsortedSpeed.append(self.SpeedMain[i])
                    tempsortedSpeedD.append(self.SpeedDaugther[i])
                    tempsortedOffset.append(self.offCentre[i])
                    
                    offsetByVFt[counter].append(self.offCentre[i])
                    timeInTJByVFt[counter].append(self.timeInTJ[i])
                    timeGeoInTJByVFt[counter].append(self.timeGeoInTJ[i])
                    tempd12Main.append(self.d12Main[i])
                    tempd12Daugther.append(self.d12Daugther[i])
                    temprt.append(self.relaxationTime[i])
                    temprd.append(self.relaxationDistance[i])
                    
#            print('len = %d' %len(aveSpeedMain))
            tempsortedSpeeds.append(np.array(tempsortedSpeed))
            tempsortedSpeedDs.append(np.array(tempsortedSpeedD))
            tempsortedOffsets.append(np.array(tempsortedOffset))
            
            self.aveSpeedMain[counter]=np.average(tempMain)
            self.aveSpeedMainSTD[counter]=np.std(tempMain, ddof=1)
            self.aveSpeedDaugther[counter]=np.average(tempDaugther)
            self.aveSpeedDaugtherSTD[counter]=np.std(tempDaugther, ddof=1)
            
            self.aveTimeinTJ[counter]=np.average(tempTime)
            self.aveTimeinTJSTD[counter]=np.std(tempTime, ddof=1)
            
            self.aveGeoTimeinTJ[counter]=np.average(tempGeoTime)
            self.aveGeoTimeinTJSTD[counter]=np.std(tempGeoTime, ddof=1)
            
            self.aveMaxWidth[counter]=np.average(tempMaxWidth)
            self.aveMaxWidthSTD[counter]=np.std(tempMaxWidth, ddof=1)
            self.aveMaxD12[counter]=np.average(tempMaxD12)
            self.aveMaxD12STD[counter]=np.std(tempMaxD12, ddof=1)
            
            self.aveD12Main[counter]=np.average(tempd12Main)
            self.aveD12MainSTD[counter]=np.std(tempd12Main, ddof=1)
            self.aveD12Daugther[counter]=np.average(tempd12Daugther)
            self.aveD12DaugtherSTD[counter]=np.std(tempd12Daugther, ddof=1)
            
            self.aveRelaxationTime[counter]=np.average(temprt)
            self.aveRelaxationTimeSTD[counter]=np.std(temprt, ddof=1)
            self.aveRelaxationDistance[counter]=np.average(temprd)
            self.aveRelaxationDistanceSTD[counter]=np.std(temprd, ddof=1)
            
            
            #flatten the arryas
            self.aveSpeedMain=self.aveSpeedMain.flatten()
            self.aveSpeedDaugther=self.aveSpeedDaugther.flatten()
            self.aveTimeinTJ=self.aveTimeinTJ.flatten()        
#            self.aveMaxWidth = self.aveMaxWidth.flatten()
#            self.aveMaxD12 = self.aveMaxD12.flatten()
            
            self.aveSpeedMainSTD=self.aveSpeedMainSTD.flatten()
            self.aveSpeedDaugtherSTD=self.aveSpeedDaugtherSTD.flatten()
            self.aveTimeinTJSTD=self.aveTimeinTJSTD.flatten()
#            self.aveMaxWidthSTD = self.aveMaxWidtself.d12MainhSTD.flatten()
#            self.aveMaxD12STD = self.aveMaxD12STD.flatten()
            
            counter+=1
        
        self.volumFluxesList=np.array(self.volumFluxesList)
                
        self.sortedSpeedMain = np.array(tempsortedSpeeds)
        self.sortedSpeedDaugther = np.array(tempsortedSpeedDs)
        self.sortedOffset = np.array(tempsortedOffsets)
        
#        print(offsetByVFt)
#        self.offsetByVF = np.array([np.array(xi) for xi in offsetByVFt]) 
#        self.timeInTJByVF = np.array([np.array(xi) for xi in timeInTJByVFt]) 
#        self.timeGeoInTJByVF = np.array([np.array(xi) for xi in offsetByVFt]) 
        
#        self.offsetByVF = np.array(offsetByVFt) 
#        self.timeInTJByVF = np.array(timeInTJByVFt) 
#        self.timeGeoInTJByVF = np.array(offsetByVFt)
        self.offsetByVF = offsetByVFt
        self.timeInTJByVF = timeInTJByVFt
        self.timeGeoInTJByVF = offsetByVFt

        self.aveMaxAccerleration, self.aveMaxAccerlerationSTD =  self.averageByQ( self.maxAccerleration )
        self.aveMinAccerleration, self.aveMinAccerlerationSTD =  self.averageByQ( self.minAccerleration )
        
        return self.volumFluxesList, self.aveSpeedMain, self.aveSpeedMainSTD, self.aveSpeedDaugther, self.aveSpeedDaugtherSTD, self.aveTimeinTJ, self.aveTimeinTJSTD
        
    def printAverageSpeed(self):
        self.averageSpeed()
        print('volumFluxesList, aveSpeedMain, aveSpeedMainSTD, aveSpeedDaugther, aveSpeedDaugtherSTD, aveTimeinTJ, aveTimeinTJSTD')
        for i in range(len(self.volumFluxesList)):
            print('%2f ,\t  %2f ,\averageSpeed(t %2f ,\t %2f ,\t %2f,\t %2f ,\t %2f' %(self.volumFluxesList[i], self.aveSpeedMain[i], self.aveSpeedMainSTD[i], self.aveSpeedDaugther[i], self.aveSpeedDaugtherSTD[i], self.aveTimeinTJ[i], self.aveTimeinTJSTD[i]))
#        avetimeInTJ
    def findSpeedGradientFromAverages(self):
        '''
        Fits gradient to speed versus volumn flux based on averages
        '''
        if self.pixelsPmm == -1 :
            raise NameError('pixelsPmm was not defined')
        
        if not hasattr(self, 'volumFluxesList'):
            self.averageSpeed()
        
        self.aveGradientSpeedMain, self.aveGradientSpeedMainRChi2, self.aveGradientSpeedMainErr, self.aveGradientSpeedMainPValue, self.aveGradientSpeedMainR2 = self.fitStraightLineScipy(self.volumFlux, self.SpeedMain/self.pixelsPmm)
        self.aveGradientSpeedDaugther, self.aveGradientSpeedDaugtherRChi2, self.aveGradientSpeedDaugtherErr, self.aveGradientSpeedDaugtherPValue, self.aveGradientSpeedDaugtherR2 = self.fitStraightLineScipy(self.volumFlux, self.SpeedDaugther/self.pixelsPmm)

        return self.aveGradientSpeedMain, self.aveGradientSpeedMainRChi2, self.aveGradientSpeedMainErr, self.aveGradientSpeedDaugther, self.aveGradientSpeedDaugtherRChi2, self.aveGradientSpeedDaugtherErr   
        
        
    def fitStraightLineScipy(self, x,y, yerr=None):
        '''Fit straight line to data with zero intercept'''
        
        x = np.array(x)
        y = np.array(y)
        fitfunc = lambda p, x: np.array(p*x) # Target function
        errfunc = lambda p, x, y: fitfunc(p, x) - np.array(y) # Distance to the target function
        
        m, pcov = sp.optimize.curve_fit(fitfunc, x, y,  p0=0.75)

        ss_err=(errfunc(m, x, y)**2).sum()
        ss_tot=((y-y.mean())**2).sum()
        rsquared=1-(ss_err/ss_tot)
        
        if yerr: 
            yerr = np.array(yerr)
            chi2 = (errfunc(m,x, y)**2).sum()/(yerr**2).sum()
            p = sp.stats.chisqprob(chi2, len(self.volumFluxesList)-1)
        else:
            chi2, p = sp.stats.chisquare(f_obs=x, f_exp=fitfunc(m, x), ddof=len(self.volumFluxesList)-1)

        RChi2 = chi2/(len(self.volumFluxesList)-1)  #the reduced chi-squared of the fit        
        perr = np.sqrt(np.diag(pcov))

        return m, RChi2, perr, p, rsquared

    def findSpeedGradient(self):            
        '''
        Fits gradient to speed versus volumn flux.
        
        Based on http://stackoverflow.com/questions/14854339/in-scipy-how-and-why-does-curve-fit-calculate-the-covariance-of-the-parameter-es
        
        pcov :  The estimated covariance of popt. The diagonals provide the variance of the parameter estimate. To compute one standard deviation errors on the parameters use perr = np.sqrt(np.diag(pcov)).
        '''
        
        if not hasattr(self, 'volumFluxesList'):
            self.averageSpeed()
        
        self.gradientSpeedMain, self.gradientSpeedMainRChi2, self.gradientSpeedMainErr, self.gradientSpeedMainPValue, self.gradientSpeedMainR2 = self.fitStraightLineScipy(self.volumFlux, self.SpeedMain/self.pixelsPmm)
        self.gradientSpeedDaugther, self.gradientSpeedDaugtherRChi2, self.gradientSpeedDaugtherErr, self.gradientSpeedDaugtherPValue, self.gradientSpeedDaugtherR2 = self.fitStraightLineScipy(self.volumFlux, self.SpeedDaugther/self.pixelsPmm)

        return self.gradientSpeedMain, self.gradientSpeedMainRChi2, self.gradientSpeedMainErr, self.gradientSpeedDaugther, self.gradientSpeedDaugtherRChi2, self.gradientSpeedDaugtherErr
    
    def findDeformationGradient(self):            
        '''
        Fits gradient to speed versus volumn flux.
        
        Based on http://stackoverflow.com/questions/14854339/in-scipy-how-and-why-does-curve-fit-calculate-the-covariance-of-the-parameter-es
        
        pcov :  The estimated covariance of popt. The diagonals provide the variance of the parameter estimate. To compute one standard deviation errors on the parameters use perr = np.sqrt(np.diag(pcov)).
        '''
        
        if not hasattr(self, 'volumFluxesList'):
            self.averageSpeed()
        self.gradientD12Main, self.gradientD12MainRChi2, self.gradientD12MainErr, self.gradientD12MainPValue, self.gradientD12MainR2 = self.fitStraightLineScipy(self.volumFlux, self.d12Main)
        self.gradientD12Daugther, self.gradientD12DaugtherRChi2, self.gradientD12DaugtherErr, self.gradientD12DaugtherPValue, self.gradientD12DaugtherR2 = self.fitStraightLineScipy(self.volumFlux, self.d12Daugther)


    def printSpeedGradient(self):
        self.findSpeedGradient()
        print('Gradient Main Channel %.2f p/m %0.3f \t  Gradient Daugther Channel %.2f p/m %0.3f ' %(self.gradientSpeedMain, self.gradientSpeedMainSTD, self.gradientSpeedDaugther, self.gradientSpeedDaugtherSTD)),

    def turnedDirection(self):
        self.turnedDirection= np.zeros((len(self.turned),1), dtype=int)
        volumnFluxTurnedRight=[]
        offCentreTurnedRight=[]
        for ll in range(len(self.turned)):
            if self.turned[ll] == 'right':
                self.turnedDirection[ll]=0
                volumnFluxTurnedRight.append(self.volumFlux[ll])
                offCentreTurnedRight.append(self.offCentre[ll])
            elif self.turned[ll] == 'left':
                self.turnedDirection[ll]=1
            else:
                self.turnedDirection[ll]=-1
        self.volumnFluxTurnedRight=np.array(volumnFluxTurnedRight)
        self.offCentreTurnedRight=np.array(offCentreTurnedRight)
        return self.turnedDirection, self.volumnFluxTurnedRight, self.offCentreTurnedRight
    
    def find1oQGradientFromAverages(self):
        '''
        Fits gradient to 1/volumn flux versus average time in T-Junction
        '''            
        if not hasattr(self, 'volumFluxesList'):
            self.averageSpeed()
        
        self.aveGradient1oQ, self.aveGradient1oQRChi2, self.aveGradient1oQErr, self.aveGradient1oQPValue, self.aveGradient1oQR2 = self.fitStraightLineScipy(1.0/self.volumFluxesList, self.aveTimeinTJ)
        
        
        return self.aveGradient1oQ, self.aveGradient1oQErr, self.aveGradient1oQRChi2, self.aveGradient1oQPValue
        
    def find1oQGradient(self):            
        '''
        Fits gradient to 1/volumn flux versus time in T-Junction
        
        Based on http://stackoverflow.com/questions/14854339/in-scipy-how-and-why-does-curve-fit-calculate-the-covariance-of-the-parameter-es
        
        pcov :  The estimated covariance of popt. The diagonals provide the variance of the parameter estimate. To compute one standard deviation errors on the parameters use perr = np.sqrt(np.diag(pcov)).
        '''
        if not hasattr(self, 'volumnFluxSOffset'):
            self.sortbyOffsetAroundCenter()

        self.gradient1oQ, self.gradient1oQRChi2, self.gradient1oQErr, self.gradient1oQPValue, self.gradient1oQR2 = self.fitStraightLineScipy(1.0/self.volumFlux, self.timeGeoInTJ)
        if len(self.volumnFluxSOffset) > 0:
            self.gradient1oQSOffset, self.gradient1oQSOffsetRChi2, self.gradient1oQSOffsetErr, self.gradient1oQSOffsetPValue, self.gradient1oQSOffsetR2 = self.fitStraightLineScipy(1.0/self.volumnFluxSOffset, self.timeInTJGeoSOffset) 
        return self.gradient1oQ, self.gradient1oQErr, self.gradient1oQRChi2, self.gradient1oQPValue
    

        
    def sortByOffset(self, binWidth=1):
        '''Sort offsets into bins x pixel wides'''
        #find min and max
        minOffset=int(np.round(np.min(self.offCentre))-1)
        maxOffset=int(np.round(np.max(self.offCentre))+1)
#        print('minOffset = %d \t maxOffset = %d'%(minOffset, maxOffset))
#        print(sorted(self.offCentre))
        
        numBins =int(np.ceil( (maxOffset - minOffset)/binWidth))
        print('numBins = %d \t (maxOffset - minOffset) = %d' %(numBins, (maxOffset - minOffset)))
        
        binnedOffsett=[[] for i in range(numBins)] 
        binnedVolumFluxt=[[]for i in range(numBins)] 
        binnedTimeInTJt=[[]for i in range(numBins)] 
        binnedTimeGeoInTJt=[[]for i in range(numBins)] 
#        print('min = %d , max = %d , numBins = %d' %(minOffset, maxOffset, numBins))
#        print(binnedOffset)
        
        numOfAppends=0
        for bb in range(0,numBins):
            binMin=minOffset+bb*binWidth+0.0
            binMax=binMin+binWidth
#            print('binMin + %.0f \tbinMax = %.0f' %(binMin, binMax))
            for jj in range(len(self.offCentre)):
                if self.offCentre[jj] >= binMin and self.offCentre[jj] < binMax :
                    numOfAppends += 1
                    binnedOffsett[bb].append(self.offCentre[jj])
                    binnedVolumFluxt[bb].append(self.volumFlux[jj])
                    binnedTimeInTJt[bb].append(self.timeInTJ[jj])
                    binnedTimeGeoInTJt[bb].append(self.timeGeoInTJ[jj])
        
        numOfData=0        
        for x in binnedOffsett:
            numOfData += len(x)
        
        if numOfData != len(self.offCentre):
            print('Befor numpying numOfData = %d but there are %d data points' %(numOfData, len(self.offCentre)))
        
        #Convert from list to numpy array
        self.binnedOffset = np.array([np.array(xi) for xi in binnedOffsett])
        self.binnedVolumFlux = np.array([np.array(xi) for xi in binnedVolumFluxt])  
        self.binnedTimeInTJ = np.array([np.array(xi) for xi in binnedTimeInTJt])  
        self.binnedTimeGeoInTJ = np.array([np.array(xi) for xi in binnedTimeGeoInTJt]) 

        numOfData=0        
        for x in self.binnedOffset:
            numOfData += len(x)
        
        if numOfData != len(self.offCentre):
            print('numOfData = %d but there are %d data points' %(numOfData, len(self.offCentre)))
        
        assert numOfData == len(self.offCentre)
#        print('numOfData = %d \tnumOfAppends = %d' %(numOfData, numOfAppends))
        return self.binnedOffset, self.binnedVolumFlux, self.binnedTimeInTJ, self.binnedTimeGeoInTJ

    def sortbyOffsetAroundCenter(self, widthAroundStreamline=0.07):
        '''Select data points close to central streamline'''
        wASP = widthAroundStreamline*self.pixelsPmm
        
        volumnFluxSOffset =[]
        speedMainSOffset =[]
        speedDaugtherSOffset =[]
        timeinTJSOffset =[]
        timeinTJGeoSOffset =[]
        
        for ii in range(len(self.volumFlux)):
            if (-1*wASP) < self.offCentre[ii] and self.offCentre[ii] < wASP:
                volumnFluxSOffset.append(self.volumFlux[ii])
                speedMainSOffset.append(self.SpeedMain[ii])
                speedDaugtherSOffset.append(self.SpeedDaugther[ii])
                timeinTJSOffset.append(self.timeInTJ[ii])
                timeinTJGeoSOffset.append(self.timeGeoInTJ[ii])
                
        self.volumnFluxSOffset =np.array(volumnFluxSOffset)
        self.speedMainSOffset =np.array(speedMainSOffset)
        self.speedDaugtherSOffset =np.array(speedDaugtherSOffset)
        self.timeInTJSOffset =np.array(timeinTJSOffset)
        self.timeInTJGeoSOffset =np.array(timeinTJGeoSOffset)
    
    def averageTimeByOffset(self, binWidth=1):
        self.sortByOffset(binWidth=binWidth)
        averageTimeBinned=[]
        averageOffsetBinned=[]
        for jj in range(len(self.binnedOffset)):
            if len(self.binnedTimeGeoInTJ[jj]) != 0:
                averageTimeBinned.append(np.average(self.binnedTimeGeoInTJ[jj]))
                averageOffsetBinned.append(np.average(self.binnedOffset[jj]))
        self.averageTimeBinned = np.array(averageTimeBinned)
        self.averageOffsetBinned = np.array(averageOffsetBinned)
        
        return self.averageTimeBinned, self.averageOffsetBinned
        
    def find_batchName(self, path):
        if platform.system() == 'Linux':
            dSlash='/'
        elif platform.system() == 'Windows': 
            dSlash='\\'
        else:
            print('Unknow Oporating System - find_batchName(path) - failed')
            
        d1=path.rfind(dSlash,1,-3)
        reslt=path[d1+1:-1]
        
        d3=reslt.rfind('_R')
        reslt=reslt[0:d3]

        return reslt
        
    def plotAverageBinnedTimeInTJ(self, savepath=None, BatchID = '', show=False, binWidth=1):
        self.averageTimeByOffset(binWidth=binWidth)
        BatchID = self.find_batchName(self.path)
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(self.averageOffsetBinned/self.pixelsPmm, self.averageTimeBinned, 'or-')
        
        ax.set_xlabel("Average Offset in Main Channel [mm]")
        ax.set_ylabel("Nondimensionalised (geometric) Time")
        string = 'pixels/mm = %.1f' %self.pixelsPmm
        plt.text(0.3, 0.8,string,    horizontalalignment='center',      verticalalignment='center',
             transform = ax.transAxes)
        
#        step= ax.get_xaxis().get_data_interval()
#        print(step)
        locs, labels =plt. xticks()
#        print(locs)
        
        ax2 = ax.twiny()
#        ax2.plot(self.averageOffsetBinned, self.averageTimeBinned, 'ob')
        ax2.set_xlim(left=locs[0]*self.pixelsPmm,right=locs[-1]*self.pixelsPmm)
#        ax2.set_xticks(locs)
#        ax2.set_xticklabels((locs*self.pixelsPmm))
        ax2.set_xlabel('Average Offset in Main Channel [pixels]')
        
        plt.title("Average Binned Offset vs Geoemtric Time -  " +BatchID, y=1.08)
        
        if savepath != None:
            plt.savefig(self.makeSaveNameSafe(savepath+'AverageBinnedOffsetVSGeoTime-'+BatchID.replace(' ', '') +'.png'), dpi=300, )
        
        if show:
            plt.show()
        else:
            plt.close()
        
    def plotBinnedTimeInTJ(self, savepath=None, BatchID  = '', BatchIDC ='', show=False, binWidth=1):
        self.averageTimeByOffset(binWidth=binWidth)
        if BatchID == '':
            BatchID = self.find_batchName(self.path)
        
        fig = plt.figure(figsize=(11, 9), dpi=150)
        ax = fig.add_subplot(111)
#        plt.plot(self.offCentre/self.pixelsPmm, self.timeGeoInTJ, '<g')
        plt.plot(self.averageOffsetBinned/self.pixelsPmm, self.averageTimeBinned, 'o-',color='#253494' , label='Averaged', markersize=7)
        numberDataPoints=0
        for ii in range(len(self.binnedOffset)):
            numberDataPoints += len(self.binnedOffset[ii])
            plt.plot(self.binnedOffset[ii]/self.pixelsPmm, self.binnedTimeGeoInTJ[ii], 's',color='#a1dab4',  markersize=5)

        ax.set_xlabel("Offset in Main Channel [mm]")
        ax.set_ylabel("Nondimensionalised Time")
        string = 'Number of Runs = %d \npixels/mm = %.1f \nBin width = %.2f pixels' %(numberDataPoints,self.pixelsPmm, binWidth)
        plt.text(0.3, 0.8,string,    horizontalalignment='center',      verticalalignment='center',
             transform = ax.transAxes)
        
#        step= ax.get_xaxis().get_data_interval()
#        print(step)
        locs, labels =plt. xticks()
#        print(locs)
        
        ax2 = ax.twiny()
#        ax2.plot(self.averageOffsetBinned, self.averageTimeBinned, 'ob')
        ax2.set_xlim(left=locs[0]*self.pixelsPmm,right=locs[-1]*self.pixelsPmm)
#        ax2.set_xticks(locs)
#        ax2.set_xticklabels((locs*self.pixelsPmm))
        ax2.set_xlabel('Offset in Main Channel [pixels]')
        
        plt.title("Offset vs Time -  " +BatchID, y=1.08)
        plt.plot([],[],'o-',color='#253494' ,)
        plt.plot([],[],'s',color='#a1dab4')
        plt.legend(['Averaged', 'Induvidual Runs'])        
        fig.tight_layout()
        ax.xaxis.grid(True, color='#D0D0D0')
        ax.yaxis.grid(True, color='#D0D0D0')
#        plt.grid(color='#D0D0D0', linestyle='--')
        if savepath != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"BinnedTimeInTJ_" +BatchIDC+".png"), dpi=300, )
        
        if show:
            plt.show()
        else:
            plt.close()
    
    def straightLine(self,x, A): 
        '''
        Returns a straight line y=f(x)
        Input
        x       x-value
        A       gradient
        '''
        return A*x
            
    def plotSpeedMainChannel(self, savepath=None, d0=None, BatchID  = '', BatchIDC ='', show=False, plotDaugtherChannel=False):
        self.findSpeedGradient()
        
        #get drag coefficients
        if d0 !=None:
            import track_capsule_TJ_v0p10 as tc
            lamb=d0/np.sqrt(4*7.8)
            k1, k2 = tc.getDragCoef(lamb)
            G=k2/k1
            if plotDaugtherChannel:
                templambda=d0/4.0
                if templambda > 0.95:
                    print('lambda daugther too big, set to 0.95')
                    templambda=0.95
                lambD=templambda
                k1D, k2D = tc.getDragCoef(lambD)
                GD=(k2D/k1D)

        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
        
        size3p5=6
        #errorbar average3p5beforSTD
        plt.errorbar(self.volumFluxesList, self.aveSpeedMain/self.pixelsPmm, yerr=self.aveSpeedMainSTD/self.pixelsPmm, linestyle='None',  marker='h', color = 'b', label='Speed Main Channel', markersize=size3p5) #
        if plotDaugtherChannel:
#            plt.errorbar(self.volumFlux, self.SpeedDaugther/self.pixelsPmm,  linestyle='None',  marker='s', color = 'g', label='Speed Daugther Channel', markersize=3) #
            plt.errorbar(self.volumFluxesList, self.aveSpeedDaugther/self.pixelsPmm, yerr=self.aveSpeedDaugtherSTD/self.pixelsPmm,  linestyle='None',  marker='o', color = 'g', label='Speed Daugther Channel', markersize=size3p5) #
        
        sampleNum=len(self.SpeedMain)
        if d0 !=None:
            if plotDaugtherChannel:
                s2 = 'Error based on standard deviation of sample \nNumber of data points = %d \nLag factor G = %.2f with $\lambda $ = %.2f and $d_0$ = %.2f $mm$ \nLag factor Daugther G = %.2f with $\lambda $ = %.2f' %(sampleNum, G, lamb, d0, GD, lambD)
            else:
                s2='Error based on standard deviation of sample \nNumber of data points = %d \nLag factor G = %.2f with $\lambda $ = %.2f and $d_0$ = %.2f $mm$' %(sampleNum, G, lamb, d0)
        else:
            s2='Error based on standard deviation of sample \nNumber of data points = %d' %sampleNum
            
        xmin, xmax = plt.xlim()
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()
        ymin, ymax = plt.ylim()
        ax2.text(xmin+xmax*0.02, ymin+ymax*0.6, s2, fontsize=10)
        #fit
        if d0 !=None:
            label='Predicted Speed Gradient Main = %.2f' %G
            plt.plot([xmin, xmax], [((2*G*xmin*1000.0/60)/32.0), ((2*G*xmax*1000.0/60)/32.0)], label=label, color='y', linestyle=':', linewidth=1)
            
        label1='Fit Main Channel, m=%.2f +/- %.2f and $R^2$ = %.2f' %(self.gradientSpeedMain, self.gradientSpeedMainErr,self.gradientSpeedMainR2)
        plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradientSpeedMain), self.straightLine(xmax, self.gradientSpeedMain)], label=label1, color='b', linestyle='-.', linewidth=1)
        
        if plotDaugtherChannel:
            label1='Fit Daugther Channel, m=%.2f +/- %.2f and $R^2$ = %.2f' %(self.gradientSpeedDaugther, self.gradientSpeedDaugtherErr,self.gradientSpeedDaugtherR2)
            plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradientSpeedDaugther), self.straightLine(xmax, self.gradientSpeedDaugther)], label=label1, color='g', linestyle='--', linewidth=1)
            if d0 !=None:
                label='Predicted Speed Gradient Daugther = %.2f' %GD
                plt.plot([xmin, xmax], [((2*GD*xmin*1000.0/60)/32.0), ((2*GD*xmax*1000.0/60)/32.0)], label=label, color='r', linestyle=':', linewidth=1)

        plt.plot([xmin, xmax], [((2*xmin*1000.0/60)/32.0), ((2*xmax*1000.0/60)/32.0)], label='2 x Mean Speed', color='k', linestyle='--', linewidth=1)
        plt.plot([xmin, xmax], [((xmin*1000.0/60)/32.0), ((xmax*1000.0/60)/32.0)], label='Mean Speed', color='k', linestyle='-', linewidth=1)
        
        plt.show()
        
        plt.title("Average Speed Main Channel -  " +BatchID)
        plt.xlabel("Volumn Flux [ml/min]")
        plt.ylabel("Speed   [mm/s]")
        
        plt.legend(loc=2, fontsize=6)
        
        if savepath != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"SpeedWFit_Graph_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
    def plotSpeedMainChannelAll(self, savepath=None, d0=None, BatchID  = '', BatchIDC ='', show=False, plotDaugtherChannel=False):
        self.findSpeedGradient()
        #get drag coefficients
        if d0 !=None:
            import track_capsule_TJ_v0p10 as tc
            lamb=d0/np.sqrt(4*7.8)
            k1, k2 = tc.getDragCoef(lamb)
            G=k2/k1
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
        
        size3p5=6
        plt.errorbar(self.volumFlux, self.SpeedMain/self.pixelsPmm,  linestyle='None',  marker='h', color = 'b', label='Speed Main Channel', markersize=size3p5) #
        if plotDaugtherChannel:
            plt.errorbar(self.volumFlux, self.SpeedDaugther/self.pixelsPmm,  linestyle='None',  marker='o', color = 'g', label='Speed Daugther Channel', markersize=size3p5) #
        
        sampleNum=len(self.SpeedMain)
        if d0 !=None:
            s2='Error based on standard deviation of sample \nNumber of data points = %d \nLag factor G = %.2f with $\lambda $ = %.2f and $d_0$ = %.2f $mm$' %(sampleNum, G, lamb, d0)
        else:
            s2='Error based on standard deviation of sample \nNumber of data points = %d' %sampleNum
            
        xmin, xmax = plt.xlim()
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()
        ymin, ymax = plt.ylim()
        ax2.text(xmin+xmax*0.02, ymin+ymax*0.8, s2, fontsize=10)
        #fit
        if d0 !=None:
            label='Predicted Speed Gradient = %.2f' %G
            plt.plot([xmin, xmax], [((2*G*xmin*1000.0/60)/32.0), ((2*G*xmax*1000.0/60)/32.0)], label=label, color='y', linestyle=':', linewidth=1)
            
        label1='Fit Main Channel, m=%.2f +/- %.2f and $R^2$ = %.2f' %(self.gradientSpeedMain, self.gradientSpeedMainErr,self.gradientSpeedMainR2)
        plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradientSpeedMain), self.straightLine(xmax, self.gradientSpeedMain)], label=label1, color='b', linestyle='-.', linewidth=1)
        
        if plotDaugtherChannel:
            label1='Fit Daugther Channel, m=%.2f +/- %.2f and $R^2$ = %.2f' %(self.gradientSpeedDaugther, self.gradientSpeedDaugtherErr,self.gradientSpeedDaugtherR2)
            plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradientSpeedDaugther), self.straightLine(xmax, self.gradientSpeedDaugther)], label=label1, color='g', linestyle='--', linewidth=1)

        plt.plot([xmin, xmax], [((2*xmin*1000.0/60)/32.0), ((2*xmax*1000.0/60)/32.0)], label='2 x Mean Speed', color='k', linestyle='--', linewidth=1)
        plt.plot([xmin, xmax], [((xmin*1000.0/60)/32.0), ((xmax*1000.0/60)/32.0)], label='Mean Speed', color='k', linestyle='-', linewidth=1)
        
        plt.show()
        
        plt.title("Average Speed Main Channel -  " +BatchID)
        plt.xlabel("Volumn Flux [ml/min]")
        plt.ylabel("Speed   [mm/s]")
        
        plt.legend(loc=2, fontsize=6)
        
        if savepath != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"SpeedWFitAll_Graph_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
        
            
    def plotOffset(self, savepath=None, BatchID  = '', BatchIDC ='', show=False):
        #=============================================================================
        #Offset in Main Channel
        
        c1, c2, c3, c4 =  self.coloursForMarker()
        #TODO: hshsh
        #volum flux
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        
        plt.plot(self.offCentre/self.pixelsPmm, self.volumFlux, linestyle='None', marker='o', color = c1, label='Turned right', markersize=5)
        plt.plot(self.offCentreTurnedRight/self.pixelsPmm, self.volumnFluxTurnedRight, linestyle='None', marker='s', color = c4, label='Turned left', markersize=5)

        ax2.set_xlabel("Offset in Main Channel [mm]")
        ax2.set_ylabel("Volumn Flux [ml/min]")
        
        locs, labels =plt.xticks()
        print(locs)
        ax3 = ax2.twiny()
        ax3.set_xlim(left=locs[0]*self.pixelsPmm, right=locs[-1]*self.pixelsPmm)
        ax3.set_xlabel('Offset in Main Channel [pixels]')
        
        xmin, xmax = plt.xlim()
#        plt.xlim([xmin, xmax*1.05])
#        xmin, xmax = plt.xlim()
        
        ymin, ymax = plt.ylim()
        plt.ylim([ymin, ymax*1.05])
        ymin, ymax = plt.ylim()       
        
        s='%d turned left and %d turned right \n pixels/mm = %.1f' %(len(self.offCentreTurnedRight), len(self.offCentre)-len(self.offCentreTurnedRight), self.pixelsPmm)
        ax2.text(0.3, 0.8, s, fontsize=12,    horizontalalignment='center',      verticalalignment='center',
             transform = ax2.transAxes)
        
        fig.tight_layout(); ax2.xaxis.grid(True, color='#D0D0D0'); ax2.yaxis.grid(True, color='#D0D0D0')
        
        plt.title("Offset in Main Channel -  " +BatchID, y=1.1)
        plt.plot([],[],'o',color=c1 ,)
        plt.plot([],[],'s',color=c4)
        plt.legend(['Turned right', 'Turned left'], loc=6, fontsize=6) 
        
        if savepath  != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"OffsetVSVolumFlux_Graph_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
    def plotDeformationInChannel(self, savepath=None, BatchID  = '',  show=False):
        ''' Plot the Taylor deformation parameter in the main and daugther channel versus volumn flux'''
        BatchIDC = BatchID.replace(' ' ,  '-').replace('/' ,  ''); c=  self.coloursForMarker()

        fig = plt.figure(figsize=(8, 6), dpi=200,); ax2 = fig.add_subplot(111)

        plt.plot(self.volumFlux, self.d12Main, linestyle='None', marker='o', color = c[0], label='Main Channel', markersize=3)
        plt.plot(self.volumFlux, self.d12Daugther, linestyle='None', marker='s', color = c[2], label='Daugther Channel', markersize=3)
        
        plt.errorbar(self.volumFluxesList, self.aveD12Main, yerr=self.aveD12MainSTD, linestyle='None', marker='o', color = c[1], label='Average Main Channel', markersize=7)
        plt.errorbar(self.volumFluxesList, self.aveD12Daugther, yerr=self.aveD12DaugtherSTD, linestyle='None', marker='s', color = c[3], label='Average Daugther Channel', markersize=7)

        ax2.set_xlabel("Volumn Flux [ml/min]"); ax2.set_ylabel("Taylor Deformation Parameter")
        
        xmin, xmax = plt.xlim(); plt.xlim([xmin, xmax*1.05]); xmin, xmax = plt.xlim()
        fig.tight_layout(); ax2.xaxis.grid(True, color='#D0D0D0'); ax2.yaxis.grid(True, color='#D0D0D0')
        plt.title("Deformation in  Channel -  " +BatchID, y=1.01); plt.legend(loc=2, fontsize=6) 
        
        if savepath  != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"DeformationVSVolumFlux_" +BatchIDC+".png"), dpi=300)
        if show: plt.show()
        else: plt.close()
   
    def plotOffsetVsTime(self, savepath=None, BatchID  = '', show=False):
        BatchIDC= BatchID.replace(' ', '_')

        XMIN = 100000
        XMAX = 0.0
        for c in self.offsetByVF:
            for l in c:
                print("%f" %l, end="")
                if l < XMIN:
                    XMIN = l
                elif l > XMAX:
                    XMAX = l        
            print("")
        print("")
        XMIN = XMIN / self.pixelsPmm; XMAX = XMAX / self.pixelsPmm;
        
        print('xmin = %f, xmax = %f' %(XMIN, XMAX))
        self.offsetByVF = np.array([np.array(xi) for xi in self.offsetByVF]) 
        self.timeInTJByVF = np.array([np.array(xi) for xi in self.timeInTJByVF]) 
        self.timeGeoInTJByVF = np.array([np.array(xi) for xi in self.timeGeoInTJByVF]) 
        print(np.shape(self.offsetByVF))
        
        c = self.coloursForMarker()
        counter = 0

        for vf in self.volumFluxesList:
            #volum flux
            fig = plt.figure(figsize=(8, 6), dpi=200,)
            ax2 = fig.add_subplot(111)
            
            plt.plot(self.offsetByVF[counter]/self.pixelsPmm, self.timeInTJByVF[counter], linestyle='None', marker='o', color = c[0], label='Acceleration Time', markersize=5)
            plt.plot(self.offsetByVF[counter]/self.pixelsPmm, self.timeGeoInTJByVF[counter], linestyle='None', marker='s', color = c[3], label='Geometric Time', markersize=5)
    #        plt.plot(self.offCentreTurnedRight/self.pixelsPmm, self.volumnFluxTurnedRight, linestyle='None', marker='s', color = c[3], label='Turned left', markersize=5)
    
            ax2.set_xlabel("Offset in Main Channel [mm]")
            ax2.set_ylabel("Time in T-Junction [s] for $Q = $ %.1f" %vf)
            
            plt.xlim([0.99* XMIN, 1.01*XMAX])
            ymin, ymax = plt.ylim()
            plt.ylim([ymin, ymax*1.05])
            ymin, ymax = plt.ylim()
            
            locs, labels =plt.xticks()
            print(locs)
            ax3 = ax2.twiny()
            ax3.set_xlim(left=locs[0]*self.pixelsPmm, right=locs[-1]*self.pixelsPmm)
            ax3.set_xlabel('Offset in Main Channel [pixels]')

            fig.tight_layout()
            ax2.xaxis.grid(True, color='#D0D0D0')
            ax2.yaxis.grid(True, color='#D0D0D0')
            
            plt.title("Offset vs Time - $Q = $ %.1f " %vf +BatchID, y=1.1)
            plt.plot([],[],'o',color=c[0] ,)
            plt.plot([],[],'s',color=c[3])
            plt.legend(['Acceleration Time', 'Geometric Time'], loc=6, fontsize=6) 
            plt.legend(loc='best')
            if savepath  != None:
                sp2 = savepath+self.makeSaveNameSafe(BatchIDC+ os.sep)
                if not os.path.exists(sp2): os.makedirs(sp2)
                name = "OffsetVSTime_Q=%.f_Graph_%s.png" %(vf, BatchIDC)
                plt.savefig(self.makeSaveNameSafe(sp2+ name), dpi=300)
            
            if show:
                plt.show()
            else:
                plt.close()
            counter +=1
            
    def findUncertaintyInTvs1oQ(self, savepath=None, BatchID  = '', BatchIDC ='', show=False):
        '''
        Ignore each data point in turn and find fit for T versus 1/Q
        '''
        m=[]
        merr=[]
        r2=[]
        count = [] 
        
        for ii in range(len(self.volumFlux)):
            iQ = np.delete(1/self.volumFlux, ii) 
            y = np.delete(self.timeInTJ, ii)
            
            tm, _, tmerr, _, tr2 = self.fitStraightLineScipy(iQ, y)
            m.append(tm)
            merr.append(tmerr)
            r2.append(tr2)
            count.append(ii)
        
        c =  self.coloursForMarker()
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        
        ax2.errorbar(count, m, yerr=merr, color=c[0], linestyle='None', marker='o')
        
        xmin, xmax = plt.xlim()
        ymin, ymax = plt.ylim()
        plt.xlim([xmin, xmax*1.05])
        plt.ylim([ymin*0.9, ymax])
        xmin, xmax = plt.xlim()
        
        ax2.set_xlabel("Ignored Data Point")
        ax2.set_ylabel("Gradient Time in T-Junction versus 1/Volumn Fluc")
        plt.title("Gradients Time vs 1/Q -  " +BatchID, y=1.01)
        
        fig.tight_layout()
        ax2.xaxis.grid(True, color='#D0D0D0')
        ax2.yaxis.grid(True, color='#D0D0D0')
        ax2.legend(loc=2, fontsize=6)
        
        ax_inset=fig.add_axes([0.65,0.21,0.25,0.25])
        fs_sp=8
        
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
        
        if savepath  != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"Gradient_Tvs1oQ_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
        
    
    
    def differenceGeoAndAccTime(self, savepath=None, BatchID  = '', show=False):
        if not hasattr(self, 'volumnFluxSOffset'):
            self.sortbyOffsetAroundCenter()

        self.gradient1oQ, self.gradient1oQRChi2, self.gradient1oQErr, self.gradient1oQPValue, self.gradient1oQR2 = self.fitStraightLineScipy(1.0/self.volumFlux, self.timeGeoInTJ)
        self.gradient1oQAcc, self.gradient1oQAccRChi2, self.gradient1oQAccErr, self.gradient1oQAccPValue, self.gradient1oQAccR2 = self.fitStraightLineScipy(1.0/self.volumFlux, self.timeInTJ)
        
        return self.gradient1oQ, self.gradient1oQErr, self.gradient1oQR2, self.gradient1oQAcc, self.gradient1oQAccErr, self.gradient1oQAccR2
        
    def plotTvs1oQ(self, savepath=None, BatchID  = '', BatchIDC ='', show=False, sortedTimes=False):
        '''
        Plot time in T-Junction versus 1/Flow rate
        '''
        
        if not hasattr(self, 'aveTimeinTJ'):
            self.find1oQGradientFromAverages()
        if not hasattr(self, 'gradient1oQ'):
            self.find1oQGradient()
            
        c =  self.coloursForMarker()
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        iQ = 1/self.volumFluxesList
        iQa = 1/self.volumFlux
        
#        plt.errorbar(iQa, self.timeInTJ, linestyle='None', marker='s', color = c4, label='Time in T-Junction', markersize=4)
        plt.errorbar(iQ, self.aveGeoTimeinTJ, yerr=self.aveGeoTimeinTJSTD, linestyle='None', marker='o', color = c[0], label='Average Time in T-Junction', markersize=5)
        
        xmin, xmax = plt.xlim()
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()
        
#        label1='Fit average Points, m=%.2f' %self.aveGradient1oQ
        label2='Fit, m=%.2f +/- %.2f with $R^2$ = %.2f' %(self.gradient1oQ, self.gradient1oQErr, self.gradient1oQR2)
        plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradient1oQ), self.straightLine(xmax, self.gradient1oQ)], label=label2, color=c[2], linestyle=':', linewidth=1)
        if len(self.volumnFluxSOffset) >0 :
            label2='Fit within 0.07mm of centre, m=%.2f +/- %.2f with $R^2$ = %.2f, (%d datapoints)' %(self.gradient1oQSOffset, self.gradient1oQSOffsetErr, self.gradient1oQSOffsetR2, len(self.gradient1oQSOffset))
            plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradient1oQSOffset), self.straightLine(xmax, self.gradient1oQSOffset)], label=label2, color=c[3], linestyle='-', linewidth=1)
            mSOffset = self.gradient1oQSOffset
        else:
            plt.plot([], [], label='No data point within 0.07mm of centerline', color=c[3], linestyle='-')
            mSOffset =-1

        ax2.set_xlabel("1/Volumn Flux [min/ml]")
        ax2.set_ylabel("Time in T-Junction [s]")
        plt.title("Time vs 1/Q -  " +BatchID, y=1.01)      
        
        list1, list2, list3 = (list(t) for t in zip(*sorted(zip(iQ, self.aveTimeinTJ, self.aveTimeinTJSTD))))
        
        m, _, merr, _, r2 = self.fitStraightLineScipy(list1[:-2], list2[:-2])
        self.gradient1oQm2, self.gradient1oQm2Err, self.gradient1oQm2R2 = m, merr, r2
 
        ax_inset=fig.add_axes([0.65,0.21,0.25,0.25])
        fs_sp=8
        ax_inset.errorbar(list1[:-2], list2[:-2], yerr=list3[:-2],color=c[0], linestyle='None', marker='o')
        ax_inset.plot([np.min(list1[:-2]), np.max(list1[:-2])], [self.straightLine(np.min(list1[:-2]), self.gradient1oQ), self.straightLine(np.max(list1[:-2]), self.gradient1oQ)],  color=c[2], linestyle=':', linewidth=1)
        labelSmall = 'Fit[:-2], $m_r$=%.2f +/- %.2f with $R^2$ = %.2f' %(m, merr, r2)
        ax_inset.plot([np.min(list1[:-2]), np.max(list1[:-2])], [self.straightLine(np.min(list1[:-2]), m), self.straightLine(np.max(list1[:-2]), m)], label=labelSmall, color=c[3], linestyle='-.', linewidth=1)
#        ax_inset.legend(fontsize=fs_sp)
#        ax_inset.set_xlim([xmin, xmax])
        ax_inset.tick_params(axis='x', labelsize=fs_sp-2)
        ax_inset.tick_params(axis='y', labelsize=fs_sp-2)
        ax_inset.set_xlabel("1/Volumn Flux [min/ml]", fontsize=fs_sp)
        ax_inset.set_ylabel("Time in T-Junction [s]", fontsize=fs_sp)
        ax_inset.legend(loc=2, fontsize=5)
        
        fig.tight_layout()
        ax2.xaxis.grid(True, color='#D0D0D0')
        ax2.yaxis.grid(True, color='#D0D0D0')
        ax2.legend(loc=2, fontsize=6)
        
        s='Difference in the gradient m - $m_r$ = %.2f \nNumber of Data points = %d \nErrorbars indicate one standard deviation. ' %(self.gradient1oQ - m, len(self.volumFlux) )
        ax2.text(0.1, 0.7, s, fontsize=10,    horizontalalignment='left',      verticalalignment='center',
             transform = ax2.transAxes)
        
#        plt.plot([],[],'o',color=c1 ,)
#        plt.plot([],[],'s',color=c4)
#        plt.legend(['Turned right', 'Turned left'], loc=6, fontsize=6) 
        
        if savepath  != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"Tvs1oQ_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return self.gradient1oQ, self.gradient1oQm2, mSOffset
            
    def plotMaxExtend(self, d0, savepath=None, BatchID  = '', BatchIDC ='', show=False):
        '''
        Plot maximum width and taylor parameter (d12) in T-Junction
        Do averages?
        '''
        c1, c2, c3, c4 =  self.coloursForMarker()
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)

        extension = (self.maxWidth/self.pixelsPmm)/d0
#        print('len(self.maxWidth) = %d, len(extension) = %d, len(self.volumFlux) = %d' %(len(self.maxWidth), len(extension), len(self.volumFlux)))
        ax2.plot(self.volumFlux, extension, linestyle='None', marker='o', color = c1,  markersize=5)#, label='Max Extension')
        ax2.set_xlabel("Volumn Flux [ml/min]")
        ax2.set_ylabel("Extension [$d_0$]")

        ax3 = ax2.twinx()
        ax3.plot(self.volumFlux, self.maxD12, linestyle='None', marker='s', color = c4, markersize=5)#, label='Max Taylor Parameter')
        ax3.set_ylabel("Taylor Deformation Paramter $D_{12}$")

        xmin, xmax = plt.xlim(); plt.xlim([xmin, xmax*1.05]); xmin, xmax = plt.xlim()
    
        ax2.xaxis.grid(True, color='#D0D0D0'); ax2.yaxis.grid(True, color='#D0D0D0')
        
        plt.title("Max Extension -  " +BatchID, y=1.01)
        plt.plot([],[],'o',color=c1); plt.plot([],[],'s',color=c4)
        plt.legend(['Max Extension', 'Max Taylor Parameter'], loc=6, fontsize=6) 
        
        plt.legend(loc=2, fontsize=6)
        fig.tight_layout()
        if savepath  != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"MaxExtension_" +BatchIDC+".png"), dpi=300)
        if show:
            plt.show()
        else:
            plt.close()
            
    def makeSaveNameSafe(self, sn):
        if self.texSaveNames:
            sn=sn.replace('_', '-')
            sn=sn.replace('#', 'nr')
        return sn
        
    def plotAverageMaxExtend(self, d0, savepath=None, BatchID  = '', BatchIDC ='', show=False):
        '''
        Plot maximum width and taylor parameter (d12) in T-Junction Averages
        '''
        c=  self.coloursForMarker()
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        print(self.aveMaxWidth)
        extension = (self.aveMaxWidth/self.pixelsPmm)/d0
        extensionSTD = (self.aveMaxWidthSTD/self.pixelsPmm)/d0
#        print('len(self.maxWidth) = %d, len(extension) = %d, len(self.volumFlux) = %d' %(len(self.maxWidth), len(extension), len(self.volumFlux)))
        ax2.errorbar(self.volumFluxesList, extension, yerr=extensionSTD,  linestyle='None', marker='o', color = c[0],  markersize=5)#, label='Max Extension')
        ax2.set_xlabel("Volumn Flux [ml/min]")
        ax2.set_ylabel("Extension [$d_0$]")
        ax2.spines['left'].set_color(c[0])
        ax2.yaxis.label.set_color(c[0])        
        ax2.tick_params(axis='y', colors=c[0])

        ax3 = ax2.twinx()
        ax3.errorbar(self.volumFluxesList, self.aveMaxD12, yerr=self.aveMaxD12STD, linestyle='None', marker='s', color = c[3], markersize=5)#, label='Max Taylor Parameter')
        ax3.set_ylabel("Taylor Deformation Paramter $D_{12}$")
        ax3.spines['right'].set_color(c[3])
        ax3.yaxis.label.set_color(c[3])        
        ax3.tick_params(axis='y', colors=c[3])

        xmin, xmax = plt.xlim()
#        ax2.set_xlim([xmin, xmax*1.05])
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()

        ax2.xaxis.grid(True, color='#D0D0D0')
        ax2.yaxis.grid(True, color='#D0D0D0')
        
        plt.title("Average Max Extension -  " +BatchID, y=1.01)
        plt.plot([],[],'o',color=c[0] ,)
        plt.plot([],[],'s',color=c[3])
        plt.legend(['Max Taylor Parameter', 'Max Extension'], loc=6, fontsize=6) 
        
        plt.legend(loc=2, fontsize=6)
        fig.tight_layout()
        if savepath  != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"AverageMaxExtension_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
    def plotRelaxationCapsule(self, savepath=None, BatchID  = '', BatchIDC ='', show=False):
        c=  self.coloursForMarker()
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        
        ax2.errorbar(self.volumFluxesList, self.aveRelaxationTime, yerr=self.aveRelaxationTimeSTD,  linestyle='None', marker='o', color = c[0],  markersize=5)#, label='Max Extension')
        ax2.set_xlabel("Volumn Flux [ml/min]")
        ax2.set_ylabel("Relaxation Time [s]")
        ax2.spines['left'].set_color(c[0])
        ax2.yaxis.label.set_color(c[0])        
        ax2.tick_params(axis='y', colors=c[0])

        ax3 = ax2.twinx()
        ax3.errorbar(self.volumFluxesList, self.aveRelaxationDistance/self.pixelsPmm, yerr=self.aveRelaxationDistanceSTD/self.pixelsPmm, linestyle='None', marker='s', color = c[3], markersize=5)#, label='Max Taylor Parameter')
#        ax3.plot(self.volumFlux, self.relaxationDistance/self.pixelsPmm, linestyle='None', marker='s', color = c[2], markersize=2)#, label='Max Taylor Parameter')
        ax3.set_ylabel("Relaxation Distance [mm]")
        ax3.spines['right'].set_color(c[3])
        ax3.yaxis.label.set_color(c[3])        
        ax3.tick_params(axis='y', colors=c[3])

        xmin, xmax = plt.xlim()
#        ax2.set_xlim([xmin, xmax*1.05])
        plt.xlim([0.9*xmin, xmax*1.05])
        xmin, xmax = plt.xlim()

        ax2.xaxis.grid(True, color='#D0D0D0')
        ax2.yaxis.grid(True, color='#D0D0D0')
        
        plt.title("Relaxation Time and Distance -  " +BatchID, y=1.01)
        plt.plot([],[],'o',color=c[0] ,)
        plt.plot([],[],'s',color=c[3])
        plt.legend([ 'Relaxation Distance', 'Relaxation Time'], loc='best', fontsize=6) 
        
#        plt.legend(loc='best', fontsize=6)
        fig.tight_layout()
        if savepath  != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"RelaxationTaD_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
    def plotRelaxationCapsuleLOG(self, savepath=None, BatchID  = '', BatchIDC ='', show=False):
        c=  self.coloursForMarker()
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        
        ax2.errorbar(self.volumFluxesList, self.aveRelaxationTime, yerr=self.aveRelaxationTimeSTD,  linestyle='None', marker='o', color = c[0],  markersize=5)#, label='Max Extension')
        ax2.set_xlabel("Volumn Flux [ml/min]")
        ax2.set_ylabel("Relaxation Time [s]")
        ax2.spines['left'].set_color(c[0])
        ax2.yaxis.label.set_color(c[0])        
        ax2.tick_params(axis='y', colors=c[0])
        plt.xscale('log')

        ax3 = ax2.twinx()
        ax3.errorbar(self.volumFluxesList, self.aveRelaxationDistance/self.pixelsPmm, yerr=self.aveRelaxationDistanceSTD/self.pixelsPmm, linestyle='None', marker='s', color = c[3], markersize=5)#, label='Max Taylor Parameter')
#        ax3.plot(self.volumFlux, self.relaxationDistance/self.pixelsPmm, linestyle='None', marker='s', color = c[2], markersize=2)#, label='Max Taylor Parameter')
        ax3.set_ylabel("Relaxation Distance [mm]")
        ax3.spines['right'].set_color(c[3])
        ax3.yaxis.label.set_color(c[3])        
        ax3.tick_params(axis='y', colors=c[3])

#        xmin, xmax = plt.xlim()
##        ax2.set_xlim([xmin, xmax*1.05])
#        plt.xlim([xmin, xmax*1.05])
#        xmin, xmax = plt.xlim()
        
        plt.xscale('log')

        ax2.xaxis.grid(True, color='#D0D0D0')
        ax2.yaxis.grid(True, color='#D0D0D0')
        
        plt.title("Relaxation Time and Distance -  " +BatchID, y=1.01)
        plt.plot([],[],'o',color=c[0] ,)
        plt.plot([],[],'s',color=c[3])
        plt.legend(['Relaxation Distance', 'Relaxation Time'], loc='best', fontsize=6) 
        
#        plt.legend(loc='best', fontsize=6)
        fig.tight_layout()
        if savepath  != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"RelaxationTaD_log_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()

    def plotAccelerationAsInertia(self, savepath=None, BatchID  = '', BatchIDC ='', show=False):
        assert(hasattr(self, 'maxAccerleration'))
        c=  self.coloursForMarker()
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        
        ax2.errorbar(self.volumFluxesList, self.aveMaxAccerleration/self.pixelsPmm, yerr=self.aveMaxAccerlerationSTD/self.pixelsPmm,  linestyle='None', marker='o', color = c[0],  markersize=5, label='Max Acceleration')
        ax2.errorbar(self.volumFluxesList, -self.aveMinAccerleration/self.pixelsPmm, yerr=self.aveMinAccerlerationSTD/self.pixelsPmm,  linestyle='None', marker='s', color = c[3],  markersize=5, label='- Min Extension')
        ax2.set_xlabel("Volumn Flux [ml/min]")
        ax2.set_ylabel("Acceleration [$mm/s^2$]")
#        ax2.spines['left'].set_color(c[0])
#        ax2.yaxis.label.set_color(c[0])        
#        ax2.tick_params(axis='y', colors=c[0])

        xmin, xmax = plt.xlim()
#        ax2.set_xlim([xmin, xmax*1.05])
        plt.xlim([0.9*xmin, xmax*1.05])
        xmin, xmax = plt.xlim()

        ax2.xaxis.grid(True, color='#D0D0D0')
        ax2.yaxis.grid(True, color='#D0D0D0')
        
        plt.title("Acceleration Max/Min -  " +BatchID, y=1.01)
        plt.legend(loc='best', fontsize=6) 
        
#        plt.legend(loc='best', fontsize=6)
        fig.tight_layout()
        if savepath  != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"MaxMinAcceleration_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()

    def plotOffsetVsMainSpeed(self, savepath=None, BatchID  = '', BatchIDC ='', show=False):
        """
        plot offset from centralline versus speed in main channel
        """
        c = self.coloursForMarker()
        if BatchID == '':
            BatchID = self.find_batchName(self.path)

        fig = plt.figure(figsize=(8, 6), dpi=200)
        
        ax = fig.add_subplot(111)
        
        
        ave=[]
        std=[]
        for ii in range(len(self.volumFluxesList)):
            meanSpeed = ((self.volumFluxesList[ii]*1000.0/60)/32.0)
            plt.plot(self.sortedOffset[ii]/self.pixelsPmm, (self.sortedSpeedMain[ii]/self.pixelsPmm)/meanSpeed, 's',color='r', markersize=7)
            ave.append((self.aveSpeedMain[ii]/self.pixelsPmm)/meanSpeed)
            std.append(np.std((self.sortedSpeedMain[ii]/self.pixelsPmm)/meanSpeed))
#            plt.plot([-0.4, -0.3], [ave[ii], ave[ii]])
            
        xmin, xmax = plt.xlim()
        
        aveSpeeds=np.average(np.array(ave))
        plt.plot([xmin, xmax], [aveSpeeds, aveSpeeds], label='Average Speed')
        
        ax.set_xlabel("Offset in Main Channel [mm]")
        ax.set_ylabel("Speed in Main Channel / Mean Speed")

        
#        step= ax.get_xaxis().get_data_interval()
#        print(step)
        locs, labels =plt. xticks()
#        print(locs)
        
        ax2 = ax.twiny()
#        ax2.plot(self.averageOffsetBinned, self.averageTimeBinned, 'ob')
        ax2.set_xlim(left=locs[0]*self.pixelsPmm,right=locs[-1]*self.pixelsPmm)
#        ax2.set_xticks(locs)
#        ax2.set_xticklabels((locs*self.pixelsPmm))
        ax2.set_xlabel('Offset in Main Channel [pixels]')
        
        plt.title("Offset vs Speed -  " +BatchID, y=1.1)
        plt.plot([],[],'o-',color='#253494' ,)
        plt.plot([],[],'s',color='#a1dab4')
#        plt.legend(['Averaged', 'Induvidual Runs'])        
        fig.tight_layout()
        ax.xaxis.grid(True, color='#D0D0D0')
        ax.yaxis.grid(True, color='#D0D0D0')
#        plt.grid(color='#D0D0D0', linestyle='--')
        if savepath != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"OffsetVsSpeed_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
        
#        plt.figure()
#        plt.errorbar(x=self.volumFluxesList, y=ave, yerr=std, marker = 's',color='b', markersize=5)
        
    def findNonDimensionalgradientSpeedChannel(self):
        ''' Fits non-dimenionalised gradients to the speed in main and daugther channel'''
        
        if self.pixelsPmm == -1 :
            raise NameError('pixelsPmm was not defined')
        
        if not hasattr(self, 'volumFluxesList'):
            self.averageSpeed()
            
        x=[]
        yM=[]
        yD=[]
        for ii in range(len(self.volumFluxesList)):
            for jj in range(len(self.sortedSpeedMain[ii])):
                x.append(self.volumFluxesList[ii])
                msM = ((self.volumFluxesList[ii]*1000.0/60)/32.0)
                msD = ((self.volumFluxesList[ii]*1000.0/60)/(2*16.0))
                yM.append(self.sortedSpeedMain[ii][jj]/(self.pixelsPmm*msM))
                yD.append(self.sortedSpeedDaugther[ii][jj]/(self.pixelsPmm*msD))
        
        self.NDAverageSpeedMain = np.mean(yM)
        self.NDAverageSpeedMainSTD = np.std(yM, ddof=1)
        self.NDAverageSpeedMainErr = np.std(yM, ddof=1)/np.sqrt(len(yM))
        self.NDAverageSpeedDaugther = np.mean(yD)
        self.NDAverageSpeedDaugtherSTD = np.std(yD, ddof=1)
        self.NDAverageSpeedDaugtherErr = np.std(yD, ddof=1)/np.sqrt(len(yD))
        
               
        
#        self.NDGradientSpeedMain, self.NDGradientSpeedMainRChi2, self.NDGradientSpeedMainErr, self.NDGradientSpeedMainPValue, self.NDGradientSpeedMainR2 = self.fitStraightLineScipy(x,yM)
#        self.NDGradientSpeedDaugther, self.NDGradientSpeedDaugtherRChi2, self.NDGradientSpeedDaugtherErr, self.NDGradientSpeedDaugtherPValue, self.NDGradientSpeedDaugtherR2 = self.fitStraightLineScipy(x,yD)
    

    def plotSpeedMainChannelNonDimensional(self, savepath=None, d0=None, BatchID  = '', BatchIDC ='', show=False, plotDaugtherChannel=False):
        if not hasattr(self, 'sortedSpeedMain'):
            self.averageSpeed()
        
        #get drag coefficients
        if d0 !=None:
            import track_capsule_TJ_v0p10 as tc
            lamb=d0/np.sqrt(4*7.8)
            k1, k2 = tc.getDragCoef(lamb)
            G=k2/k1
            lambD=d0/4.0
            if lambD > 0.95:
                lambTemp=0.95
            else:
                lambTemp=lambD
            k1D, k2D = tc.getDragCoef(lambTemp)
            GD=k2D/k1D
        
        c = self.coloursForMarker()
        
        size=6
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1self.sortedSpeedMain, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
        
        ms=[]
        for ii in range(len(self.volumFluxesList)):
            meanSpeed = ((self.volumFluxesList[ii]*1000.0/60)/32.0)
            ms.append(meanSpeed)
            xvalue = np.repeat(self.volumFluxesList[ii], len(self.sortedSpeedMain[ii]))
            plt.errorbar(x=xvalue, y=(self.sortedSpeedMain[ii]/self.pixelsPmm)/meanSpeed, marker = 'o', color = c[0], markersize=4,linestyle='None')
        ms=np.array(ms)
        plt.errorbar(x=self.volumFluxesList, y=(self.aveSpeedMain/self.pixelsPmm)/ms, yerr=(self.aveSpeedMainSTD/self.pixelsPmm)/ms, marker = 's', color = c[2], label='Mean Speed Main Channel',  markersize=size,linestyle='None') #
        self.meanSpeedMainND = np.mean((self.aveSpeedMain/self.pixelsPmm)/ms)
        self.meanSpeedMainNDSTD = np.std((self.aveSpeedMain/self.pixelsPmm)/ms, ddof=1)
        
        if plotDaugtherChannel:
            msD=[]
            for ii in range(len(self.volumFluxesList)):
                meanSpeed = ((self.volumFluxesList[ii]*1000.0/60)/(2*16.0))
                msD.append(meanSpeed)
                xvalue = np.repeat(self.volumFluxesList[ii], len(self.sortedSpeedDaugther[ii]))
                plt.errorbar(x=xvalue, y=(self.sortedSpeedDaugther[ii]/self.pixelsPmm)/meanSpeed, marker = '<', color = c[1], markersize=4,linestyle='None') #label='Speed Daugther Channel',
            msD=np.array(msD)
            plt.errorbar(x=self.volumFluxesList, y=(self.aveSpeedDaugther/self.pixelsPmm)/msD, yerr=(self.aveSpeedDaugtherSTD/self.pixelsPmm)/msD, marker = 'h', color = c[3],  label='Mean Speed Daugther Channel', markersize=size,linestyle='None')
            self.meanSpeedDaugtherND = np.mean((self.aveSpeedDaugther/self.pixelsPmm)/msD)
            self.meanSpeedDaugtherNDSTD = np.std((self.aveSpeedDaugther/self.pixelsPmm)/msD, ddof=1)
        sampleNum=len(self.SpeedMain)
        
        self.findNonDimensionalgradientSpeedChannel()
        if d0 !=None:
            self.mainChannelGradientDifferencToPredicted = (2.0*G) - self.NDAverageSpeedMain
            self.daugtherChannelGradientDifferencToPredicted = (2.0*GD) - self.NDAverageSpeedDaugther
            if lambTemp == lambD:
                s2='Error based on standard deviation of sample \nGradient difference to predicted main = %.2f, daugther = %.2f \nNumber of data points = %d \nLag factor G = %.2f with $\lambda $ = %.2f and $d_0$ = %.2f $mm$ \nLag factor G = %.2f with $\lambda $ = %.2f in Daugther' %(self.mainChannelGradientDifferencToPredicted, self.daugtherChannelGradientDifferencToPredicted, sampleNum, G, lamb, d0, GD, lambD)
            else:

                s2='Error based on standard deviation of sample \nGradient difference to predicted main = %.2f, daugther = %.2f \nNumber of data points = %d \nLag factor G = %.2f with $\lambda $ = %.2f and $d_0$ = %.2f $mm$ \nLag factor G = %.2f with for $\lambda $ = 0.95 (actually is $\lambda $ = %.2f) in Daugther' %(self.mainChannelGradientDifferencToPredicted, self.daugtherChannelGradientDifferencToPredicted, sampleNum, G, lamb, d0, GD, lambD)                
        else:
            s2='Error based on standard deviation of sample \nNumber of data points = %d' %sampleNum
        
        xmin, xmax = plt.xlim()
        plt.xlim([xmin - ((xmax-xmin)*0.05), xmax+((xmax-xmin)*0.05)])
        xmin, xmax = plt.xlim()
        ymin, ymax = plt.ylim()
        plt.ylim([ymin, ymax*1.05])
        ymin, ymax = plt.ylim()

        #fit
        if d0 !=None:
            
            labelm='Predicted Speed Main Gradient = %.2f' %(2.0*G)
            plt.plot([xmin, xmax], [2*G, 2*G], label=labelm, color='y', linestyle=':', linewidth=1)
            if plotDaugtherChannel:
                labeld='Predicted Speed Daugther Gradient = %.2f' %(2.0*GD)
                plt.plot([xmin, xmax], [2*GD, 2*GD], label=labeld, color='m', linestyle=':', linewidth=1)
#                print('%s \n%s' %(labelm, labeld))
                
        
        label1='Mean Main Channel, m=%.2f +/- %.2f' %(self.NDAverageSpeedMain, self.NDAverageSpeedMainErr)
        plt.plot([xmin, xmax], [self.NDAverageSpeedMain, self.NDAverageSpeedMain], label=label1, color='b', linestyle='-.', linewidth=1)
        
        if plotDaugtherChannel:
            label1='Mean Daugther Channel, m=%.2f +/- %.2f ' %(self.NDAverageSpeedDaugther, self.NDAverageSpeedDaugtherErr)
            plt.plot([xmin, xmax], [self.NDAverageSpeedDaugther, self.NDAverageSpeedDaugther], label=label1, color='g', linestyle='--', linewidth=1)
        
        plt.show()
        
        ymin, ymax = plt.ylim()
        ax2.text(xmin+xmax*0.3, ymin+ymax*0.01, s2, fontsize=10)
        plt.show()
        
        plt.title("Speed Nondimensional -  " +BatchID)
        plt.xlabel("Volumn Flux [ml/min]")
        plt.ylabel("Speed as fraction of Mean Speed")
        
        plt.legend(loc='upper left', fontsize=6, ncol=2)
        
        if savepath != None:
            plt.savefig(self.makeSaveNameSafe(savepath+"Speed_ND_Graph_" +BatchIDC+".png"), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
    def mad(arr):
        """ Median/Man Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation 
        From: http://stackoverflow.com/questions/8930370/where-can-i-find-mad-mean-absolute-deviation-in-scipy
        """
        arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
        med = np.meann(arr)
        return np.median(np.abs(arr - med))


    def coloursForMarker(self, n=4):
        '''
        Returns 4 colours that will be dinstingusiable in greyscale
        Frome: http://colorbrewer2.org/
        '''
#        c1= '#ca0020'
#        c2= '#f4a582'
#        c3= '#92c5de'
#        c4= '#0571b0'
        if n <=4:
#            c1= '#253494'
#            c2= '#2c7fb8'
#            c3= '#41b6c4'
#            c4= '#a1dab4'
            c1= '#d7191c'
            c2= '#fdae61'
            c3= '#abd9e9'
            c4= '#2c7bb6'
            return [c1, c2, c3, c4]
#        c4= '#ffffb2'
#        c3= '#fecc5c'
#        c2= '#fd8d3c'
#        c1= '#e31a1c'
        
        elif n > 4 and n <= 6:
#            c1= '#ffffcc'
#            c2= '#c7e9b4'
#            c3= '#7fcdbb'
#            c4= '#41b6c4'
#            c5= '#2c7fb8'
#            c6= '#253494'
            c1= '#d73027'
            c2= '#fc8d59'
            c3= '#fee090'
            c4= '#e0f3f8'
            c5= '#91bfdb'
            c6= '#4575b4'
            return [c1, c2, c3, c4, c5, c6]
        
        elif n > 6 and n <=8:
            c1= '#b2182b'
            c2= '#d6604d'
            c3= '#f4a582'
            c4= '#fddbc7'
            c5= '#d1e5f0'
            c6= '#92c5de'
            c7= '#4393c3'
            c8= '#2166ac'
            return [c1, c2, c3, c4, c5, c6, c7, c8]
        
        elif n>8 and n<=10:
            c1= '#a50026'
            c2= '#d73027'
            c3= '#f46d43'
            c4= '#fdae61'
            c5= '#fee090'
            c6= '#e0f3f8'
            c7= '#abd9e9'
            c8= '#74add1'
            c9= '#4575b4'
            c10= '#313695'
            return [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

       
        
    
    def calcAll(self):
        self.findSpeedGradientFromAverages()
        self.findSpeedGradient()
        self.turnedDirection()
        self.find1oQGradientFromAverages()
        self.find1oQGradient()
        self.findDeformationGradient()
        
    
#rsltRigid3p5mm=ResultsClass('M:\\EdgarHaener\\Capsules\\RigidParticle-3.5mm\\31032015\\RigidParticle-3.5mm-31032015_Results.txt')
#print(rsltRigid3p5mm.volumFlux)
#rsltRigid3p5mm.printData()
