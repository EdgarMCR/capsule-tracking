# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:00:53 2015

@author: Edgar
"""

from __future__ import absolute_import, division, print_function

import sys
import track_capsule_TJ as tr 


def runTrackingScriptOnDirectory(directory, d0, pPmm, rotation, yTop, yBottom, xRight, xLeft, twoCapsules=0, OpenCV3=1):
    print('Starting function "runTrackingScriptOnDirectory"')
    
    fpss=[10, 11, 20, 25, 30, 40, 50, 60, 70, 80, 100, 120, 140]
    #fpss=[6, 10, 14, 20, 25, 30, 35, 40]
    
    problems1=[]
    for fps in fpss:
        try:
            backPath = directory +'Background'+str(fps)+'FPS.png'
            a = tr.userInputClass(directory, '', d0, pPmm, rotation, fps, yTop, yBottom, xRight, xLeft, backPath)
            tr.runOneFPS(parameters=a, FPS=fps, twoCapsules=twoCapsules, OpenCV3=OpenCV3)                
            problems1.append("%d Completed! " %fps)
        except:
            problems1.append("\t\t%d didn't complete" %fps)
    
    print(problems1)
    
if __name__ == '__main__':
    print(sys.argv, end="")
    print('\tlen(sys.argv) = %d' %len(sys.argv))
    if len(sys.argv) < 10:
        runTrackingScriptOnDirectory(directory=sys.argv[1], d0=float(sys.argv[2]), pPmm=float(sys.argv[3]), rotation=float(sys.argv[4]), yTop=int(float(sys.argv[5])), yBottom=int(float(sys.argv[6])), xRight=int(float(sys.argv[7])), xLeft=int(float(sys.argv[8])))
    elif len(sys.argv) == 10:
        runTrackingScriptOnDirectory(directory=sys.argv[1], d0=float(sys.argv[2]), pPmm=float(sys.argv[3]), rotation=float(sys.argv[4]), yTop=int(float(sys.argv[5])), yBottom=int(float(sys.argv[6])), xRight=int(float(sys.argv[7])), xLeft=int(float(sys.argv[8])), twoCapsules=float(sys.argv[9]))
    else:
        runTrackingScriptOnDirectory(directory=sys.argv[1], d0=float(sys.argv[2]), pPmm=float(sys.argv[3]), rotation=float(sys.argv[4]), yTop=int(float(sys.argv[5])), yBottom=int(float(sys.argv[6])), xRight=int(float(sys.argv[7])), xLeft=int(float(sys.argv[8])), twoCapsules=float(sys.argv[9]), OpenCV3=float(sys.argv[10]))