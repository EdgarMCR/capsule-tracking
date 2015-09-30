# -*- coding: utf-8 -*-
"""
Read tif image sequence and save as png
Created on Wed Apr 08 12:04:01 2015

@author: Edgar
"""

from PIL import Image
import os.path

loadpath='C:\\Users\\Edgar\\Desktop\\Experiments20032015\\08042015\\PlasticRed-3mm-080415-30fps-10mlPmin-3.tif'

im = Image.open(loadpath)
im.show()
im.save("img1.png","PNG")