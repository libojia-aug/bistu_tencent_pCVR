
file_object = open('../data/pre/train.csv')
try:
    all_the_text = file_object.readlines()
finally:
    file_object.close()

print len(all_the_text)

count = 0
for i in xrange(1, len(all_the_text)):
    line_arr = all_the_text[i].split(',')
    # print line_arr[2]
    if line_arr[2] != '':
        count += 1

print count
print float(count) / (len(all_the_text) - 1)
