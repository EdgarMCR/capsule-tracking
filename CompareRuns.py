# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 17:27:02 2015

@author: mbbxkeh2

Compare different Runs, i.e. deal with several results classes
"""

from __future__ import absolute_import, division, print_function
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import os

import sys
sys.path.append('C:\\Users\\mbbxkeh2\\Dropbox\\PhD\\Python\\OpenCV\\T-Junction') #Machine ALT 2.115
sys.path.append('C:\\Users\\Edgar\\Dropbox\\PhD\\Python\\OpenCV\\T-Junction') #Machine Schuster G.21
sys.path.append('/home/magda/Dropbox/PhD/Python/OpenCV/T-Junction') #Home Ubuntu

#my imports
import ReadResultsFile as rrf

#=========================
#Constant
SIGNATURE= 'Edgar Haener, ALT 2.105'
HFONT = {'fontname':'Helvetica'}
HFONT = {'fontname':'Comic Sans MS'}
ERRFORCE=0.5


def plotMaxExtension(listOfInstances, listOfd0, listOfNames, savepath=None, title  = '', savename ='', show=False):
    '''
    Plot several main channel speeds
    '''
    #only 6 colours implemented
    leng = len(listOfInstances)
    assert leng <= 10
    c =  listOfInstances[0].coloursForMarker(n=leng)    
    markers=['o', 'h', '<', 'd', '*', 's', '^', 'p' ]
    fig = plt.figure(figsize=(8, 6), dpi=200,)
    ax2 = fig.add_subplot(111)
    aveextension=[]
    aveextensionSTD=[]
    for ii in range(len(listOfInstances)):
        aveextension.append((listOfInstances[ii].aveMaxWidth/listOfInstances[ii].pixelsPmm)/listOfd0[ii])
        aveextensionSTD.append((listOfInstances[ii].aveMaxWidthSTD/listOfInstances[ii].pixelsPmm)/listOfd0[ii])
#        print('len(self.maxWidth) = %d, len(extension) = %d, len(self.volumFlux) = %d' %(len(self.maxWidth), len(extension), len(self.volumFlux)))
        
    for ii in range(len(listOfInstances)):
       ax2.errorbar(listOfInstances[ii].volumFluxesList, aveextension[ii], yerr=aveextensionSTD[ii] ,linestyle='None', marker=markers[ii], label=listOfNames[ii] + ' $d_0 = $ %.1f' %listOfd0[ii], color = c[ii],  markersize=6)#, label='Max Extension')
        
    ax2.set_xlabel("Volumn Flux [ml/min]")
    ax2.set_ylabel("Extension [$d_0$]")
    

    ax2.legend(loc=2, fontsize=6) 
#    ax3 = ax2.twinx()
#    for ii in range(len(listOfInstances)):
#        ax3.errorbar(listOfInstances[ii].volumFluxesList, listOfInstances[ii].aveMaxD12, yerr=listOfInstances[ii].aveMaxD12STD, linestyle='None',   marker='*', label='Max $D_{12}$ ' + listOfNames[ii], color = c[ii], markersize=5)#, label='Max Taylor Parameter')
#    ax3.set_ylabel("Taylor Deformation Paramter $D_{12}$")
    
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
    
    plt.title("Mean Max Extension -  " +title, y=1.01)
#    plt.legend(loc=9, fontsize=6) 
    
    fig.tight_layout()
    if savepath  != None:
        plt.savefig(listOfInstances[0].makeSaveNameSafe(savepath+"AveMaxExtension_" +savename+".png"), dpi=300)
    
    if show:
        plt.show()
    else:
        plt.close()
        
def plotRelaxationTime(listOfInstances, listOfNames, savepath=None, title  = '', savename ='', show=False):
    '''
    Plot several relaxation times
    '''
    #only 6 colours implemented
    leng = len(listOfInstances)
    assert leng <= 10
    c =  listOfInstances[0].coloursForMarker(n=leng)    
    markers=['o', 'h', '<', 'd', '*', 's', '^', 'p' ]
    fig = plt.figure(figsize=(8, 6), dpi=200,)
    ax2 = fig.add_subplot(111)

    for ii in range(len(listOfInstances)):
        y = (np.array(listOfInstances[ii].aveRelaxationTime).flatten())
        ystd = (np.array(listOfInstances[ii].aveRelaxationTimeSTD).flatten())
        ax2.errorbar(listOfInstances[ii].volumFluxesList, y, yerr=ystd ,linestyle='None', marker=markers[ii], label=listOfNames[ii], color = c[ii],  markersize=6)#, label='Max Extension')
    ax2.set_xlabel("Volumn Flux [ml/min]")
    ax2.set_ylabel("Relaxation Time [s]")
    ax2.legend(loc='best', fontsize=6) 

    xmin, xmax = plt.xlim()
#        ax2.set_xlim([xmin, xmax*1.05])
    plt.xlim([0.9*xmin, xmax*1.05])
    xmin, xmax = plt.xlim()
    
    
    ax2.xaxis.grid(True, color='#D0D0D0')
    ax2.yaxis.grid(True, color='#D0D0D0')
    
    plt.title("Relaxation Time -  " +title, y=1.01)
#    plt.legend(loc=9, fontsize=6) 
    
    fig.tight_layout()
    if savepath  != None:
        plt.savefig(listOfInstances[0].makeSaveNameSafe(savepath+"RelaxationTime_" +savename+".png"), dpi=300)
    
    if show:
        plt.show()
    else:
        plt.close()
        
def plotRelaxationDistance(listOfInstances, listOfNames, savepath=None, title  = '', savename ='', show=False):
    '''
    Plot several relaxation times
    '''
    #only 6 colours implemented
    leng = len(listOfInstances)
    assert leng <= 10
    c =  listOfInstances[0].coloursForMarker(n=leng)    
    markers=['o', 'h', '<', 'd', '*', 's', '^', 'p' ]
    fig = plt.figure(figsize=(8, 6), dpi=200,)
    ax2 = fig.add_subplot(111)

    for ii in range(len(listOfInstances)):
        y = ( np.array(listOfInstances[ii].aveRelaxationDistance).flatten()/(listOfInstances[ii].pixelsPmm))
        ystd = ( np.array(listOfInstances[ii].aveRelaxationDistanceSTD).flatten()/(listOfInstances[ii].pixelsPmm))
        ax2.errorbar(listOfInstances[ii].volumFluxesList, y, yerr=ystd ,linestyle='None', marker=markers[ii], label=listOfNames[ii], color = c[ii],  markersize=6)#, label='Max Extension')
    ax2.set_xlabel("Volumn Flux [ml/min]")
    ax2.set_ylabel("Relaxation Distance [mm]")
    ax2.legend(loc='best', fontsize=6) 

    xmin, xmax = plt.xlim()
#        ax2.set_xlim([xmin, xmax*1.05])
    plt.xlim([0.9*xmin, xmax*1.05])
    xmin, xmax = plt.xlim()
    
    
    ax2.xaxis.grid(True, color='#D0D0D0')
    ax2.yaxis.grid(True, color='#D0D0D0')
    
    plt.title("Relaxation Time -  " +title, y=1.01)
#    plt.legend(loc=9, fontsize=6) 
    
    fig.tight_layout()
    if savepath  != None:
        plt.savefig(listOfInstances[0].makeSaveNameSafe(savepath+"RelaxationDistance_" +savename+".png"), dpi=300)
    
    if show:
        plt.show()
    else:
        plt.close()

def plotMaxTaylorDeformation(listOfInstances, listOfd0, listOfNames, savepath=None, title  = '', savename ='', show=False):
    '''
    Plot several main channel speeds
    '''
    #only 6 colours implemented
    leng = len(listOfInstances)
    assert leng <= 10
    c =  listOfInstances[0].coloursForMarker(n=leng)     
        
    fig = plt.figure(figsize=(8, 6), dpi=200,)
    ax2 = fig.add_subplot(111)
#    aveextension=[]
#    aveextensionSTD=[]
#    for ii in range(len(listOfInstances)):
#        aveextension.append((listOfInstances[ii].aveMaxWidth/listOfInstances[ii].pixelsPmm)/listOfd0[ii])
#        aveextensionSTD.append((listOfInstances[ii].aveMaxWidthSTD/listOfInstances[ii].pixelsPmm)/listOfd0[ii])
##        print('len(self.maxWidth) = %d, len(extension) = %d, len(self.volumFlux) = %d' %(len(self.maxWidth), len(extension), len(self.volumFlux)))
#        
#    for ii in range(len(listOfInstances)):
#        ax2.errorbar(listOfInstances[ii].volumFluxesList, aveextension[ii], yerr=aveextensionSTD[ii] ,linestyle='None', marker='h', label='Max Extension ' + listOfNames[ii], color = c[ii],  markersize=6)#, label='Max Extension')
        
    ax2.set_xlabel("Volumn Flux [ml/min]")
#    ax2.set_ylabel("Extension [$d_0$]")
#    ax2.legend(loc=2, fontsize=6) 
#    ax3 = ax2.twinx()
    for ii in range(len(listOfInstances)):
        ax2.errorbar(listOfInstances[ii].volumFluxesList, listOfInstances[ii].aveMaxD12, yerr=listOfInstances[ii].aveMaxD12STD, linestyle='None',   marker='*', label='Max $D_{12}$ ' + listOfNames[ii], color = c[ii], markersize=5)#, label='Max Taylor Parameter')
    ax2.set_ylabel("Taylor Deformation Paramter $D_{12}$")
    
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
    
    plt.title("Mean Max Taylor -  " +title, y=1.01)
    plt.legend(loc=2, fontsize=6) 
    
    fig.tight_layout()
    if savepath  != None:
        plt.savefig(listOfInstances[0].makeSaveNameSafe(savepath+"AveMaxTaylor_" +savename+".png"), dpi=300)
    
    if show:
        plt.show()
    else:
        plt.close()
        
        
def plotSpeedMainChannel(listOfInstances, listOfd0, listOfNames, savepath=None, title  = '', savename ='', show=False, plotPrediction=False, plotDaugtherChannel=False):

        #only 6 colours implemented
        leng = len(listOfInstances)
        assert leng <= 8
        if leng <= 4:
            c=  listOfInstances[0].coloursForMarker()
        elif leng <= 6:
            c =  listOfInstances[0].coloursForMarker(n=6)
        elif leng <= 8:
            c =  listOfInstances[0].coloursForMarker(n=8)
        
        #get drag coefficients
        if plotPrediction:
            import track_capsule_TJ_v0p10 as tc
            lamb=[]
            G=[]
            for ii in range(len(listOfInstances)):
                lamb.append(listOfd0[ii]/np.sqrt(4*7.8))
                k1, k2 = tc.getDragCoef(lamb[-1])
                G.append(k2/k1)
        


        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
        
        size3p5=6
        #errorbar average3p5beforSTD
        sampleNum=[]
        for ii in range(len(listOfInstances)):
            plt.errorbar(listOfInstances[ii].volumFluxesList, listOfInstances[ii].aveSpeedMain/listOfInstances[ii].pixelsPmm, yerr=listOfInstances[ii].aveSpeedMainSTD/listOfInstances[ii].pixelsPmm, linestyle='None',  marker='h', color = c[ii], label='Speed Main Channel ' + listOfNames[ii], markersize=size3p5) #
            if plotDaugtherChannel:
                plt.errorbar(listOfInstances[ii].volumFluxesList, listOfInstances[ii].aveSpeedDaugther/listOfInstances[ii].pixelsPmm, yerr=listOfInstances[ii].aveSpeedDaugtherSTD/listOfInstances[ii].pixelsPmm, linestyle='None',  marker='*', color = c[ii], label='Speed Daugther Channel '+ listOfNames[ii], markersize=size3p5) #
            sampleNum.append(len(listOfInstances[ii].SpeedMain))
            
        if plotPrediction:
            s2='      Error based on standard deviation of sample'
            for ii in range(len(listOfInstances)):
                s2 += '\n%s:  Runs = %d, G = %.2f with $\lambda $ = %.2f and $d_0$ = %.2f $mm$' %(listOfNames[ii], sampleNum[ii], G[ii], lamb[ii], listOfd0[ii])
        else:
            s2='   Error based on standard deviation of sample' 
            for ii in range(len(listOfInstances)):
                s2 += '\n    %s has %d  data points' %(listOfNames[ii], sampleNum[ii])
            
        xmin, xmax = plt.xlim()
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()
        ymin, ymax = plt.ylim()
        if leng <6:
            fs=8
            xm=0.28
            nrCol=1
        elif leng <7:
            fs=6
            xm=0.38
            nrCol=1
            
        else:
            fs = 5
            xm=0.48
            nrCol=2
            
        ax2.text(xmin+xmax*xm, ymin+ymax*0.01, s2, fontsize=fs)
        #fit
        if plotPrediction:
            for ii in range(len(listOfInstances)):
                label='Predicted Speed Gradient %s = %.2f' %(listOfNames[ii], G[ii])
                plt.plot([xmin, xmax], [((2*G[ii]*xmin*1000.0/60)/32.0), ((2*G[ii]*xmax*1000.0/60)/32.0)], label=label, color=c[ii], linestyle=':', linewidth=1)
            
        for ii in range(len(listOfInstances)):
            label1='Fit Main Channel %s m=%.2f' %(listOfNames[ii], listOfInstances[ii].gradientSpeedMain)
            plt.plot([xmin, xmax], [listOfInstances[ii].straightLine(xmin, listOfInstances[ii].gradientSpeedMain), listOfInstances[ii].straightLine(xmax, listOfInstances[ii].gradientSpeedMain)], label=label1, color=c[ii], linestyle='-.', linewidth=1)
        
        if plotDaugtherChannel:
            for ii in range(len(listOfInstances)):
                label1='Fit Daugther Channel %s m=%.2f' %(listOfNames[ii],listOfInstances[ii].gradientSpeedDaugther)
                plt.plot([xmin, xmax], [listOfInstances[ii].straightLine(xmin, listOfInstances[ii].gradientSpeedDaugther), listOfInstances[ii].straightLine(xmax, listOfInstances[ii].gradientSpeedDaugther)], label=label1, color=c[ii], linestyle='--', linewidth=1)

        #label1='3mm Fit Main Chanel, m=%.2f' %rsltRigid3mmRed230415.gradientSpeedMain
        #label2='3mm Fit Daugther Chanel, m=%.2f' %rsltRigid3mmRed230415.gradientSpeedDaugther
        #plt.plot([minVolumnFlux, maxVolumnFlux], [f2(minVolumnFlux, rsltRigid3mmRed230415.gradientSpeedMain), f2(maxVolumnFlux, rsltRigid3mmRed230415.gradientSpeedMain)], label=label1, color=c1, linestyle='-.', linewidth=1)
        #plt.plot([minVolumnFlux, maxVolumnFlux], [f2(minVolumnFlux, rsltRigid3mmRed230415.gradientSpeedDaugther), f2(maxVolumnFlux, rsltRigid3mmRed230415.gradientSpeedDaugther)], label=label2, color=c4, linestyle=':', linewidth=1)
        
        plt.plot([xmin, xmax], [((2*xmin*1000.0/60)/32.0), ((2*xmax*1000.0/60)/32.0)], label='2 x Mean Speed', color='k', linestyle='--', linewidth=1)
        plt.plot([xmin, xmax], [((xmin*1000.0/60)/32.0), ((xmax*1000.0/60)/32.0)], label='Mean Speed', color='k', linestyle='-', linewidth=1)
        
        plt.show()
        
        plt.title("Average Speed Main Channel -  " +title)
        plt.xlabel("Volumn Flux [ml/min]")
        plt.ylabel("Speed   [mm/s]")
        
        plt.legend(loc=2, fontsize=fs, ncol =nrCol)
        
        if savepath != None:
            plt.savefig(listOfInstances[0].makeSaveNameSafe(savepath+"SpeedWFit_Graph_" +savename+".png"), dpi=300)
#            plt.savefig(savepath+"SpeedWFit_Graph_" +savename+".pdf", dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
            
        
def plotSpeedDaugtherChannel(listOfInstances, listOfd0, listOfNames, savepath=None, title  = '', savename ='', show=False, plotPrediction=False):

        #only 6 colours implemented
        leng = len(listOfInstances)
        assert leng <= 8
        if leng <= 4:
            c=  listOfInstances[0].coloursForMarker()
        elif leng <= 6:
            c =  listOfInstances[0].coloursForMarker(n=6)
        elif leng <= 8:
            c =  listOfInstances[0].coloursForMarker(n=8)
            
        
        #get drag coefficients
        dChannel = np.sqrt(4*4)
        
        actualLambda=[]
        if plotPrediction:
            import track_capsule_TJ_v0p10 as tc
            lamb=[]
            G=[]
            for ii in range(len(listOfInstances)):
                templambda=listOfd0[ii]/dChannel
                actualLambda.append(templambda)
                if templambda > 0.95:
                    print('lambda too big, set to 0.95')
                    templambda=0.95
                lamb.append(templambda)
                k1, k2 = tc.getDragCoef(lamb[-1])
                G.append(k2/k1)
        


        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
        
        size3p5=6
        #errorbar average3p5beforSTD
        sampleNum=[]
        for ii in range(len(listOfInstances)):
            plt.errorbar(listOfInstances[ii].volumFluxesList, listOfInstances[ii].aveSpeedDaugther/listOfInstances[ii].pixelsPmm, yerr=listOfInstances[ii].aveSpeedMainSTD/listOfInstances[ii].pixelsPmm, linestyle='None',  marker='h', color = c[ii], label='Speed Daugther Channel ' + listOfNames[ii], markersize=size3p5) #
            sampleNum.append(len(listOfInstances[ii].SpeedMain))
            
        if plotPrediction:
            s2='      Error based on standard deviation of sample'
            for ii in range(len(listOfInstances)):
                if actualLambda [ii] == lamb[ii]: 
                    s2 += '\n%s:  Runs = %d, G = %.2f with $\lambda $ = %.2f and $d_0$ = %.2f $mm$' %(listOfNames[ii], sampleNum[ii], G[ii], lamb[ii], listOfd0[ii])
                else:
                    s2 += '\n%s:  Runs = %d, G = %.2f with $\lambda $ = %.2f (actually = %.2f) and $d_0$ = %.2f $mm$' %(listOfNames[ii], sampleNum[ii], G[ii], lamb[ii], actualLambda [ii], listOfd0[ii])
        else:
            s2='   Error based on standard deviation of sample' 
            for ii in range(len(listOfInstances)):
                s2 += '\n    %s has %d  data points' %(listOfNames[ii], sampleNum[ii])
            
        xmin, xmax = plt.xlim()
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()
        ymin, ymax = plt.ylim()
        
        UmeanMin = (xmin*1000.0/60)/(2*16.0)      
        UmeanMax = (xmax*1000.0/60)/(2*16.0 )
        
#        print('UmeanMin, UmeanMax in Main = %.2f, %.2f \t in Daugther = %.2f, %.2f' %((xmin*1000.0/60)/32.0, (xmax*1000.0/60)/32.0, UmeanMin,UmeanMax))
        if leng <6:
            fs=8
            xm=0.28
            nrCol=1
        elif leng <7:
            fs=6
            xm=0.38
            nrCol=1
            
        else:
            fs = 5
            xm=0.48
            nrCol=2

        ax2.text(xmin+xmax*xm, ymin+ymax*0.01, s2, fontsize=fs)
        #fit
        if plotPrediction:
            for ii in range(len(listOfInstances)):
                label='Predicted Speed Gradient %s = %.2f' %(listOfNames[ii], G[ii])
                plt.plot([xmin, xmax], [(2*G[ii]*  UmeanMin), ((2*G[ii]*UmeanMax))], label=label, color=c[ii], linestyle=':', linewidth=1)
            
        for ii in range(len(listOfInstances)):
            label1='Fit Daugther Channel %s m=%.2f' %(listOfNames[ii],listOfInstances[ii].gradientSpeedDaugther)
            plt.plot([xmin, xmax], [listOfInstances[ii].straightLine(xmin, listOfInstances[ii].gradientSpeedDaugther), listOfInstances[ii].straightLine(xmax, listOfInstances[ii].gradientSpeedDaugther)], label=label1, color=c[ii], linestyle='--', linewidth=1)

        #label1='3mm Fit Main Chanel, m=%.2f' %rsltRigid3mmRed230415.gradientSpeedMain
        #label2='3mm Fit Daugther Chanel, m=%.2f' %rsltRigid3mmRed230415.gradientSpeedDaugther
        #plt.plot([minVolumnFlux, maxVolumnFlux], [f2(minVolumnFlux, rsltRigid3mmRed230415.gradientSpeedMain), f2(maxVolumnFlux, rsltRigid3mmRed230415.gradientSpeedMain)], label=label1, color=c1, linestyle='-.', linewidth=1)
        #plt.plot([minVolumnFlux, maxVolumnFlux], [f2(minVolumnFlux, rsltRigid3mmRed230415.gradientSpeedDaugther), f2(maxVolumnFlux, rsltRigid3mmRed230415.gradientSpeedDaugther)], label=label2, color=c4, linestyle=':', linewidth=1)
        
        plt.plot([xmin, xmax], [(2*UmeanMin), (2*UmeanMax)], label='2 x Mean Speed', color='k', linestyle='--', linewidth=1)
        plt.plot([xmin, xmax], [UmeanMin, UmeanMax], label='Mean Speed', color='k', linestyle='-', linewidth=1)
        
        plt.show()
        
        plt.title("Average Speed Daugther Channel -  " +title)
        plt.xlabel("Volumn Flux [ml/min]")
        plt.ylabel("Speed   [mm/s]")
        
        plt.legend(loc=2, fontsize=fs, ncol = nrCol)
        
        if savepath != None:
            plt.savefig(listOfInstances[0].makeSaveNameSafe(savepath+"SpeedDaugtherWFit_" +savename+".png"), dpi=300)
#            plt.savefig(savepath+"SpeedDaugtherWFit_" +savename+".pdf", dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()


def plotTvs1oQ(listOfInstances, listOfNames, savepath=None, title  = '', savename ='', show=False):
        '''
        Plot time in T-Junction versus 1/Flow rate
        '''
        #only 6 colours implemented
        leng = len(listOfInstances)
        assert leng <= 8
        if leng <= 4:
            c=  listOfInstances[0].coloursForMarker()
        elif leng <= 6:
            c =  listOfInstances[0].coloursForMarker(n=6)
        elif leng <= 8:
            c =  listOfInstances[0].coloursForMarker(n=8)

        
        markers=['o', 'h', '<', 'd', '*', 's', '^', 'p' ]
        
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111)
        iQ=[]        
        for ii in range(len(listOfInstances)):
            iQ.append( 1.0/listOfInstances[ii].volumFluxesList)
            plt.errorbar(iQ[ii], listOfInstances[ii].aveTimeinTJ, yerr=listOfInstances[ii].aveTimeinTJSTD, linestyle='None', marker=markers[ii], color = c[ii], label='Time in T-Junction '+ listOfNames[ii], markersize=5)
        
        xmin, xmax = plt.xlim()
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()
        
        for ii in range(len(listOfInstances)):
            label1='Fit %s: m=%.2f' %(listOfNames[ii], listOfInstances[ii].gradient1oQ)
            plt.plot([xmin, xmax], [listOfInstances[ii].straightLine(xmin, listOfInstances[ii].gradient1oQ), listOfInstances[ii].straightLine(xmax, listOfInstances[ii].gradient1oQ)], label=label1, color=c[ii], linestyle='-.', linewidth=1)


        ax2.set_xlabel("1/Volumn Flux [min/ml]")
        ax2.set_ylabel("Time in T-Junction [s]")
        
#        locs, labels =plt.xticks()
#        print(locs)
#        ax3 = ax2.twiny()
#        ax3.set_xlim(left=locs[0]*self.pixelsPmm, right=locs[-1]*self.pixelsPmm)
#        ax3.set_xlabel('Offset in Main Channel [pixels]')
#        ymin, ymax = plt.ylim()
#        plt.ylim([ymin, ymax*1.05])
#        ymin, ymax = plt.ylim()       
        
#        s='%d turned left and %d turned right \n pixels/mm = %.1f' %(len(self.offCentreTurnedRight), len(self.offCentre)-len(self.offCentreTurnedRight), self.pixelsPmm)
#        ax2.text(0.3, 0.8, s, fontsize=12,    horizontalalignment='center',      verticalalignment='center',
#             transform = ax2.transAxes)
        
        
        ax2.xaxis.grid(True, color='#D0D0D0')
        ax2.yaxis.grid(True, color='#D0D0D0')
        
        plt.title("Time vs 1/Q -  " +title, y=1.01)
        fig.tight_layout()
#        plt.plot([],[],'o',color=c1 ,)
#        plt.plot([],[],'s',color=c4)
#        plt.legend(['Turned right', 'Turned left'], loc=6, fontsize=6) 
        
        plt.legend(loc=2, fontsize=6)
        
        if savepath  != None:
            plt.savefig(listOfInstances[0].makeSaveNameSafe(savepath+"Tvs1oQ_" +savename+".png"), dpi=300)
        if show:
            plt.show()
        else:
            plt.close()
            
def printParameters(listOfClassInstances, lostOfD0, listOfNames):
    if not hasattr(listOfClassInstances[0], 'NDGradientSpeedMain'):
        for ii in range(len(listOfClassInstances)):
            listOfClassInstances[ii].findNonDimensionalgradientSpeedChannel()
        
    print('Batch Name \t Capsule Nr \t diameter \t \t speed main \t +/- \t err \t R2 \t p-value \t \t speed Daugther \t +/- \t err \t r2 \t p-value  \t \t T vs 1/Q \t +/- \t err \t r2 \t p-value  \t \t Left \t Right \t Max Width \t Max D12')
    for ii in range(len(listOfClassInstances)):
        print('%s \t %s \t %.1f \t \t %.2f \t +/- \t %.4f \t %.2f \t %.3e \t \t %.2f \t +/- \t %.4f \t %.2f \t %.3e \t \t %.2f \t +/- \t %.2f \t %.2f \t %.3e \t \t %d \t %d \t%.2f \t %.2f' 
            %(listOfNames[ii][:-3], listOfNames[ii][-3:], lostOfD0[ii], 
            listOfClassInstances[ii].gradientSpeedMain, listOfClassInstances[ii].gradientSpeedMainErr, listOfClassInstances[ii].gradientSpeedMainR2, listOfClassInstances[ii].gradientSpeedMainPValue ,
            listOfClassInstances[ii].gradientSpeedDaugther , listOfClassInstances[ii].gradientSpeedDaugtherErr, listOfClassInstances[ii].gradientSpeedDaugtherR2, listOfClassInstances[ii].gradientSpeedDaugtherPValue,
            listOfClassInstances[ii].gradient1oQ, listOfClassInstances[ii].gradient1oQErr, listOfClassInstances[ii].gradient1oQR2,  listOfClassInstances[ii].gradient1oQPValue,
            len(listOfClassInstances[ii].offCentreTurnedRight), 
            len(listOfClassInstances[ii].offCentre)-len(listOfClassInstances[ii].offCentreTurnedRight),
            listOfClassInstances[ii].maxWidth[-1]/(listOfClassInstances[ii].pixelsPmm*lostOfD0[ii]), listOfClassInstances[ii].aveMaxD12[-1]))
    
#    for ii in range(len(listOfClassInstances)):
#        print('chi = %.2f' %(listOfClassInstances[ii].gradientSpeedMainRChi2* len(listOfClassInstances[ii].SpeedMain)))
    print('\nMain Speed Averages')
    for ii in range(len(listOfClassInstances)):
        print('%.2f \t +/- \t %.4f \t %.2f \t %.3f'%(listOfClassInstances[ii].aveGradientSpeedMain, listOfClassInstances[ii].aveGradientSpeedMainErr, listOfClassInstances[ii].aveGradientSpeedMainRChi2, listOfClassInstances[ii].aveGradientSpeedMainPValue ))
        
     
    print('\n Duagther Speed Averages')
    for ii in range(len(listOfClassInstances)):
        print('%.2f \t +/- \t %.4f \t %.2f \t %.3f'%(listOfClassInstances[ii].aveGradientSpeedDaugther, listOfClassInstances[ii].aveGradientSpeedDaugtherErr, listOfClassInstances[ii].aveGradientSpeedDaugtherRChi2, listOfClassInstances[ii].aveGradientSpeedDaugtherPValue))
        
    
    print('\n T vs 1/q Averages')
    for ii in range(len(listOfClassInstances)):
        print('%.2f \t +/- \t %.4f \t %.2f \t %.3f'%(listOfClassInstances[ii].aveGradient1oQ, listOfClassInstances[ii].aveGradient1oQErr, listOfClassInstances[ii].aveGradient1oQRChi2,  listOfClassInstances[ii].aveGradient1oQPValue))
        
def plotNDSpeedGradients(listOfClassInstances, listOfD0, listOfNames, savepath='CheckSpeed', show=False):
    if savepath != None:
        path = savepath+os.sep
        if not os.path.exists(savepath): os.makedirs(savepath)
    else:
        path =None
                
    for ii in range(len(listOfClassInstances)):

        listOfClassInstances[ii].plotSpeedMainChannelNonDimensional(savepath=path, d0=listOfD0[ii], BatchID  = listOfNames[ii], BatchIDC =listOfNames[ii].replace(' ', '_'), show=show, plotDaugtherChannel=True)

def findPseudCA(q, f, ef):
    '''Take volumn flux q and force f with error ef and return CA, errCA'''
    q = np.array(q)
    CA = q/f
    errCAp = q/(f+ef)
    errCAm = q/(f-ef)
    errCA = (errCAm - errCAp)/2.0
    return CA, errCA
    
def plotNDSpeedMainCA(listOfClassInstances, listOfD0, listOfNames, force,  compression, savepath='CheckSpeed', show=False, CA = True, forPub=False):
    
    #Find the predicted speed
    dChannel = np.sqrt(8*4)
    lamb=3.7/dChannel
    import track_capsule_TJ_v0p12 as tc
    k1, k2 = tc.getDragCoef(lamb)
    G = (k2/k1)
    print('lamb = %.2f, G = %.2f' %(lamb, G))
                
    leng= len(listOfClassInstances)
    assert(leng <= 10)
    c =  listOfClassInstances[0].coloursForMarker(n=leng) 
    if not forPub:
        fig = plt.figure(figsize=(8, 6), dpi=200,); ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
    else:
        fig = plt.figure(figsize=(4, 4), dpi=300,); ax2 = fig.add_subplot(111)
    sizeM=6; markers=['s', 'o', 'h', '>', 'p', 'd', '<', '*', 'x', '+']
    
    for jj in range(leng):
        ms=[]
        for ii in range(len(listOfClassInstances[jj].volumFluxesList)):
            meanSpeed = ((listOfClassInstances[jj].volumFluxesList[ii]*1000.0/60)/32.0)
            ms.append(meanSpeed)
            
        pseudoCA, pseudoCAerr = findPseudCA(listOfClassInstances[jj].volumFluxesList, force[jj], ERRFORCE)
        ms=np.array(ms)
        
        if CA:
            plt.errorbar(x=pseudoCA, xerr=pseudoCAerr, y=(listOfClassInstances[jj].aveSpeedMain/listOfClassInstances[jj].pixelsPmm)/ms, yerr=(listOfClassInstances[jj].aveSpeedMainSTD/listOfClassInstances[jj].pixelsPmm)/ms, marker = markers[jj], color = c[jj], label='%s ($d_0= $ %.1f)' %(listOfNames[jj], listOfD0[jj]),  markersize=sizeM,linestyle='None') #
        else:
            plt.errorbar(x=listOfClassInstances[jj].volumFluxesList, y=(listOfClassInstances[jj].aveSpeedMain/listOfClassInstances[jj].pixelsPmm)/ms, yerr=(listOfClassInstances[jj].aveSpeedMainSTD/listOfClassInstances[jj].pixelsPmm)/ms, marker = markers[jj], color = c[jj], label='%s ($d_0= $ %.1f)' %(listOfNames[jj], listOfD0[jj]),  markersize=sizeM,linestyle='None') #
    xmin, xmax = plt.xlim()
    
    if CA:    
        if not forPub:
            plt.title("Pseudo Capilary number versus Speed Main Channel")
            s1 = ' '
            for ii in range(leng):
                s1 += '%d, ' %len(listOfClassInstances[ii].volumFlux)
            plt.text(0.5, 0.5, 'Assumed Error on Force = %.1f \nNumber of Runs [%s]' %(ERRFORCE, s1), fontsize = 12, horizontalalignment='left', verticalalignment='center', transform = ax2.transAxes)
    
        plt.xlabel("Pseudo $Ca$ (using Force at %d %% Compresion)" %compression)
    else:
        if not forPub: plt.title("$Q$ versus Speed Main Channel")
        plt.xlabel("Volumn Flux $Q$")
    plt.ylabel("Speed [fraction mean speed]")
    if not forPub:
        plt.legend(loc='best', fontsize=6)
        plt.xlim([xmin, xmax*1.05])
        plt.text(0.99, 0.01, SIGNATURE, fontsize = 4, horizontalalignment='right', verticalalignment='center', transform = ax2.transAxes, **HFONT)
    else:
        plt.xticks(fontsize = 10)
        plt.yticks(fontsize = 10)
    
#    plt.plot([xmin, xmax], [(2*G), ((2*G))], color='b', linestyle='--', linewidth=2)
    
    plt.show()
    plt.tight_layout()

    if savepath != None:
        if not forPub:
            if savepath !=  ''  and not os.path.exists(savepath): os.makedirs(savepath)
            name=os.path.join(os.sep, "NDSpeedMain_Ca=%s.jpg" %CA)
            plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)
        else:
            plt.savefig(listOfClassInstances[0].makeSaveNameSafe("C:\\Users\\mbbxkeh2\\Dropbox\\PhD\\AdministrativeStuff\\Conferences\\FiguresPoster\\NDSpeedMain_Ca=%s.png" %CA), dpi=300)

    if show:
        plt.show()
    else:
        plt.close()
        
def plotNDSpeedDaugtherCA(listOfClassInstances, listOfD0, listOfNames, force,  compression, savepath='CheckSpeed', show=False, CA=True):
    leng= len(listOfClassInstances)
    assert(leng <= 10)
    c =  listOfClassInstances[0].coloursForMarker(n=leng) 
    fig = plt.figure(figsize=(8, 6), dpi=200,); ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
    sizeM=6; markers=['s', 'o', 'h', '>', 'p', 'd', '<', '*', 'x', '+']
    
    for jj in range(leng):
        ms=[]
        for ii in range(len(listOfClassInstances[jj].volumFluxesList)):
            meanSpeed = ((listOfClassInstances[jj].volumFluxesList[ii]*1000.0/60)/32.0)
            ms.append(meanSpeed)
        ms=np.array(ms)
        pseudoCA, pseudoCAerr = findPseudCA(listOfClassInstances[jj].volumFluxesList, force[jj], ERRFORCE)
        if CA:
            plt.errorbar(x=pseudoCA, xerr = pseudoCAerr, y=(listOfClassInstances[jj].aveSpeedDaugther/listOfClassInstances[jj].pixelsPmm)/ms, yerr=(listOfClassInstances[jj].aveSpeedDaugtherSTD/listOfClassInstances[jj].pixelsPmm)/ms, marker = markers[jj], color = c[jj], label='%s ($d_0= $ %.1f)' %(listOfNames[jj], listOfD0[jj]),  markersize=sizeM,linestyle='None') #
        else:
            plt.errorbar(x=listOfClassInstances[jj].volumFluxesList, y=(listOfClassInstances[jj].aveSpeedDaugther/listOfClassInstances[jj].pixelsPmm)/ms, yerr=(listOfClassInstances[jj].aveSpeedDaugtherSTD/listOfClassInstances[jj].pixelsPmm)/ms, marker = markers[jj], color = c[jj], label='%s ($d_0= $ %.1f)' %(listOfNames[jj], listOfD0[jj]),  markersize=sizeM,linestyle='None') #
    if CA:
        s1 = ' '
        for ii in range(leng):
            s1 += '%d, ' %len(listOfClassInstances[ii].volumFlux)
        plt.text(0.5, 0.5, 'Assumed Error on Force = %.1f \nNumber of Runs [%s]' %(ERRFORCE, s1), fontsize = 12, horizontalalignment='left', verticalalignment='center', transform = ax2.transAxes)
    xmin, xmax = plt.xlim()
    plt.xlim([xmin, xmax*1.05])
    
    plt.text(0.99, 0.01, SIGNATURE, fontsize = 4, horizontalalignment='right', verticalalignment='center', transform = ax2.transAxes, **HFONT)
    if CA:    
        plt.title("Pseudo Capilary number versus Speed Daugther Channel")
        plt.xlabel("Pseudo $Ca$ (using Force at %d %% Compresion)" %compression)
    else:
        plt.title("$Q$ versus Speed Daugther Channel")
        plt.xlabel("Volumn Flux $Q$")
    plt.ylabel("Speed [fraction mean speed]")
    plt.legend(loc='best', fontsize=6)
    plt.show()

    if savepath != None:
        if savepath != '' and not os.path.exists(savepath): os.makedirs(savepath)
        name=os.path.join(os.sep, "NDSpeedDaugther_Ca=%s.jpg" %CA)
        p = savepath+name

        plt.savefig(listOfClassInstances[0].makeSaveNameSafe(p), dpi=300)

    if show:
        plt.show()
    else:
        plt.close()
        
def plotExtensionVsCA(listOfClassInstances, listOfD0, listOfNames, force,  compression, savepath='CheckSpeed', show=False, CA=True, forPub =False):
    leng= len(listOfClassInstances)
    assert(leng <= 10)
    c =  listOfClassInstances[0].coloursForMarker(n=leng) 
    if not forPub:
        fig = plt.figure(figsize=(8, 6), dpi=200,)
    else:
        fig = plt.figure(figsize=(4, 4), dpi=300,)
    
    ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
    sizeM=6; markers=['s', 'o', 'h', '>', 'p', 'd', '<', '*', 'x', '+']
    
    for jj in range(leng):
        pseudoCA, pseudoCAerr = findPseudCA(listOfClassInstances[jj].volumFluxesList, force[jj], ERRFORCE)
        extension = (listOfClassInstances[jj].aveMaxWidth/listOfClassInstances[jj].pixelsPmm)/listOfD0[jj]
        extensionSTD = (listOfClassInstances[jj].aveMaxWidthSTD/listOfClassInstances[jj].pixelsPmm)/listOfD0[jj]
        if CA:
            plt.errorbar(x=pseudoCA, xerr = pseudoCAerr, y=extension, yerr=extensionSTD, marker = markers[jj], color = c[jj], label='%s ($d_0= $ %.1f)' %(listOfNames[jj], listOfD0[jj]),  markersize=sizeM,linestyle='None') #
        else:
            plt.errorbar(x=listOfClassInstances[jj].volumFluxesList, y=extension, yerr=extensionSTD, marker = markers[jj], color = c[jj], label='%s ($d_0= $ %.1f)' %(listOfNames[jj], listOfD0[jj]),  markersize=sizeM,linestyle='None') #

    xmin, xmax = plt.xlim()
       
    
    if CA:
        if not forPub: 
            plt.title("Pseudo Capilary number versus max extension")
            s1 = ' '
            for ii in range(leng):
                s1 += '%d, ' %len(listOfClassInstances[ii].volumFlux)
            plt.text(0.5, 0.3, 'Assumed Error on Force = %.1f \nNumber of Runs [%s]' %(ERRFORCE, s1), fontsize = 12, horizontalalignment='left', verticalalignment='center', transform = ax2.transAxes)
    
        plt.xlabel("Pseudo $Ca$ (force at %d %% Compresion)" %compression)
    else:
        if not forPub: plt.title("Volumn Flux vs max extension")
        plt.xlabel("Volumn Flux $Q$ [ml/min]")
    
    plt.ylabel("Extension [$d_0$]")
    if not forPub: 
        plt.legend(loc='best', fontsize=6)
        plt.xlim([xmin, xmax*1.05]) 
        plt.text(0.99, 0.01, SIGNATURE, fontsize = 4, horizontalalignment='right', verticalalignment='center', transform = ax2.transAxes, **HFONT)
    else:
        plt.xticks(fontsize = 10)
        plt.yticks(fontsize = 10)
        
    plt.show()
    fig.tight_layout()

    if savepath != None:
        if not forPub:
            if savepath != ''  and not os.path.exists(savepath): os.makedirs(savepath)
            name=os.path.join(os.sep, "ExtensionVsCA_CA=%s.jpg" %(CA))
            plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)
        else:
            plt.savefig(listOfClassInstances[0].makeSaveNameSafe('C:\\Users\\mbbxkeh2\\Dropbox\\PhD\\AdministrativeStuff\\Conferences\\FiguresPoster\\ExtensionVsCA.png'), dpi=300)
    if show:
        plt.show()
    else:
        plt.close()


def plotGradientDifference(listOfClassInstances,  listOfD0, listOfNames, savepath='CheckSpeedGradients', show=False):
    if not hasattr(listOfClassInstances[0], 'mainChannelGradientDifferencToPredicted'):
        plotNDSpeedGradients(listOfClassInstances, listOfD0, listOfNames, savepath=None, show=False)
    
#    plt.xkcd()
    main = []
    daugther = []
    
    for ii in range(len(listOfClassInstances)):
        main.append(listOfClassInstances[ii].mainChannelGradientDifferencToPredicted)
        daugther.append(listOfClassInstances[ii].daugtherChannelGradientDifferencToPredicted)
        
    c=  listOfClassInstances[0].coloursForMarker()
    
    fig = plt.figure(figsize=(8, 6), dpi=200)
    ax = fig.add_subplot(111)
    x = range(len(listOfClassInstances))
    plt.xticks(x, listOfNames, rotation=45)
    plt.plot(x,main,marker = "s", color=c[0], label='Main Channel')
    plt.plot(x,daugther,marker = "o", color=c[2], label='Daugther Channel')
    plt.legend(loc='best', fontsize=6)
    
    locs, labels =plt. xticks()
    ax2 = ax.twiny()
    plt.xticks(x, listOfD0)

    ax2.set_xlabel('Capsule Diameter [mm]')
    plt.title("Difference between predicted and measured gradient", y=1.2)
    plt.ylabel("Difference (predicted - measured)")
    plt.tight_layout()
    plt.show()
    plt.text(0.99, 0.01, SIGNATURE, fontsize = 4, horizontalalignment='right', verticalalignment='center', transform = ax2.transAxes, **HFONT)
    if savepath != None:
        if not os.path.exists(savepath) and savepath != "": 
            os.makedirs(savepath)
        if savepath != "":
            name=os.path.join(os.sep, "GradientDifference.jpg")
        else:
            name = "GradientDifference.png"

        plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)
    
    if show:
        plt.show()
    else:
        plt.close()
    
def plotAverageMaxExtension(listOfClassInstances,  listOfNames, listOfd0, savepath='CheckAveExtension', show=False):
    if not os.path.exists(savepath): os.makedirs(savepath)
    for ii in range(len(listOfClassInstances)):
        listOfClassInstances[ii].plotAverageMaxExtend(listOfd0[ii], savepath=savepath+os.sep,  BatchID  = listOfNames[ii], BatchIDC =listOfNames[ii].replace(' ', '_'), show=show)

def plotOffsetVsMainSpeedND(listOfClassInstances,  listOfNames, savepath='CheckSpeed', show=False):
    if not os.path.exists(savepath): os.makedirs(savepath)
    for ii in range(len(listOfClassInstances)):
        listOfClassInstances[ii].plotOffsetVsMainSpeed(savepath=savepath+os.sep,  BatchID  = listOfNames[ii], BatchIDC =listOfNames[ii].replace(' ', '_'), show=show)

def plotTimeVs1oQ_Induvidual(listOfClassInstances,  listOfNames, savepath='CheckTVs1OQ', show=False):
    if not os.path.exists(savepath): os.makedirs(savepath)
    m1=[];  m2=[];  m3 =[]; 
    
    for ii in range(len(listOfClassInstances)):
        m1t, m2t, m3t = listOfClassInstances[ii].plotTvs1oQ(savepath=savepath+os.sep,  BatchID  = listOfNames[ii], BatchIDC =listOfNames[ii].replace(' ', '_'), show=show)
        m1.append(m1t)
        m2.append(m2t)
        m3.append(m3t)
        
    c=  listOfClassInstances[0].coloursForMarker()
    fig = plt.figure(figsize=(8, 6), dpi=200)
    ax = fig.add_subplot(111)
    x = range(len(listOfClassInstances))
    plt.xticks(x, listOfNames, rotation=45)
    plt.plot(x,m1,marker = "s", color=c[0], label='All Data Points')
    plt.plot(x,m3,marker = "o", color=c[2], label='within 0.07mm if centreline')
    plt.legend(loc='best', fontsize=6)    
    plt.title("Difference T vs 1/Q gradient from offset", y=1.01)
    plt.ylabel("T vs 1/Q gradient")
    plt.tight_layout()
    plt.show()
    plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+'DifferenceTvs1oQGradient_centralStreamline.png'), dpi=300)

def plotOffsetVsTime_Induvidual(listOfClassInstances,  listOfNames, savepath='Offset', show=False):
    if not os.path.exists(savepath): os.makedirs(savepath)
    
    for ii in range(len(listOfClassInstances)):
        listOfClassInstances[ii].plotOffsetVsTime(savepath=savepath+os.sep,  BatchID  = listOfNames[ii], show=show)
        listOfClassInstances[ii].plotAverageBinnedTimeInTJ( savepath=savepath+os.sep, show=show, binWidth=1)
        listOfClassInstances[ii].plotBinnedTimeInTJ(savepath=savepath+os.sep, BatchID  = listOfNames[ii], BatchIDC =listOfNames[ii].replace(' ', '_'), show=show, binWidth=1)

        
def plotGradientTimeVs1oQ_Induvidual(listOfClassInstances,  listOfNames, savepath='CheckGradientTVs1oQ', show=False):
    if not os.path.exists(savepath): os.makedirs(savepath)
    for ii in range(len(listOfClassInstances)):
        listOfClassInstances[ii].plotTvs1oQ(savepath=savepath+os.sep,  BatchID  = listOfNames[ii], BatchIDC =listOfNames[ii].replace(' ', '_'), show=show)
    
def plotGeometricVsAccelerationTime(listOfClassInstances, listOfD0, listOfNames, savepath='CheckTimes', show=False):
    '''
    Plot the two times in T-Junction against flow rate for each capsule
    '''

    c=  listOfClassInstances[0].coloursForMarker()
     
    diff=[]
    for ii in range(len(listOfClassInstances)):
        fig = plt.figure(figsize=(8, 6), dpi=200,)
        ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
        ax2.set_yscale("log", nonposy='clip')
        size3p5=6
        #errorbar average3p5beforSTD
        plt.errorbar(listOfClassInstances[ii].volumFluxesList, listOfClassInstances[ii].aveTimeinTJ, yerr=listOfClassInstances[ii].aveTimeinTJSTD, linestyle='None',  marker='o', color = c[0], label='Acceleration Time $t_1$', markersize=size3p5) #
        plt.errorbar(listOfClassInstances[ii].volumFluxesList, listOfClassInstances[ii].aveGeoTimeinTJ, yerr=listOfClassInstances[ii].aveGeoTimeinTJSTD, linestyle='None',  marker='s', color = c[2], label='Geometric Time $t_2$', markersize=size3p5)
       
        sampleNum=len(listOfClassInstances[ii].SpeedMain)
        s2='Error based on standard deviation of sample \nNumber of data points = %d, $d_0$ = %.2f $mm$' %(sampleNum,  listOfD0[ii])
    
        xmin, xmax = plt.xlim()
        plt.xlim([xmin, xmax*1.05])
        xmin, xmax = plt.xlim()
        ymin, ymax = plt.ylim()
        ax2.text(xmin+xmax*0.05, 0.2, s2, fontsize=10)
        plt.title("Time vs Q -  " +listOfNames[ii])
        plt.xlabel("Volumn Flux [ml/min]")
        plt.ylabel("Time [s]")
        plt.legend(loc=2, fontsize=6)
        
        ax_inset=fig.add_axes([0.6,0.6,0.25,0.25])
        fs_sp=10
        y=[]
        for jj in range(len(listOfClassInstances[ii].aveTimeinTJ)):
            a = listOfClassInstances[ii].aveTimeinTJ[jj]
            g = listOfClassInstances[ii].aveGeoTimeinTJ[jj]
#            print('%.4f  %.4f  %.4f ' %(a, g, (a-g)/a))
            y.append(( a - g )/(a))
            diff.append(( a - g )/(a))
        
        y=np.array(y)
#        print(y)
        ax_inset.plot(listOfClassInstances[ii].volumFluxesList, y,color=c[1],label='Difference $(t_1 - t_2)/t_1$', linestyle='None', marker='d')
#        ax_inset.legend(fontsize=fs_sp)
        ax_inset.set_xlim([xmin, xmax]);    ax_inset.tick_params(axis='x', labelsize=fs_sp);         ax_inset.tick_params(axis='y', labelsize=fs_sp)
        plt.text(0.99, 0.01, SIGNATURE, fontsize = 4, horizontalalignment='right', verticalalignment='center', transform = ax2.transAxes, **HFONT)
        ax_inset.set_xlabel("Volumn Flux [ml/min]", fontsize=fs_sp)
        ax_inset.set_ylabel("% difference $(t_1 - t_2)/t_1$", fontsize=fs_sp)

        plt.show()

        if savepath != None:
            if not os.path.exists(savepath): os.makedirs(savepath)
            name=os.path.join(os.sep, "TimeVsQ_"+listOfNames[ii].replace(' ', '_')+ ".jpg")
            plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)
        
        if show:
            plt.show()
        else:
            plt.close()
    
    print('Average difference = %.2f' %(np.average(diff)*100))
    
def plotForceAgainstTimeGradinet(listOfClassInstances, listOfNames, force, compression, savepath='CheckForce', show=False):
    '''
    Plot the force at a given compression against the gradient of time in T-Junction
    versus 1 / Volumn Flux Q
    
    '''
    leng= len(listOfClassInstances)
    assert(leng <= 10)
    c =  listOfClassInstances[0].coloursForMarker(n=leng) 

    fig = plt.figure(figsize=(8, 6), dpi=200,)
    ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)

    size3p5=6
    #errorbar average3p5beforSTD
    for ii in range(len(listOfClassInstances)):
        plt.errorbar(force[ii], listOfClassInstances[ii].aveGradient1oQ, yerr=listOfClassInstances[ii].aveGradient1oQErr, linestyle='None',  marker='s', color = c[ii], label=listOfNames[ii], markersize=size3p5) #
    xmin, xmax = plt.xlim()
    plt.xlim([xmin, xmax*1.05])

    plt.title("Force against gradient Time vs 1/Q")
    plt.xlabel("Force at %d %% Compresion [mN]" %compression)
    plt.ylabel("Time Gradient in T-Junction")
    plt.legend(loc=2, fontsize=6)
    plt.show()
    plt.text(0.99, 0.01, SIGNATURE, fontsize = 4, horizontalalignment='right', verticalalignment='center', transform = ax2.transAxes, **HFONT)
    if savepath != None:
        if not os.path.exists(savepath): os.makedirs(savepath)
        name=os.path.join(os.sep, "ForceVsTime_"+listOfNames[ii].replace(' ', '_')+ ".jpg")
        plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)

    if show:
        plt.show()
    else:
        plt.close()

def compareGeoAndAccTime(listOfClassInstances, listOfNames, savepath='CheckGradientTVs1oQ', show=False):
    gradient1oQ=[]; gradient1oQErr=[]; gradient1oQR2=[]; gradient1oQAcc=[]; gradient1oQAccErr=[]; gradient1oQAccR2=[];
    for ii in range(len(listOfClassInstances)):
        gradient1oQt, gradient1oQErrt, gradient1oQR2t, gradient1oQAcct, gradient1oQAccErrt, gradient1oQAccR2t = listOfClassInstances[ii].differenceGeoAndAccTime(savepath=savepath+os.sep,  BatchID  = listOfNames[ii], show=show)
        gradient1oQ.append(gradient1oQt); gradient1oQErr.append(gradient1oQErrt); gradient1oQR2.append(gradient1oQR2t); gradient1oQAcc.append(gradient1oQAcct); gradient1oQAccErr.append(gradient1oQAccErrt); gradient1oQAccR2.append(gradient1oQAccR2t);
   
    c=  listOfClassInstances[0].coloursForMarker()
    fig = plt.figure(figsize=(8, 6), dpi=200)
    ax = fig.add_subplot(111)
    x = range(len(listOfClassInstances))
    
    plt.errorbar(x,gradient1oQ, yerr=gradient1oQErr, marker = "s", color=c[0], label='Geometric Time')
    plt.errorbar(x,gradient1oQAcc, yerr = gradient1oQAccErr, marker = "o", color=c[2], label='Acceleration Time')
    plt.legend(loc='best', fontsize=6) 
    plt.xticks(x, listOfNames, rotation=45)
    plt.text(0.99, 0.01, SIGNATURE, fontsize = 4, horizontalalignment='right', verticalalignment='center', transform = ax2.transAxes, **HFONT)
    plt.title("Difference T vs 1/Q gradient for accerlation versu geometric time", y=1.01)
    plt.ylabel("T vs 1/Q gradient")
    plt.tight_layout()
    plt.show()
    plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+'DifferenceTvs1oQGradient_timemeasure.png'), dpi=300)
    


def plotForceVsTime(listOfClassInstances, listOfNames, force,  compression, savepath='CheckForce', show=False):
    leng= len(listOfClassInstances)
    x = range(leng); t=[]; tstd=[]
    for ii in x:
        t.append(listOfClassInstances[ii].aveGeoTimeinTJ[-1])
        tstd.append(listOfClassInstances[ii].aveGeoTimeinTJSTD[-1])

    assert(leng <= 10)
    c =  listOfClassInstances[0].coloursForMarker(n=leng) 
    fig = plt.figure(figsize=(8, 6), dpi=200,); ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
    size3p5=6
    plt.errorbar(force, t, yerr=tstd, linestyle='None',  marker='s', color = c[ii], label='', markersize=size3p5) #    
    
    xmin, xmax = plt.xlim()
    plt.xlim([xmin, xmax*1.05])

    plt.title("Time in T-Junction at max flow versus Forze", y=1.01)
    plt.ylabel("Time in T-Junction (geometric) [s]")
    plt.xlabel("Force at %d %% Compresion [mN]" %compression)
    plt.legend(loc='best', fontsize=6);
    plt.text(0.99, 0.01, SIGNATURE, fontsize = 4, horizontalalignment='right', verticalalignment='center', transform = ax2.transAxes, **HFONT)
    if savepath != None:
        if not os.path.exists(savepath): os.makedirs(savepath)
        name=os.path.join(os.sep, "ForceVsTime.jpg")
        plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)

    if show: plt.show()
    else: plt.close()
    
def plotForceVsDeformationMain(listOfClassInstances, listOfNames, force,  compression, listd0, savepath='CheckForce', show=False):
    leng= len(listOfClassInstances)
    assert(leng <= 10)
    c =  listOfClassInstances[0].coloursForMarker(n=leng) 
    fig = plt.figure(figsize=(8, 6), dpi=200,); ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
    size3p5=6; markers=['s', 'o', 'h', '>', 'p', 'd', '<', '*', 'x', '+']
    for ii in range(leng):
        plt.errorbar(force[ii], listOfClassInstances[ii].aveD12Main[-1], yerr=listOfClassInstances[ii].aveD12MainSTD[-1], linestyle='None', marker = markers[ii], color = c[ii], label=listOfNames[ii] + ' d0 = %.1f' %listd0[ii], markersize=size3p5) #    
    
    xmin, xmax = plt.xlim()
    plt.xlim([xmin, xmax*1.05])

    plt.title("Deformation in Main Channel versus Force", y=1.01)
    plt.ylabel("Deformation $D_{12}$ at max $Q$")
    plt.xlabel("Force at %d %% Compresion [mN]" %compression)
    plt.legend(loc=2, fontsize=6);
    plt.text(0.99, 0.01, SIGNATURE, fontsize = 4, horizontalalignment='right', verticalalignment='center', transform = ax2.transAxes, **HFONT)
    if savepath != None:
        if not os.path.exists(savepath): os.makedirs(savepath)
        name=os.path.join(os.sep, "ForceVsD_Main.jpg")
        plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)

    if show: plt.show()
    else: plt.close()

def plotForceVsDeformationDaugther(listOfClassInstances, listOfNames, force,  compression, listd0, savepath='CheckForce', show=False):
    leng= len(listOfClassInstances)
    assert(leng <= 10)
    c =  listOfClassInstances[0].coloursForMarker(n=leng) 
    fig = plt.figure(figsize=(8, 6), dpi=200,); ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
    size3p5=6; markers=['s', 'o', 'h', '>', 'p', 'd', '<', '*', 'x', '+']
    for ii in range(leng):
        plt.errorbar(force[ii], listOfClassInstances[ii].aveD12Daugther[-1], yerr=listOfClassInstances[ii].aveD12DaugtherSTD[-1], linestyle='None', marker = markers[ii], color = c[ii], label=listOfNames[ii] + ' d0 = %.1f' %listd0[ii], markersize=size3p5) #    
    
    xmin, xmax = plt.xlim()
    plt.xlim([xmin, xmax*1.05])
    signature(ax2)
    plt.title("Deformation in Daugther Channel versus Force", y=1.01)
    plt.ylabel("Deformation $D_{12}$ at max $Q$")
    plt.xlabel("Force at %d %% Compresion [mN]" %compression)
    plt.legend(loc=2, fontsize=6);
    plt.text(0.99, 0.01, SIGNATURE, fontsize = 4, horizontalalignment='right', verticalalignment='center', transform = ax2.transAxes, **HFONT)
    if savepath != None:
        if not os.path.exists(savepath): os.makedirs(savepath)
        name=os.path.join(os.sep, "ForceVsD_Daugther.jpg")
        plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)

    if show: plt.show()
    else: plt.close()
    
def plotForceVsDeformationGradient(listOfClassInstances, listOfNames, force,  compression, listd0, savepath='CheckForce', show=False):
    leng= len(listOfClassInstances)
    assert(leng <= 10)
    c =  listOfClassInstances[0].coloursForMarker(n=leng) 
    fig = plt.figure(figsize=(8, 6), dpi=200,); ax2 = fig.add_subplot(111) #ax2.text(minVolumnFlux+maxVolumnFlux*0.1, ((2*minVolumnFlux*1000.0/60)/32.0), s2, fontsize=10)
    size3p5=6; markers=['s', 'o', 'h', '>', 'p', 'd', '<', '*', 'x', '+']
    for ii in range(leng):
        print('%s' %(listOfNames[ii]))
        plt.errorbar(force[ii], listOfClassInstances[ii].gradientD12Main, yerr=listOfClassInstances[ii].gradientD12MainErr, linestyle='None', marker = 'o', color = c[ii], label=listOfNames[ii] + ' d0 = %.1f Main' %listd0[ii], markersize=size3p5) # 
        plt.errorbar(force[ii], listOfClassInstances[ii].gradientD12Daugther, yerr=listOfClassInstances[ii].gradientD12DaugtherErr, linestyle='None', marker = 's', color = c[ii], label=listOfNames[ii] + ' d0 = %.1f Daugther' %listd0[ii], markersize=size3p5)
    
    xmin, xmax = plt.xlim()
    plt.xlim([xmin, xmax*1.05])
    signature(ax2)
    plt.title("Deformation Gradient versus Force", y=1.01)
    plt.ylabel("Deformation Gradient $D_{12}$ with $Q$")
    plt.xlabel("Force at %d %% Compresion [mN]" %compression)
    plt.legend(loc='best', fontsize=6, ncol=2);

    if savepath != None:
        if savepath != ''  and not os.path.exists(savepath): os.makedirs(savepath)
        name=os.path.join(os.sep, "ForceVsDGradient.jpg")
        plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)

    if show: plt.show()
    else: plt.close()
    
def checkProbabilityLeftRight(listOfClassInstances, listOfNames):
    '''
    Check probability of left, right distribution assuming T-Junction is perfect
    
    see http://math.stackexchange.com/questions/151810/probability-of-3-heads-in-10-coin-flips
    for binomial distribution used
    (nk)pk(1−p)n−k=(103)⋅(12)3⋅(12)7=15128
    '''    
    
    n= [] #number of trials
    k = [] #number of turns right
    p = [] #probability
    
    print('Trys \tTurned Right \tProbability')
    for inst in listOfClassInstances:
        n.append( len(inst.offCentre))
        k.append(len(inst.offCentreTurnedRight))
#        p.append( sp.special.binom(n[-1], k[-1]) * ptr**k[-1] * (1 - ptr)**(n[-1] - k[-1]))
        p.append(sp.stats.binom.pmf(k[-1], n[-1], 0.5))
        print('%d \t%d \t\t%.3f' %(n[-1], k[-1], p[-1]))
    
    return n, k, p

def STDofOffcentre(listOfClassInstances, listOfNames, listOfD0, nrCap=0, savepath=None, show=False):
    leng = len(listOfClassInstances)
    stdOffcentre=[]
    meanOffcentre=[]
    Offcentre=[]
    Offcentre2=[]
    for ii in range(leng):
        for jj in range(len(listOfClassInstances[ii].timeGeoInTJ)):
            if ii < nrCap:
                Offcentre.append(listOfClassInstances[ii].offCentre[jj]/listOfClassInstances[ii].pixelsPmm)
            else:
                Offcentre2.append(listOfClassInstances[ii].offCentre[jj]/listOfClassInstances[ii].pixelsPmm)
        stdOffcentre.append(np.std(listOfClassInstances[ii].offCentre/listOfClassInstances[ii].pixelsPmm, ddof=1))
        meanOffcentre.append(np.mean(listOfClassInstances[ii].offCentre)) #/listOfClassInstances[ii].pixelsPmm))
    std = np.std(Offcentre, ddof=1)
    std2 = np.std(Offcentre2, ddof=1)
    
    assert(leng <= 10)
    c=  listOfClassInstances[0].coloursForMarker(n=leng)
    markers=['o', 'h', '<', 'd', '*', 's', '^', 'p', '>', '8']
    
    fig = plt.figure(figsize=(8, 6), dpi=200)
    ax = fig.add_subplot(111)
    x = range(leng)
    
    plt.xticks(x, listOfNames, rotation=45)
    plt.ylabel('Unbiased Standard Deviation from Centerline [mm]')
    if nrCap != 0 :
        ax.plot(x[:nrCap],stdOffcentre[:nrCap],marker = '.', color='k', label='', markersize=1)
        ax.plot(x[nrCap:],stdOffcentre[nrCap:],marker = '.', color='k', label='', markersize=1)
    for ii in range(leng):
        plt.plot(x[ii],stdOffcentre[ii],marker = markers[ii], color=c[ii], label=listOfNames[ii] + ' $d_0 = $%.1f, $\\bar{x} = $ %.3f' %(listOfD0[ii], meanOffcentre[ii]))
    if nrCap != 0 :
        plt.text(0.4, 0.8, 'Capsule std = %.3f, Gel Beads std = %.3f \nBased on %d and %d data points \nAverage of average std %.3f and %.3f' %(std, std2, len(Offcentre), len(Offcentre2), np.mean(stdOffcentre[:nrCap]), np.mean(stdOffcentre[nrCap:])), fontsize = 8, horizontalalignment='left', verticalalignment='center', transform = ax.transAxes, **HFONT)
#    plt.legend(loc='best', fontsize=4)
    
    locs, labels =plt. xticks()
    ax2 = ax.twiny()
    plt.xticks(x, listOfD0)
    
    ymin, ymax = plt.ylim()
    plt.ylim([0.0, ymax])
    
#    ax.ylabel('Unbiased Standard Deviation from Centerline [mm]')
    plt.title("STD for Offcenter Distance", y=1.2)
    plt.tight_layout()
    plt.show()
    signature(ax)
    if savepath != None:
        if not os.path.exists(savepath) and savepath != "": 
            os.makedirs(savepath)
        if savepath != "":
            name=os.path.join(os.sep, "STDVariation.jpg")
        else:
            name = "STDVariation.png"
        plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)
    
    if show:
        plt.show()
    else:
        plt.close()

def STDofSpeed(listOfClassInstances, listOfNames, listOfD0, nrCap=0, savepath=None, show=False):
    leng = len(listOfClassInstances)
    stdSpeedM=[]
    stdSpeedD=[]

    for ii in range(leng):
        sM=[]
        sD= []
        for jj in range(len(listOfClassInstances[ii].timeGeoInTJ)):
            meanSpeed = ((2*listOfClassInstances[ii].volumFlux[jj]*1000.0/60)/32.0)
            sM.append(listOfClassInstances[ii].SpeedMain[jj]/(listOfClassInstances[ii].pixelsPmm*meanSpeed))
            sD.append(listOfClassInstances[ii].SpeedDaugther[jj]/(listOfClassInstances[ii].pixelsPmm*meanSpeed))
#            if ii < nrCap:
#                Offcentre.append(listOfClassInstances[ii].offCentre[jj]/listOfClassInstances[ii].pixelsPmm)
#            else:
#                Offcentre2.append(listOfClassInstances[ii].offCentre[jj]/listOfClassInstances[ii].pixelsPmm)
#        stdSpeedM.append(np.std(sM, ddof=1))
#        stdSpeedD.append(np.std(sD, ddof=1))
        stdSpeedM.append(np.mean((listOfClassInstances[ii].aveSpeedMainSTD)/(listOfClassInstances[ii].aveSpeedMain)))
        stdSpeedD.append(np.mean((listOfClassInstances[ii].aveSpeedDaugtherSTD)/(listOfClassInstances[ii].aveSpeedDaugther)))
    
    assert(leng <= 10)
    c=  listOfClassInstances[0].coloursForMarker(n=leng)
    markers=['o', 'h', '<', 'd', '*', 's', '^', 'p', '>', '8']
    
    fig = plt.figure(figsize=(8, 6), dpi=200)
    ax = fig.add_subplot(111)
    x = range(leng)
    
    plt.xticks(x, listOfNames, rotation=45)
    plt.ylabel('Unbiased Standard Deviation of Speed')
    if nrCap != 0 :
        ax.plot(x[:nrCap],stdSpeedM[:nrCap],marker = '.', color='k', label='', markersize=1)
        ax.plot(x[nrCap:],stdSpeedM[nrCap:],marker = '.', color='k', label='', markersize=1)
        ax.plot(x[:nrCap],stdSpeedD[:nrCap],marker = '.', color='k', linestyle = ':', label='', markersize=1)
        ax.plot(x[nrCap:],stdSpeedD[nrCap:],marker = '.', color='k', linestyle = ':', label='', markersize=1)
    for ii in range(leng):
        plt.plot(x[ii],stdSpeedM[ii],marker = markers[ii], color=c[ii], label=listOfNames[ii] + ' $d_0 = $%.1f' %(listOfD0[ii]))
        plt.plot(x[ii],stdSpeedD[ii],marker = markers[ii], color=c[ii])
    if nrCap != 0 :
        plt.text(0.2, 0.8, 'Main Channel Capsule std = %.3f, Gel Beads std = %.3f, difference = %.3f \nDaugther Channel Capsule std = %.3f, Gel Beads std = %.3f, difference = %.3f' %(np.mean(stdSpeedM[:nrCap]), np.mean(stdSpeedM[nrCap:]), np.mean(stdSpeedM[:nrCap])- np.mean(stdSpeedM[nrCap:])  ,np.mean(stdSpeedD[:nrCap]), np.mean(stdSpeedD[nrCap:]),np.mean(stdSpeedD[:nrCap]) - np.mean(stdSpeedD[nrCap:])), fontsize = 8, horizontalalignment='left', verticalalignment='center', transform = ax.transAxes, **HFONT)
#    plt.legend(loc='best', fontsize=4)
    
    locs, labels =plt. xticks()
    ax2 = ax.twiny()
    plt.xticks(x, listOfD0)
    
    ymin, ymax = plt.ylim()
    plt.ylim([0.0, ymax])
    
#    ax.ylabel('Unbiased Standard Deviation from Centerline [mm]')
    plt.title("STD of Speed", y=1.2)
    plt.tight_layout()
    plt.show()
    signature(ax)
    if savepath != None:
        if not os.path.exists(savepath) and savepath != "": 
            os.makedirs(savepath)
        if savepath != "":
            name=os.path.join(os.sep, "STDspeed.png")
        else:
            name = "STDspeed.png"
        plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)
    
    if show:
        plt.show()
    else:
        plt.close()
        
def STDofTime(listOfClassInstances, listOfNames, listOfD0, nrCap=0, savepath=None, show=False):
    leng = len(listOfClassInstances)
    stdTime=[]

    for ii in range(leng):
        stdTime.append(np.mean((listOfClassInstances[ii].aveGeoTimeinTJSTD)/(listOfClassInstances[ii].aveGeoTimeinTJ)))
    
    assert(leng <= 10)
    c=  listOfClassInstances[0].coloursForMarker(n=leng)
    markers=['o', 'h', '<', 'd', '*', 's', '^', 'p', '>', '8']
    
    fig = plt.figure(figsize=(8, 6), dpi=200)
    ax = fig.add_subplot(111)
    x = range(leng)
    
    plt.xticks(x, listOfNames, rotation=45)
    plt.ylabel('Unbiased Standard Deviation of Time')
    if nrCap != 0 :
        ax.plot(x[:nrCap],stdTime[:nrCap],marker = '.', color='k', label='', markersize=1)
        ax.plot(x[nrCap:],stdTime[nrCap:],marker = '.', color='k', label='', markersize=1)
    for ii in range(leng):
        plt.plot(x[ii],stdTime[ii],marker = markers[ii], color=c[ii], label=listOfNames[ii] + ' $d_0 = $%.1f' %(listOfD0[ii]))
        plt.plot(x[ii],stdTime[ii],marker = markers[ii], color=c[ii])
    if nrCap != 0 :
        plt.text(0.2, 0.8, 'Capsule std = %.3f, Gel Beads std = %.3f, difference = %.3f' %(np.mean(stdTime[:nrCap]), np.mean(stdTime[nrCap:]), np.mean(stdTime[:nrCap])- np.mean(stdTime[nrCap:])), fontsize = 8, horizontalalignment='left', verticalalignment='center', transform = ax.transAxes, **HFONT)
#    plt.legend(loc='best', fontsize=4)
    
    locs, labels =plt. xticks()
    ax2 = ax.twiny()
    plt.xticks(x, listOfD0)
    
    ymin, ymax = plt.ylim()
    plt.ylim([0.0, ymax])
#    ax.ylabel('Unbiased Standard Deviation from Centerline [mm]')
    plt.title("STD of Time in T-Junction", y=1.2)
    plt.tight_layout()
    plt.show()
    signature(ax)
    if savepath != None:
        if not os.path.exists(savepath) and savepath != "": 
            os.makedirs(savepath)
        if savepath != "":
            name=os.path.join(os.sep, "STDinTime.png")
        else:
            name = "STDinTime.png"
        plt.savefig(listOfClassInstances[0].makeSaveNameSafe(savepath+name), dpi=300)

    if show:
        plt.show()
    else:
        plt.close()
    
def signature(ax):
    ax.text(1.01, -0.05, SIGNATURE, fontsize = 3, horizontalalignment='left', verticalalignment='center', transform = ax.transAxes, **HFONT)
    
        
        