def getData(path):
    file_object = open(path)
    try:
        all_the_text = file_object.readlines()
    finally:
        file_object.close()
    return all_the_text

trainData =  getData('../data/pre/train.csv')

# print trainData
file_object = open('../output/NCUsers.csv', 'w+')

file_object.write('label,clickTime,conversionTime,creativeID,userID,positionID,connectionType,telecomsOperator' + '\n')

for i in xrange(1, len(trainData)):
    line = trainData[i].split(',')
    if int(line[0]) == 0:
    	file_object.write(','.join(line))

file_object.close()