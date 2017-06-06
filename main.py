# -*- coding: utf-8 -*-
import os, sys, random
import numpy
import pylab
from PIL import Image
from math import *
import time


import packages.conv as conv
import packages.rotation as rot
import packages.ml_alg as ml




def main():
    # stacks = ['/home/axel/Documents/DATASET/final_model_data/t2_star_0',
    #         '/home/axel/Documents/DATASET/final_model_data/t2_star_1',
    #         '/home/axel/Documents/DATASET/final_model_data/t2_star_2',
    #         '/home/axel/Documents/DATASET/final_model_data/Thumbnail',
    #         '/home/axel/Documents/DATASET/final_model_data/mouse_kidney',
    #         '/home/axel/Documents/DATASET/final_model_data/kidney_2'
    #         ]

    vec_files = [
        '/home/axel/Documents/DATASET/final_model_data/t2_star_0/png/resized/vecImg.csv',
        '/home/axel/Documents/DATASET/final_model_data/t2_star_1/png/resized/vecImg.csv',
        '/home/axel/Documents/DATASET/final_model_data/t2_star_2/png/resized/vecImg.csv',
        '/home/axel/Documents/DATASET/final_model_data/Thumbnail/resized/vecImg.csv',
        '/home/axel/Documents/DATASET/final_model_data/mouse_kidney/png/resized/vecImg.csv',
        '/home/axel/Documents/DATASET/final_model_data/kidney_2/png/resized/vecImg.csv'
    ]

    rot_files = [
        '/home/axel/Documents/DATASET/final_model_data/t2_star_0/png/resized/rotations.csv',
        '/home/axel/Documents/DATASET/final_model_data/t2_star_1/png/resized/rotations.csv',
        '/home/axel/Documents/DATASET/final_model_data/t2_star_2/png/resized/rotations.csv',
        '/home/axel/Documents/DATASET/final_model_data/Thumbnail/resized/rotations.csv',
        '/home/axel/Documents/DATASET/final_model_data/mouse_kidney/png/resized/rotations.csv',
        '/home/axel/Documents/DATASET/final_model_data/kidney_2/png/resized/rotations.csv'
    ]

    # vec_files = []
    #
    # rot_files = []
    # largerSize = rot.getLargerSize(stacks)
    #
    # for stack in stacks :
    #     print stack
    #     pngStack = rot.processDir(stack)
    #     resizedStack = rot.resize(pngStack, largerSize)
    #     rotFile = rot.create_pairs(resizedStack)
    #     rot_files.append(rotFile)
    #
    #     vecFile = conv.fc(resizedStack)
    #     vec_files.append(vecFile)
    #     print ('vecFile = ' + vecFile)



    stop, training_data, training_labels, test_data, test_labels = ml.arrange_data(vec_files, rot_files)
    if stop :
        return 0
    else :
        res = ml.learn(training_data, training_labels, test_data, test_labels)


    return 0

if __name__ == '__main__':
    main()
