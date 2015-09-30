# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 20:26:56 2015

@author: mbbxkeh2
"""

from __future__ import absolute_import, division, print_function
import numpy as np
import track_capsule_TJ_v0p10 as tr

#To run script on a file, change path and run    
#path='/media/magda/ed/Capsules/Batch120415-002/Capsule#1/Batch120415-002-#1-130415-10mlPmin-2/'
directory = 'M:\\EdgarHaener\\Capsules\\Batch040615-002\\T-Junction\\Capsule#1\\'
path=directory + 'Batch040615-002-#1-1S-5kcSt-70FPS-35mlPmin-8\\'

#path='M:\\EdgarHaener\\Capsules\\Batch010615-001\\T-Junction\\Capsule#1\\Batch010615-001_#1-030615-5kcSt-1S-10FPS-5mlPmin-1\\Test\\'
tr.find_max_extend(path, d0=3.8, pPmm=22.2, constantFrequency=True, rotate=-0.3, plot=False, threshold=130, printDebugInfo=False)