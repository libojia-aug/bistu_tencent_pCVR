from prepare import *
import os

# time pypy-2.4 -u runmodel.py | tee output_0.txt
from FTRL import *
import random
from math import log

import sys
alldata = prepare()


def getData(path):
    file_object = open(path)
    try:
        all_the_text = file_object.readlines()
    finally:
        file_object.close()
    return all_the_text

# for training data
#['0', '170000', '', '1', '1\n'
# , '1321', '83', '10', '434', '1\n'
# , '25', '2', '1', '3', '1', '0', '1301\n'
# , '0', '3\n'
# , '16151.1753589\n']
# label,clickTime,conversionTime,connectionType,telecomsOperator
#,adID,camgaignID,advertiserID,appID,appPlatform
#,age,gender,education,marriageStatus,haveBaby,hometown,residence
#,sitesetID,positionType,
#,userFeature

# for testing data
#['1', '-1', '310000', '1', '3\n'
# , '1166', '430', '80', '14', '2\n'
# , '29', '2', '1', '0', '1', '605', '605\n'
# , '0', '1\n'
# , 0]
# instanceID,label,clickTime,connectionType,telecomsOperator
#,adID,camgaignID,advertiserID,appID,appPlatform
#,age,gender,education,marriageStatus,haveBaby,hometown,residence
#,sitesetID,positionType,
#,userFeature


def getXYorID(line):
    line_arr = line.split(',')
    trainLine = []
    trainLine.extend(line_arr[0:3])
    trainLine.extend(line_arr[6:8])
    trainLine.extend(alldata.getAll(line_arr[3], line_arr[4], line_arr[5]))
    # print trainLine
    # sys.exit()
    # print map(eval, trainLine[3:])
    return map(eval, trainLine[3:]), int(trainLine[0])


#### RANDOM SEED ####
random.seed(5)  # seed random variable for reproducibility
#####################



####################
#### PARAMETERS ####
####################
reportFrequency = 1000
trainingFile = './data/pre/train.csv'
testingFile = './data/pre/test.csv'

fm_dim = 4
fm_initDev = .01

alpha = .1
beta = 1.

alpha_fm = .01
beta_fm = 1.

p_D = 22
D = 2 ** p_D

L1 = 1.0
L2 = .1
L1_fm = 2.0
L2_fm = 3.0

dropoutRate = 0.8

n_epochs = 1


# initialize a FM learner
learner = FM_FTRL_machine(fm_dim, fm_initDev, L1, L2, L1_fm, L2_fm, D, alpha, beta, alpha_fm = alpha_fm, beta_fm = beta_fm, dropoutRate = dropoutRate)


print("Start Training:")
for e in range(n_epochs):
    ####
    start = datetime.now()
    os.makedirs('./output/' + str(start))
    outputTestingFile = './output/' + str(start) + '/submission.csv'
    w_outfile = './output/' + str(start) + '/param.w.txt'
    w_fm_outfile = './output/' + str(start) + '/param.w_fm.txt'
    # if it is the first epoch, then don't use L1_fm or L2_fm
    if e == 0:
        learner.L1_fm = 0.
        learner.L2_fm = 0.
    else:
        learner.L1_fm = L1_fm
        learner.L2_fm = L2_fm

    loss_a = 0
    trainData = getData(trainingFile)
    for i in xrange(1, len(trainData)):
        x, y = getXYorID(trainData[i])
        p = learner.dropoutThenPredict(x)
        loss = logLoss(p, y)

        if i > 90000:
            loss_a +=loss
        else:
            learner.update(x, p, y)
        if i % reportFrequency == 0:
            print("Epoch %d\tcount: %d\tProgressive Loss: %f" % (e, i, loss))
        if i % 100000 == 0:
            print("Progressive Loss: %f" % (loss_a/10000))
            sys.exit()

    file_object = open(outputTestingFile, 'w+')
    file_object.write('instanceID, prob' + '\n')
    testData = getData(testingFile)
    for j in xrange(1, len(testData)):
        x, instanceID = getXYorID(testData[j])
        p = learner.predictWithDroppedOutModel(x)
        file_object.write("%i,%f\n" % (instanceID, p))
        if j % reportFrequency == 0:
            print("Epoch %d\tcount: %d" % (e, j))
    file_object.close()
    print("Epoch %d finished.\t elapsed time: %s" %
          (e, str(datetime.now() - start)))

# save the weights
learner.write_w(w_outfile)
learner.write_w_fm(w_fm_outfile)
