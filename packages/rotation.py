# -*- coding: utf-8 -*-
import os, sys
import numpy
from PIL import Image
import shutil
from math import *
import glob
import csv
import pandas as pd


#Check if first file of a directory is tif or not
def processDir(stackPath) :
    print stackPath

    for root, dirs, files in os.walk(stackPath, topdown=True):
        for name in files:
            #print name
            if name.endswith('tif'):
                print 'TEST'
                stackIsTif = True
                break
            else :
                print 'File tested : ' + str(name)
                stackIsTif = False
                break
        break

    #If stackIsTif convert to PNG
    if stackIsTif :
        print"Let's convert stack to PNG"
        stackPath = tifToPng(stackPath)
    else :
        print"We can now resize the stack"
        #stackPath = os.path.join(stackPath, 'png')
        print stackPath
    return stackPath

#Create a png copy of images of a stack and return the path of the new stack
def tifToPng(directory):
    print" Working in : " + directory + " directory"
    #Create new directory to store the new png images
    new_dir = os.path.join(directory,'png')
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    #For each image of the stack, create a png copy and save it in the new directory
    for fileName in os.listdir(directory) :
        imgPath = os.path.join(directory,fileName)
        if not os.path.isdir(imgPath) and (imgPath.endswith('.tif')):
            with Image.open(imgPath) as im:
                finalPath = os.path.join(new_dir,fileName)
                pre, ext = os.path.splitext(finalPath)
                finalPath = finalPath = pre + '.png'
                im.mode='I'
                im.point(lambda i:i*(1./256)).convert('L').save(finalPath)
        else :
            filePath = os.path.join(directory,fileName)
    return new_dir


#Check all stacks and get the larger size of image to resize other stacks
def getLargerSize(stacks):
    largerSize = 0
    for stack in stacks:
        for root, dirs, files in os.walk(stack, topdown=True):
            print 'PASS IN LOOP'
            for name in files:
                print name
                imgPath = os.path.join(stack, name)
                with Image.open(imgPath) as im:
                    if im.size[0] > im.size[1] :
                        if im.size[0] > largerSize :
                            largerSize = im.size[0]
                            break
                        else :
                            break
                    else :
                        if im.size[1] > largerSize :
                            largerSize = im.size[1]
                            break
                        else :
                            break
            break

    return largerSize


# Resize the stack such as rotations don't crop the original image
def resize(stackPath, largerSize):
    #First check if stack is already resized
    #The stack path is supposed to only contain images (as files)
    for root, dirs, files in os.walk(stackPath, topdown=True):
        for name in files:
            testPath = os.path.join(stackPath,name)
            pre, ext = os.path.splitext(testPath)
            if pre.endswith('resized'):
                resized = True
                break
            else :
                resized = False
                break
        break

    if not resized :
        print'Start resizing stack'
        #Create a new directory to store resized images
        new_dir = os.path.join(stackPath,'resized')
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        #Resize each image and save it in the new directory
        for fileName in os.listdir(stackPath) :
            filePath = os.path.join(stackPath,fileName)
            if not os.path.isdir(filePath) and fileName.endswith('.png') :
                with Image.open(filePath) as im:
                    # if im.size[0] > im.size[1] :
                    #     newSize = im.size[0]
                    # else :
                    #     newSize = im.size[1]

                    diago = int(round(sqrt(2)*largerSize))
                    new_size = (diago,diago)

                    new_im = Image.new("L", new_size)
                    new_im.paste(im,((new_size[0]-im.size[0])/2,(new_size[1]-im.size[1])/2))

                    newFileName = os.path.join(new_dir,fileName)
                    pre, ext = os.path.splitext(newFileName)
                    newFileName = pre + '_resized' + ext
                    new_im.save(newFileName)

            else :
                print" WARNING " +str(filePath) + " does not exist or is not a png image !!"
        print 'Ready to rotate'
        return new_dir
    else :
        print'This stack is already resized, we can rotate it'
        return stackPath

def create_pairs(stack):
    print ' Start creating rotated pairs'
    i=0
    # angleSign = 1
    stackPNG = os.path.join(stack, '*.png')
    filesList = glob.glob(stackPNG)
    randomArray = numpy.random.uniform(0,720,len(filesList))
    #print randomArray
    rotations = []
    new_dir = os.path.join(stack,str(i))
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    for pic in filesList :
        if i==0 :
            with Image.open(pic) as im :
                ext = str(i)+'.png'
                newImgPath = os.path.join(new_dir,ext)
                #print newImgPath
                r = randomArray[i]
                angle = (-90)+(180*r/720)
                #print angle
                newImg = im.rotate(angle)
                newImg.save(newImgPath)
                rotations.append(angle)
        else :
            prev_dir = new_dir
            new_dir = os.path.join(stack,str(i))
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            with Image.open(pic) as im :
                ext = str(i)+'.png'
                newImgPath = os.path.join(new_dir,ext)
                newImgPrevPath = os.path.join(prev_dir,ext)
                print newImgPath
                r = randomArray[i]
                angle = (-90)+(180*r/720)
                #print angle
                newImg = im.rotate(angle)
                newImg.save(newImgPath)
                newImg.save(newImgPrevPath)
                rotations.append(angle)
        i+=1
    pairsRot = []
    for j in range(1,len(rotations)):
        rot = rotations[j]-rotations[j-1]
        pairsRot.append(rot)
    #print pairsRot
    rotFile = os.path.join(stack,'rotations.csv')
    pairsRotDf = pd.DataFrame(pairsRot)
    pairsRotDf.to_csv(rotFile, index=False, header=False)

    return rotFile
