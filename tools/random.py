import numpy as np


def r():
    return np.random.randn() + 0.0248729973479

file_object = open('../output/submission-random.csv', 'w')

file_object.write('instanceID, prob' + '\n')

for i in xrange(1, 338490):
    p = -1
    while p < 0 or p > 1:
        p = r()
    file_object.write(str(i) + ',' + str(p) + '\n')

file_object.close()
