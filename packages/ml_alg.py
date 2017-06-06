import numpy as np
import random
from sklearn import random_projection
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from sklearn import neural_network
import csv
import os
import time
import ast
import matplotlib.pyplot as plt
import pandas as pd

def arrange_data(vec_files, rot_files):
    vecList = []

    all_vec = '/home/axel/Documents/DATASET/final_model_data/vecShuf.csv'
    for vecFile in vec_files :
        tmpList = pd.read_csv(vecFile,header=0)
        for index, row in tmpList.iterrows():
            vecList.append(row.tolist())

    print 'VECLIST SIZE : ' + str(len(vecList))

    failed = []
    j = 0
    for i in range (1,len(vecList)):
        if len(vecList[i]) == len(vecList[i-1]):
            pass
        else :
            print 'OOOOOUUUUUUPS !'
            failed.append(i)
            j+=1
    print str(j) + ' Times len mismatch'
    print failed

    rot_list = []

    all_rot = '/home/axel/Documents/DATASET/final_model_data/rotShuf.csv'

    for rotFile in rot_files :
        tmpList = pd.read_csv(rotFile,header=0)
        for index, row in tmpList.iterrows():
            rot_list.append(row.tolist()[0])

    print 'ROT LIST SIZE : ' + str(len(rot_list))

    shuf = '/home/axel/Documents/DATASET/final_model_data/rotShuf.csv'
    if len(vecList) == len(rot_list) :
            index_shuf = range(len(vecList))
    else :
        print 'DATA SIZE AND LABEL SIZE ARE NOT THE SAME'
        stop = True
        return stop

    random.shuffle(index_shuf)

    dataShuf = []
    labelShuf = []

    training_size = 70*len(vecList)//100

    for i in index_shuf:
        dataShuf.append(vecList[i])
        labelShuf.append(rot_list[i])

    shufDf = pd.DataFrame(index_shuf)
    vecDf = pd.DataFrame(dataShuf)
    rotDf = pd.DataFrame(labelShuf)

    shufDf.to_csv(shuf, index=False, header=False)
    vecDf.to_csv(all_vec, index=False, header=False)
    rotDf.to_csv(all_rot, index=False, header=False)

    training_data = dataShuf[:training_size]
    training_labels = labelShuf[:training_size]
    test_data = dataShuf[training_size:]
    test_labels = labelShuf[training_size:]

    print 'Len of test_labels : ' + str(len(test_labels))

    test_pred_df = pd.DataFrame(test_labels)
    test_pred_df.to_csv('/home/axel/Documents/DATASET/final_model_data/pred_val.csv', index=False, header=False)

    stop = False

    return stop, training_data, training_labels, test_data, test_labels

def learn(training_data, training_labels, test_data, test_labels):
    ##################### SUPPORT VECTOR REGRESSION #####################
    svr_res_lin = []
    svr_res_poly =[]

    #svr_rbf = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_lin = svm.SVR(kernel='linear', C=1e3)
    svr_poly = svm.SVR(kernel='poly', C=1e3, degree=2)

    #y_rbf = svr_rbf.fit(inputDataTest, inputMetaDataTest)

    lin_Time = time.time()
    y_lin = svr_lin.fit(training_data, training_labels)
    print("--- %s seconds --- Linear training Time" % (time.time() - lin_Time))
    poly_Time = time.time()
    y_poly = svr_poly.fit(training_data, training_labels)
    print("--- %s seconds --- Poly training Time" % (time.time() - poly_Time))
    ################## TRAINING DATA ##################
    svr_linTrain = y_lin.score(training_data, training_labels)
    svr_polyTrain = y_poly.score(training_data, training_labels)
    print "svr_linTrain = " + str(svr_linTrain)
    print "svr_polyTrain = " + str(svr_polyTrain)


    #################### TEST DATA ####################
    #LINEAR SVR
    svr_lin = y_lin.score(test_data, test_labels)
    print "svr_linTest = " + str(svr_lin)
    svr_res_lin.append(svr_lin)

    #POLY SVR
    svr_poly = y_poly.score(test_data, test_labels)
    print "svr_polyTest = " + str(svr_poly)
    svr_res_poly.append(svr_poly)

    ############ MAKE AND SAVE PREDICTION ############
    lin_pred = y_lin.predict(test_data)
    poly_pred = y_poly.predict(test_data)

    lin_err = 0
    for z in range(len(test_labels)):
        lin_err += abs(lin_pred[z]-test_labels[z])
    lin_err = lin_err/len(test_labels)
    print ' Linear SVR error : ' + str(lin_err)

    poly_err = 0
    for z in range(len(test_labels)):
        poly_err += abs(poly_pred[z]-test_labels[z])
    poly_err = poly_err/len(test_labels)
    print ' Poly SVR error : ' + str(poly_err)

    lin_pred_df = pd.DataFrame(lin_pred)
    poly_pred_df = pd.DataFrame(poly_pred)

    lin_pred_df.to_csv('/home/axel/Documents/Final_res/lin_pred.csv', index=False, header=False)
    poly_pred_df.to_csv('/home/axel/Documents/Final_res/poly_pred.csv', index=False, header=False)

    ###################### RANDOM FOREST REGRESSOR ######################
    rfr_res=[]
    rfr_iter = []
    rfr_iter_val = []
    x = [10, 50, 100]
    for j in x :

        nb_estim = j
        # RandomForestRegressor
        rgs = RandomForestRegressor(n_estimators=nb_estim)

        forestTime = time.time()
        rgs = rgs.fit(training_data, training_labels)
        print("--- %s seconds --- RFR Training Time with %d estimators" %((time.time() - forestTime),j))

        resTrain = rgs.score(training_data, training_labels)
        print "TRAIN results with RandomForestRegressor : " + str(resTrain)

        print "estimators :" + str(nb_estim)
        res = rgs.score(test_data, test_labels)
        rfr_iter.append(res)
        print "TEST results with RandomForestRegressor : " + str(res)

        rfr_pred = rgs.predict(test_data)

        rfr_pred_df = pd.DataFrame(rfr_pred)

        rfr_pred_path = '/home/axel/Documents/Final_res/rfr_pred_' + str(j) + '.csv'

        rfr_pred_df.to_csv(rfr_pred_path, index=False, header=False)

        rfr_err = 0
        for z in range(len(test_labels)):
            rfr_err += abs(rfr_pred[z]-test_labels[z])
        rfr_err = rfr_err/len(test_labels)
        print ' RFR error : ' + str(rfr_err) + 'With ' + str(j) + 'estimators'

    rfr_res.append(rfr_iter)
    # rfr_val.append(rfr_iter_val)
    #####################################################################

    ##################### NEURAL NETWORK REGRESSION #####################
    hd_lrs = [100,200,300]

    nnr_res =[]
    nnr_iter = []
    for h in hd_lrs :

        nnr = neural_network.MLPRegressor(hidden_layer_sizes=h,activation='identity',solver='adam')

        NNRTime = time.time()
        nnr = nnr.fit(training_data, training_labels)
        print("--- %s seconds --- NNR Training Time with %d estimators" %((time.time() - NNRTime),h))

        resVal = nnr.score(training_data, training_labels)

        print "TRAIN results with NeuralNetworkRegressor : " + str(resVal)
        res = nnr.score(test_data, test_labels)

        nnr_pred = nnr.predict(test_data)

        nnr_pred_df = pd.DataFrame(nnr_pred)

        nnr_pred_path = '/home/axel/Documents/Final_res/nnr_pred_' + str(h) + '.csv'

        rfr_pred_df.to_csv(rfr_pred_path, index=False, header=False)

        print "TEST results with NeuralNetworkRegressor : " + str(res)
        nnr_iter.append(res)

        nnr_err = 0
        for z in range(len(test_labels)):
            nnr_err += abs(nnr_pred[z]-test_labels[z])
        nnr_err = nnr_err/len(test_labels)
        print ' NNR error : ' + str(nnr_err) + 'With hidden layers of size :' + str(h)

    nnr_res.append(nnr_iter)

    return 0
