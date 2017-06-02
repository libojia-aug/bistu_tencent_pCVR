from prepare import *
import os

# time pypy-2.4 -u runmodel.py | tee output_0.txt
from FTRL import *
import random
from math import log

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
# , '0', '3\n']
# label,clickTime,conversionTime,connectionType,telecomsOperator
#,adID,camgaignID,advertiserID,appID,appPlatform
#,age,gender,education,marriageStatus,haveBaby,hometown,residence
#,sitesetID,positionType,

# for testing data
#['1', '-1', '310000', '1', '3\n'
# , '1166', '430', '80', '14', '2\n'
# , '29', '2', '1', '0', '1', '605', '605\n'
# , '0', '1\n']
# instanceID,label,clickTime,connectionType,telecomsOperator
#,adID,camgaignID,advertiserID,appID,appPlatform
#,age,gender,education,marriageStatus,haveBaby,hometown,residence
#,sitesetID,positionType,


def getXYorID(line):
    line_arr = line.split(',')
    trainLine = []
    trainLine.extend(line_arr[0:3])
    trainLine.extend(line_arr[6:8])
    trainLine.extend(alldata.getAll(line_arr[3], line_arr[4], line_arr[5]))
    return map(eval, trainLine[3:]), int(trainLine[0])


#### RANDOM SEED ####
random.seed(5)  # seed random variable for reproducibility
#####################

####
start = datetime.now()

####################
#### PARAMETERS ####
####################
reportFrequency = 10000
trainingFile = './data/pre/train.csv'
testingFile = './data/pre/test.csv'
os.makedirs('./output/' + str(start))
outputTestingFile = './output/' + str(start) + '/submission_.csv'
w_outfile = './output/' + str(start) + '/param.w.txt'
w_fm_outfile = './output/' + str(start) + '/param.w_fm.txt'

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

n_epochs = 1


# initialize a FM learner
learner = FM_FTRL_machine(fm_dim, fm_initDev, L1, L2, L1_fm,
                          L2_fm, D, alpha, beta, alpha_fm=alpha_fm, beta_fm=beta_fm)

print("Start Training:")
for e in range(n_epochs):

    # if it is the first epoch, then don't use L1_fm or L2_fm
    if e == 0:
        learner.L1_fm = 0.
        learner.L2_fm = 0.
    else:
        learner.L1_fm = L1_fm
        learner.L2_fm = L2_fm

    cvLoss = 0.
    cvCount = 0.
    trainData = getData(trainingFile)
    for i in xrange(1, len(trainData)):
        x, y = getXYorID(trainData[i])
        p = learner.predict(x)
        loss = logLoss(p, y)
        learner.update(x, p, y)
        if i % reportFrequency == 0:
            print("Epoch %d\tcount: %d\tProgressive Loss: %f" % (e, i, loss))

    file_object = open(outputTestingFile, 'w+')
    file_object.write('instanceID, prob' + '\n')
    testData = getData(testingFile)
    for j in xrange(1, len(testData)):
        x, instanceID = getXYorID(testData[j])
        p = learner.predict(x)
        file_object.write("%i %f\n" % (instanceID, p))
        if i % reportFrequency == 0:
            print("Epoch %d\tcount: %d" % (e, i))
    file_object.close()
    print("Epoch %d finished.\t elapsed time: %s" %
          (e, str(datetime.now() - start)))

# save the weights
learner.write_w(w_outfile)
learner.write_w_fm(w_fm_outfile)
