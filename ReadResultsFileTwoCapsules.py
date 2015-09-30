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
from scipy.optimize import curve_fit
from scipy.stats import chisqprob



class ResultsClassTwoCapsules:
    """A class to hold and read results from T-Junction experiments"""
    
    def __init__(self, path1):
        self.path = path1
        self.volumFlux =[]
        self.name = []
        self.distanceMain = [] 
        self.distanceDaugther = []
        self.speedMain1 = [] 
        self.speedDaugther1 = []
        self.offCentre1 = []
        self.turned1 = []
        self.maxWidth1 = []
        self.maxD121 = []
        self.speedMain2 = [] 
        self.speedDaugther2 = []
        self.offCentre2 = []
        self.turned2 = []
        self.maxWidth2 = []
        self.maxD122 = []
        self.pixelsPmm=-1
        
        #read in the data
        self.readData()
            
    def printData(self):
        print('Vol Flux \tname , \tave speed 1, \tave speed 2,  \tOff-centre, \tturned')
        for i in range(len(self.volumFlux)):
            print('%.2f \t%s \t%.2f  \t%.2f \t%.2f \t%.2f \t%.2f \t%s' %(self.volumFlux[i], self.name[i], self.SpeedMain[i], self.SpeedDaugther[i], self.timeInTJ[i], self.offCentre[i], self.turned[i] ))
            

        
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
#Vol Flux 	name 	distance Main 	 distance Daugther 		 
#Capsule 1: Speed Main 	 Speed Daugther 	 Off-centre 	 turned 	 max width 	 max d12 		 
            if len(entries)>=16:
                self.volumFlux.append(float(entries[0]))
                self.name.append(entries[1])
                self.distanceMain.append(float(entries[2]))
                self.distanceDaugther.append(float(entries[3]))
                
                self.speedMain1.append(float(entries[4]) )
                self.speedDaugther1.append(float(entries[5]))
                self.offCentre1.append(float(entries[6]))
                self.turned1.append(entries[7])  
                self.maxWidth1.append(float(entries[8]) )
                self.maxD121.append(float(entries[9]) )
                
                self.speedMain2.append(float(entries[10]) )
                self.speedDaugther2.append(float(entries[11]))
                self.offCentre2.append(float(entries[12]))
                self.turned2.append(entries[13])  
                self.maxWidth2.append(float(entries[14])) 
                self.maxD122.append(float(entries[15]))
            indexC=indexC+1        
            
        self.volumFlux=np.array(self.volumFlux)
        self.distanceMain = np.array(self.distanceMain)
        self.distanceDaugther = np.array(self.distanceDaugther)
        
        self.speedMain1=np.array(self.speedMain1)
        self.speedDaugther1=np.array(self.speedDaugther1)
        self.offCentre1=np.array(self.offCentre1)
        self.maxWidth1 = np.array(self.maxWidth1) 
        self.maxD121 = np.array(self.maxD121)
        
        self.speedMain2=np.array(self.speedMain2)
        self.speedDaugther2=np.array(self.speedDaugther2)
        self.offCentre2=np.array(self.offCentre2)
        self.maxWidth2 = np.array(self.maxWidth2) 
        self.maxD122 = np.array(self.maxD122)


    def _sortByVolumnFlux(self, volumFlux, sm, sd, mw, md12, oc ):
        vfl=[]
        for VF in volumFlux:
            isInList=False
            for x in volumFlux:
                if VF == x:
                    isInList=True
            if not isInList:
                vfl.append(VF)
                
        lenvfl= len(vfl)
        aveSpeedMain=np.zeros((lenvfl,1))
        aveSpeedMainSTD=np.zeros((lenvfl, 1))
        aveSpeedDaugther=np.zeros((lenvfl, 1))
        aveSpeedDaugtherSTD=np.zeros((lenvfl, 1))
        
        aveMaxWidth=np.zeros((lenvfl))
        aveMaxWidthSTD=np.zeros((lenvfl))
        aveMaxD12=np.zeros((lenvfl))
        aveMaxD12STD=np.zeros((lenvfl))
        
        tempsortedSpeeds=[]
        tempsortedSpeedDs=[]
        tempsortedOffsets=[]
        
        counter=0
        for x in vfl:
            tempMain=[]
            tempDaugther=[]
            tempMaxWidth=[]
            tempMaxD12 = []
            tempsortedSpeed = [] 
            tempsortedSpeedD = [] 
            tempsortedOffset = [] 
#            print('Counter =%d' %counter)
            for i in range(len(volumFlux)):
                if volumFlux[i] == x:
#                    print('Volumn Flux = %.2f' %vfl)
                    tempMain.append(sm[i])
                    tempDaugther.append(sd[i])
                    tempMaxWidth.append(mw[i])
                    tempMaxD12.append(md12[i])
                    tempsortedSpeed.append(sm[i])
                    tempsortedSpeedD.append(sd[i])
                    tempsortedOffset.append(oc[i])
                    
#            print('len = %d' %len(aveSpeedMain))
            tempsortedSpeeds.append(np.array(tempsortedSpeed))
            tempsortedSpeedDs.append(np.array(tempsortedSpeedD))
            tempsortedOffsets.append(np.array(tempsortedOffset))
            
            aveSpeedMain[counter]=np.average(tempMain)
            aveSpeedMainSTD[counter]=np.std(tempMain)
            aveSpeedDaugther[counter]=np.average(tempDaugther)
            aveSpeedDaugtherSTD[counter]=np.std(tempDaugther)
            
            aveMaxWidth[counter]=np.average(tempMaxWidth)
            aveMaxWidthSTD[counter]=np.std(tempMaxWidth)
            aveMaxD12[counter]=np.average(tempMaxD12)
            aveMaxD12STD[counter]=np.std(tempMaxD12)

            #flatten the arryas
            aveSpeedMain=aveSpeedMain.flatten()
            aveSpeedDaugther=aveSpeedDaugther.flatten()     
            
            aveSpeedMainSTD=aveSpeedMainSTD.flatten()
            aveSpeedDaugtherSTD=aveSpeedDaugtherSTD.flatten()
            counter+=1
        
        volumFluxesList=np.array(vfl)
                
        sortedSpeedMain = np.array(tempsortedSpeeds)
        sortedSpeedDaugther = np.array(tempsortedSpeedDs)
        sortedOffset = np.array(tempsortedOffsets)
        
        return volumFluxesList, aveSpeedMain, aveSpeedMainSTD, aveSpeedDaugther, aveSpeedDaugtherSTD, aveMaxWidth, aveMaxWidthSTD, aveMaxD12, aveMaxD12STD
        
    def averageSpeed(self):
        self.volumFluxesList, self.aveSpeedMain1, self.aveSpeedMainSTD1, self.aveSpeedDaugther1, \
            self.aveSpeedDaugtherSTD1, self.aveMaxWidth1, self.aveMaxWidthSTD1, self.aveMaxD121, self.aveMaxD12STD1 \
            = self._sortByVolumnFlux(self.volumFlux, self.speedMain1, self.speedDaugther1, self.maxWidth1, self.maxD121, self.offCentre1 )
        self.volumFluxesList, self.aveSpeedMain2, self.aveSpeedMainSTD2, self.aveSpeedDaugther2, \
            self.aveSpeedDaugtherSTD2, self.aveMaxWidth2, self.aveMaxWidthSTD2, self.aveMaxD122, self.aveMaxD12STD2 \
            = self._sortByVolumnFlux(self.volumFlux, self.speedMain2, self.speedDaugther2, self.maxWidth2, self.maxD122, self.offCentre2 )
        
        
        
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
        '''
        Fit straight line to data with zero intercept
        '''
        
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
        self.averageSpeed()
        self.gradientSpeedMain1, self.gradientSpeedMainRChi21, self.gradientSpeedMainErr1, self.gradientSpeedMainPValue1, self.gradientSpeedMainR21 = self.fitStraightLineScipy(self.volumFlux, self.speedMain1/self.pixelsPmm)
        self.gradientSpeedDaugther1, self.gradientSpeedDaugtherRChi21, self.gradientSpeedDaugtherErr1, self.gradientSpeedDaugtherPValue1, self.gradientSpeedDaugtherR21 = self.fitStraightLineScipy(self.volumFlux, self.speedDaugther1/self.pixelsPmm)
        self.gradientSpeedMain2, self.gradientSpeedMainRChi22, self.gradientSpeedMainErr2, self.gradientSpeedMainPValue2, self.gradientSpeedMainR22 = self.fitStraightLineScipy(self.volumFlux, self.speedMain2/self.pixelsPmm)
        self.gradientSpeedDaugther2, self.gradientSpeedDaugtherRChi22, self.gradientSpeedDaugtherErr2, self.gradientSpeedDaugtherPValue2, self.gradientSpeedDaugtherR22 = self.fitStraightLineScipy(self.volumFlux, self.speedDaugther2/self.pixelsPmm)

#        return self.gradientSpeedMain, self.gradientSpeedMainRChi2, self.gradientSpeedMainErr, self.gradientSpeedDaugther, self.gradientSpeedDaugtherRChi2, self.gradientSpeedDaugtherErr
    

    def printSpeedGradient(self):
        self.findSpeedGradient()
        print('Gradient Main Channel %.2f p/m %0.3f \t  Gradient Daugther Channel %.2f p/m %0.3f ' %(self.gradientSpeedMain, self.gradientSpeedMainSTD, self.gradientSpeedDaugther, self.gradientSpeedDaugtherSTD)),

    def _turnedDirection(self, turned,vf, oc):
        turnedDirection= np.zeros((len(turned),1), dtype=int)
        volumnFluxTurnedRight=[]
        offCentreTurnedRight=[]
        for ll in range(len(turned)):
            if turned[ll] == 'right':
                turnedDirection[ll]=0
                volumnFluxTurnedRight.append(vf[ll])
                offCentreTurnedRight.append(oc[ll])
            elif turned[ll] == 'left':
                turnedDirection[ll]=1
            else:
                turnedDirection[ll]=-1
                
        volumnFluxTurnedRight=np.array(volumnFluxTurnedRight)
        offCentreTurnedRight=np.array(offCentreTurnedRight)
        return turnedDirection, volumnFluxTurnedRight, offCentreTurnedRight
        
    def turnedDirection(self):
        self.turnedDirection1, self.volumnFluxTurnedRight1, self.offCentreTurnedRight1 = \
            self._turnedDirection(self.turned1, self.volumFlux, self.offCentre1)
            
        self.turnedDirection2, self.volumnFluxTurnedRight2, self.offCentreTurnedRight2 = \
            self._turnedDirection(self.turned2, self.volumFlux, self.offCentre2)
        
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
    
    def straightLine(self,x, A): 
        '''
        Returns a straight line y=f(x)
        Input
        x       x-value
        A       gradient
        '''
        return A*x
    def _averageOffCentre(self):
        aveOffCentre=[]
        for ii in range(len(self.offCentre1)):
            if self.offCentre1[ii] != -1 and self.offCentre2[ii] != -1:
                aveOffCentre.append((self.offCentre1[ii]+self.offCentre2[ii])/2)
            else:
                aveOffCentre.append(-1)
        self.aveOffCentre = np.array(aveOffCentre)
        
    def _findNotEqualTurned(self):
        self._averageOffCentre()
        
        turnedDirection= np.zeros((len(self.turned1),2), dtype=int)
        distanceMTurnedOpposite=[]
        offCentreTurnedOpposite=[]
        for ll in range(len(self.turned1)):
            if self.turned1[ll] == 'right':
                turnedDirection[ll,0]=0
            else:
                turnedDirection[ll,0]=1
            
            if self.turned2[ll] == 'right':
                turnedDirection[ll,1]=0
            else:
                turnedDirection[ll,1]=1
                
            if self.turned1[ll] != self.turned2[ll]:
                distanceMTurnedOpposite.append(self.distanceMain[ll])
                offCentreTurnedOpposite.append(self.aveOffCentre[ll])
                
        self.distanceMTurnedOpposite=np.array(distanceMTurnedOpposite)
        self.offCentreTurnedOpposite=np.array(offCentreTurnedOpposite)

        
    def plotDistanceAndTurn(self, savepath=None, BatchID  = '', show=False ):
        c1, c2, c3, c4 =  self.coloursForMarker()
            
    def plotSpeedMainChannel(self, savepath=None, d0=None, BatchID  = '', BatchIDC ='', show=False, plotDaugtherChannel=False):
        self.findSpeedGradient()
        c1, c2, c3, c4 =  self.coloursForMarker()
        
        #get drag coefficients
        if d0 !=None:
            import track_capsule_TJ_v0p10 as tc
            lamb1=d0[0]/np.sqrt(4*7.8)
            k11, k21 = tc.getDragCoef(lamb1)
            G1=k21/k11
            lamb2=d0[1]/np.sqrt(4*7.8)
            k12, k22 = tc.getDragCoef(lamb2)
            G2=k22/k12
            if plotDaugtherChannel:
                templambda1=d0[0]/4.0
                if templambda1 > 0.95:
                    print('lambda daugther too big, set to 0.95')
                    templambda1=0.95
                lambD1=templambda1
                k1D1, k2D1 = tc.getDragCoef(lambD1)
                GD1=(k2D1/k1D1)
                templambda2=d0[1]/4.0
                if templambda2 > 0.95:
                    print('lambda daugther too big, set to 0.95')
                    templambda2=0.95
                lambD2=templambda2
                k1D2, k2D2 = tc.getDragCoef(lambD2)
                GD2=(k2D2/k1D2)

        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
        
        size3p5=6
        #errorbar average3p5beforSTD
        plt.errorbar(self.volumFluxesList, self.aveSpeedMain1/self.pixelsPmm, yerr=self.aveSpeedMainSTD1/self.pixelsPmm, linestyle='None',  marker='h', color = c1, label='Speed Main Channel Capsule 1', markersize=size3p5) #
        plt.errorbar(self.volumFluxesList, self.aveSpeedMain2/self.pixelsPmm, yerr=self.aveSpeedMainSTD2/self.pixelsPmm, linestyle='None',  marker='p', color = c3, label='Speed Main Channel Capsule 2', markersize=size3p5) #
        if plotDaugtherChannel:
#            plt.errorbar(self.volumFlux, self.SpeedDaugther/self.pixelsPmm,  linestyle='None',  marker='s', color = 'g', label='Speed Daugther Channel', markersize=3) #
            plt.errorbar(self.volumFluxesList, self.aveSpeedDaugther1/self.pixelsPmm, yerr=self.aveSpeedDaugtherSTD1/self.pixelsPmm,  linestyle='None',  marker='o', color = c2, label='Speed Daugther Channel Capsule 1', markersize=size3p5) #
            plt.errorbar(self.volumFluxesList, self.aveSpeedDaugther2/self.pixelsPmm, yerr=self.aveSpeedDaugtherSTD2/self.pixelsPmm,  linestyle='None',  marker='s', color = c3, label='Speed Daugther Channel Capsule 2', markersize=size3p5) #
        sampleNum1=len(self.speedMain1)
        if d0 !=None:
            if plotDaugtherChannel:
                s2 = 'Error based on standard deviation of sample \nNumber of data points = %d \nLag factor G = %.2f / %.2f with $\lambda $ = %.2f / %.2f and $d_0$ = %.2f /%.2f $mm$ \nLag factor Daugther G = %.2f /%.2f with $\lambda $ = %.2f / %.2f' %(sampleNum1, G1, G2, lamb1, lamb2, d0[0], d0[1], GD1, GD2, lambD1, lambD2)
            else:
                s2='Error based on standard deviation of sample \nNumber of data points = %d \nLag factor G = %.2f / %.2f with $\lambda $ = %.2f / %.2f and $d_0$ = %.2f $mm$' %(sampleNum1, G1, G2, lamb1, lamb2, d0[0], d0[1])
        else:
            s2='Error based on standard deviation of sample \nNumber of data points = %d' %sampleNum
            
        xmin, xmax = plt.xlim()
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()
        ymin, ymax = plt.ylim()
        ax2.text(xmin+xmax*0.02, ymin+ymax*0.7, s2, fontsize=10)
        #fit
        if d0 !=None:
            label='Predicted Speed Gradient Main 1 = %.2f' %G1
            plt.plot([xmin, xmax], [((2*G1*xmin*1000.0/60)/32.0), ((2*G1*xmax*1000.0/60)/32.0)], label=label, color=c1, linestyle=':', linewidth=1)
            label='Predicted Speed Gradient Main 2 = %.2f' %G2            
            plt.plot([xmin, xmax], [((2*G2*xmin*1000.0/60)/32.0), ((2*G2*xmax*1000.0/60)/32.0)], label=label, color=c3, linestyle=':', linewidth=1)
            
        label1='Fit Main Channel 1, m=%.2f +/- %.2f and $R^2$ = %.2f' %(self.gradientSpeedMain1, self.gradientSpeedMainErr1,self.gradientSpeedMainR21)
        plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradientSpeedMain1), self.straightLine(xmax, self.gradientSpeedMain1)], label=label1, color=c1, linestyle='-.', linewidth=1)
        label1='Fit Main Channel 2, m=%.2f +/- %.2f and $R^2$ = %.2f' %(self.gradientSpeedMain2, self.gradientSpeedMainErr2,self.gradientSpeedMainR22)
        plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradientSpeedMain2), self.straightLine(xmax, self.gradientSpeedMain2)], label=label1, color=c3, linestyle='-.', linewidth=1)
             
        if plotDaugtherChannel:
            label1='Fit Daugther Channel 1, m=%.2f +/- %.2f and $R^2$ = %.2f' %(self.gradientSpeedDaugther1, self.gradientSpeedDaugtherErr1,self.gradientSpeedDaugtherR21)
            plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradientSpeedDaugther1), self.straightLine(xmax, self.gradientSpeedDaugther1)], label=label1, color=c2, linestyle='--', linewidth=1)
            label1='Fit Daugther Channel 2, m=%.2f +/- %.2f and $R^2$ = %.2f' %(self.gradientSpeedDaugther2, self.gradientSpeedDaugtherErr2,self.gradientSpeedDaugtherR22)
            plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradientSpeedDaugther2), self.straightLine(xmax, self.gradientSpeedDaugther2)], label=label1, color=c4, linestyle='--', linewidth=1)
            if d0 !=None:
                label='Predicted Speed Gradient Daugther 1= %.2f' %GD1
                plt.plot([xmin, xmax], [((2*GD1*xmin*1000.0/60)/32.0), ((2*GD1*xmax*1000.0/60)/32.0)], label=label, color=c2, linestyle=':', linewidth=1)
                label='Predicted Speed Gradient Daugther 2= %.2f' %GD2
                plt.plot([xmin, xmax], [((2*GD2*xmin*1000.0/60)/32.0), ((2*GD2*xmax*1000.0/60)/32.0)], label=label, color=c4, linestyle=':', linewidth=1)
        
        plt.plot([xmin, xmax], [((2*xmin*1000.0/60)/32.0), ((2*xmax*1000.0/60)/32.0)], label='2 x Mean Speed', color='k', linestyle='--', linewidth=1)
        plt.plot([xmin, xmax], [((xmin*1000.0/60)/32.0), ((xmax*1000.0/60)/32.0)], label='Mean Speed', color='k', linestyle='-', linewidth=1)
        
        plt.show()
        
        plt.title("Average Speed Main Channel -  " +BatchID)
        plt.xlabel("Volumn Flux [ml/min]")
        plt.ylabel("Speed   [mm/s]")
        
        plt.legend(loc=2, fontsize=6)
        
        if savepath != None:
            plt.savefig(savepath+"SpeedWFit_Graph_" +BatchIDC+".png", dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
             
 
            
    def plotOffset(self, savepath=None, BatchID  = '', BatchIDC ='', show=False):
        #=============================================================================
        #Offset in Main Channel
        
        c1, c2, c3, c4 =  self.coloursForMarker()
        
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
        
        fig.tight_layout()
        ax2.xaxis.grid(True, color='#D0D0D0')
        ax2.yaxis.grid(True, color='#D0D0D0')
        
        plt.title("Offset in Main Channel -  " +BatchID, y=1.1)
        plt.plot([],[],'o',color=c1 ,)
        plt.plot([],[],'s',color=c4)
        plt.legend(['Turned right', 'Turned left'], loc=6, fontsize=6) 
        
        if savepath  != None:
            plt.savefig(savepath+"OffsetVSVolumFlux_Graph_" +BatchIDC+".png", dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()

            
    def plotMaxExtend(self, d0, savepath=None, BatchID  = '', show=False):
        '''
        Plot maximum width and taylor parameter (d12) in T-Junction
        Do averages?
        '''
        c1, c2, c3, c4 =  self.coloursForMarker()
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        print(self.maxWidth1)
        extension1 = (self.maxWidth1/self.pixelsPmm)/d0[0]
        extension2 = (self.maxWidth2/self.pixelsPmm)/d0[0]
#        print('len(self.maxWidth) = %d, len(extension) = %d, len(self.volumFlux) = %d' %(len(self.maxWidth), len(extension), len(self.volumFlux)))
#        ax2.plot(self.volumFlux, extension1, linestyle='None', marker='o', color = c1,  markersize=5)#, label='Max Extension')
#        ax2.plot(self.volumFlux, extension2, linestyle='None', marker='<', color = c3,  markersize=5)#, label='Max Extension')
        ax2.plot(np.arange(len(extension1)), extension1, linestyle='None', marker='o', color = c1,  markersize=5)#, label='Max Extension')
        ax2.plot(np.arange(len(extension1)), extension2, linestyle='None', marker='<', color = c3,  markersize=5)#, label='Max Extension')
        ax2.set_xlabel("Run")
        ax2.set_ylabel("Extension [$d_0$]")
        

        
        ax3 = ax2.twinx()
#        ax3.plot(self.volumFlux, self.maxD121, linestyle='None', marker='s', color = c2, markersize=5)#, label='Max Taylor Parameter')
#        ax3.plot(self.volumFlux, self.maxD122, linestyle='None', marker='>', color = c4, markersize=5)#, label='Max Taylor Parameter')
        ax3.plot(np.arange(len(extension1)), self.maxD121, linestyle='None', marker='s', color = c2, markersize=5)#, label='Max Taylor Parameter')
        ax3.plot(np.arange(len(extension1)), self.maxD122, linestyle='None', marker='>', color = c4, markersize=5)#, label='Max Taylor Parameter')
        ax3.set_ylabel("Taylor Deformation Paramter $D_{12}$")
        
#        label1='Fit, m=%.2f' %self.gradient1oQ
#        plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradient1oQ), self.straightLine(xmax, self.gradient1oQ)], label=label1, color=c1, linestyle='-.', linewidth=1)
   
        
#        s='%d turned left and %d turned right \n pixels/mm = %.1f' %(len(self.offCentreTurnedRight), len(self.offCentre)-len(self.offCentreTurnedRight), self.pixelsPmm)
#        ax2.text(0.3, 0.8, s, fontsize=12,    horizontalalignment='center',      verticalalignment='center',
#             transform = ax2.transAxes)
        
        xmin, xmax = plt.xlim()
#        ax2.set_xlim([xmin, xmax*1.05])
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()
        
        
        ax2.xaxis.grid(True, color='#D0D0D0')
        ax2.yaxis.grid(True, color='#D0D0D0')
        
        plt.title("Max Extension -  " +BatchID, y=1.01)
        plt.plot([],[],'o',color=c1 ,)
        plt.plot([],[],'<',color=c3)
        plt.plot([],[],'s',color=c2 ,)
        plt.plot([],[],'>',color=c4)
        plt.legend(['Max Extension 1','Max Extension 2', 'Max Taylor Parameter 1', 'Max Taylor Parameter 2'], loc='best', fontsize=6) 
        
        plt.legend(loc=2, fontsize=6)
        fig.tight_layout()
        if savepath  != None:
            plt.savefig(savepath+"MaxExtension_" +BatchID.replace(' ', '_').replace('/', '') +".png", dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
    def plotMaxExtendVSOffSet(self, d0, savepath=None, BatchID  = '', show=False):
        '''
        Plot maximum width and taylor parameter (d12) in T-Junction
        Do averages?
        '''
        c1, c2, c3, c4 =  self.coloursForMarker()
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        print(self.maxWidth1)
        extension1 = (self.maxWidth1/self.pixelsPmm)/d0[0]
        extension2 = (self.maxWidth2/self.pixelsPmm)/d0[0]
        ax2.plot(self.offCentre1, extension1, linestyle='None', marker='o', color = c1,  markersize=5)#, label='Max Extension')
        ax2.plot(self.offCentre2, extension2, linestyle='None', marker='<', color = c3,  markersize=5)#, label='Max Extension')
        ax2.set_xlabel("Offset in Main Channel [mm]")
        ax2.set_ylabel("Maximal Extension [$d_0$]")
        

        
        ax3 = ax2.twinx()
#        ax3.plot(self.volumFlux, self.maxD121, linestyle='None', marker='s', color = c2, markersize=5)#, label='Max Taylor Parameter')
#        ax3.plot(self.volumFlux, self.maxD122, linestyle='None', marker='>', color = c4, markersize=5)#, label='Max Taylor Parameter')
        ax3.plot(self.offCentre1, self.maxD121, linestyle='None', marker='s', color = c2, markersize=5)#, label='Max Taylor Parameter')
        ax3.plot(self.offCentre2, self.maxD122, linestyle='None', marker='>', color = c4, markersize=5)#, label='Max Taylor Parameter')
        ax3.set_ylabel("Max Taylor Deformation Paramter $D_{12}$")
        
#        label1='Fit, m=%.2f' %self.gradient1oQ
#        plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradient1oQ), self.straightLine(xmax, self.gradient1oQ)], label=label1, color=c1, linestyle='-.', linewidth=1)
   
        
#        s='%d turned left and %d turned right \n pixels/mm = %.1f' %(len(self.offCentreTurnedRight), len(self.offCentre)-len(self.offCentreTurnedRight), self.pixelsPmm)
#        ax2.text(0.3, 0.8, s, fontsize=12,    horizontalalignment='center',      verticalalignment='center',
#             transform = ax2.transAxes)
        
        xmin, xmax = plt.xlim()
#        ax2.set_xlim([xmin, xmax*1.05])
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()
        
        locs, labels =plt.xticks()
        print(locs)
        ax4 = ax2.twiny()
        ax4.set_xlim(left=locs[0]*self.pixelsPmm, right=locs[-1]*self.pixelsPmm)
        ax4.set_xlabel('Offset in Main Channel [pixels]')
        
        xmin, xmax = plt.xlim()
#        plt.xlim([xmin, xmax*1.05])
#        xmin, xmax = plt.xlim()
        
        ymin, ymax = plt.ylim()
        plt.ylim([ymin, ymax*1.05])
        ymin, ymax = plt.ylim() 
        
        
        ax2.xaxis.grid(True, color='#D0D0D0')
        ax2.yaxis.grid(True, color='#D0D0D0')
        
        plt.title("Extension & Offset -  " +BatchID, y=1.1)
        plt.plot([],[],'o',color=c1 ,)
        plt.plot([],[],'<',color=c3)
        plt.plot([],[],'s',color=c2 ,)
        plt.plot([],[],'>',color=c4)
        plt.legend(['Max Extension 1','Max Extension 2', 'Max Taylor Parameter 1', 'Max Taylor Parameter 2'], loc='best', fontsize=6) 
        
        plt.legend(loc='best', fontsize=6)
        fig.tight_layout()
        if savepath  != None:
            plt.savefig(savepath+"MaxExtensionVsOffset_" +BatchID.replace(' ', '_').replace('/', '') +".png", dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
            
    def plotAverageMaxExtend(self, d0, savepath=None, BatchID  = '', BatchIDC ='', show=False):
        '''
        Plot maximum width and taylor parameter (d12) in T-Junction Averages
        '''
        c=  self.coloursForMarker()
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)

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
        
#        label1='Fit, m=%.2f' %self.gradient1oQ
#        plt.plot([xmin, xmax], [self.straightLine(xmin, self.gradient1oQ), self.straightLine(xmax, self.gradient1oQ)], label=label1, color=c1, linestyle='-.', linewidth=1)
   
        
#        s='%d turned left and %d turned right \n pixels/mm = %.1f' %(len(self.offCentreTurnedRight), len(self.offCentre)-len(self.offCentreTurnedRight), self.pixelsPmm)
#        ax2.text(0.3, 0.8, s, fontsize=12,    horizontalalignment='center',      verticalalignment='center',
#             transform = ax2.transAxes)
        
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
            plt.savefig(savepath+"AverageMaxExtension_" +BatchIDC+".png", dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
    
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
        self.NDAverageSpeedMainSTD = np.std(yM)
        self.NDAverageSpeedMainErr = np.std(yM)/np.sqrt(len(yM))
        self.NDAverageSpeedDaugther = np.mean(yD)
        self.NDAverageSpeedDaugtherSTD = np.std(yD)
        self.NDAverageSpeedDaugtherErr = np.std(yD)/np.sqrt(len(yD))
        
               
        
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
        self.meanSpeedMainNDSTD = np.std((self.aveSpeedMain/self.pixelsPmm)/ms)
        
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
            self.meanSpeedDaugtherNDSTD = np.std((self.aveSpeedDaugther/self.pixelsPmm)/msD)
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
        plt.xlim([xmin, xmax*1.05])
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
            plt.savefig(savepath+"Speed_ND_Graph_" +BatchIDC+".png", dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
    def plotOffsetVsDistance(self, savepath=None, BatchID  = '', show=False):
        """
        plot offset from centralline versus speed in main channel
        """
        self._findNotEqualTurned()
        c = self.coloursForMarker()
        if BatchID == '':
            BatchID = self.find_batchName(self.path)

        fig = plt.figure(figsize=(8, 6), dpi=200)
        ax = fig.add_subplot(111)
        self.distanceMain= np.array(self.distanceMain)
        print(self.distanceMain)
        plt.plot(self.aveOffCentre/self.pixelsPmm, self.distanceMain/self.pixelsPmm, 's', color = c[3], label= 'Same Direction', linestyle='None')
        plt.plot(self.offCentreTurnedOpposite/self.pixelsPmm, self.distanceMTurnedOpposite/self.pixelsPmm, 'o', color = c[0], label= 'Opposite Direction', linestyle='None')   
        
        xmin, xmax = plt.xlim()
        
        ax.set_xlabel("Average Offset in Main Channel [mm]")
        ax.set_ylabel("Distance in Main Channel [mm]")
 
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
        
        plt.title("Offset vs Distance -  " +BatchID, y=1.1)
        plt.plot([],[],'s',color=c[3] ,)
        plt.plot([],[],'o',color=c[0])
        plt.legend(['Same Direction', 'Opposite Direction'], loc='best')        
        fig.tight_layout()
        ax.xaxis.grid(True, color='#D0D0D0')
        ax.yaxis.grid(True, color='#D0D0D0')
#        plt.grid(color='#D0D0D0', linestyle='--')
        if savepath != None:
            plt.savefig(savepath+"OffsetVsDistance_" +BatchID.replace(' ', '').replace('/', '')+".png", dpi=300, )
        
        if show:
            plt.show()
        else:
            plt.close()


    def coloursForMarker(self, n=4):
        '''
        Returns 4 colours that will be dinstingusiable in greyscale
        Frome: http://colorbrewer2.org/
        '''
#        c1= '#ca0020'
#        c2= '#f4a582'
#        c3= '#92c5de'
#        c4= '#0571b0'
        if n==4:
            c1= '#253494'
            c2= '#2c7fb8'
            c3= '#41b6c4'
            c4= '#a1dab4'
            return [c1, c2, c3, c4]
#        c4= '#ffffb2'
#        c3= '#fecc5c'
#        c2= '#fd8d3c'
#        c1= '#e31a1c'
        
        elif n > 4 and n <= 6:
            c1= '#ffffcc'
            c2= '#c7e9b4'
            c3= '#7fcdbb'
            c4= '#41b6c4'
            c5= '#2c7fb8'
            c6= '#253494'
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

       
        
    
    def calcAll(self):
#        self.findSpeedGradientFromAverages()
        self.findSpeedGradient()
        self.turnedDirection()
    
#rsltRigid3p5mm=ResultsClass('M:\\EdgarHaener\\Capsules\\RigidParticle-3.5mm\\31032015\\RigidParticle-3.5mm-31032015_Results.txt')
#print(rsltRigid3p5mm.volumFlux)
#rsltRigid3p5mm.printData()
