from prepare import *
trainingFile = './data/pre/train.csv'
testingFile = './data/pre/test.csv'
outputTrainingFile = './data/xgb/train.csv'
alldata = prepare()


def getData(path):
    file_object = open(path)
    try:
        all_the_text = file_object.readlines()
    finally:
        file_object.close()
    return all_the_text

def getXYorID(line):
    line_arr = line.split(',')
    trainLine = []
    trainLine.extend(line_arr[0:3])
    trainLine.extend(line_arr[6:8])
    trainLine.extend(alldata.getAll(line_arr[3], line_arr[4], line_arr[5]))
    # print ",".join(map(eval, trainLine[3:]))
    return map(eval, trainLine[3:]), str(trainLine[0])


trainData = getData(trainingFile)
file_object = open(outputTrainingFile, 'w+')
file_object.write('connectionType,telecomsOperator,adID,camgaignID,advertiserID,appID,appPlatform,age,gender,education,marriageStatus,haveBaby,hometown,residence,sitesetID,positionType,userFeature,label' + '\n')
for i in xrange(1, len(trainData)):
    x,y= getXYorID(trainData[i])
    file_object.write(str(x)[1:-1])
    file_object.write(',')
    file_object.write(y+'\n')
file_object.close()
