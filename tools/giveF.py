# -*- coding:utf-8 -*-
import os
from getCUser import getData

installedApps = getData('../data/pre/user_installedapps.csv')

c = {}
c['210'] = 437.2079122
c['211'] = 416.1429931
c['110'] = 423.8225956
c['1'] = 409.9602377
c['0'] = 6.335796631
c['407'] = 147.0032104
c['406'] = 434.4933626
c['405'] = 510.7377538
c['2'] = 425.7038419
c['403'] = 377.242635
c['402'] = 608.2054288
c['401'] = 291.9669111
c['503'] = 929.7557125
c['409'] = 407.1688163
c['408'] = 418.5122032
c['201'] = 511.836904
c['203'] = 553.8796054
c['204'] = 409.2866881
c['209'] = 198.9956448
c['301'] = 540.3519243
c['303'] = 441.2176825
c['108'] = 483.9008965
c['109'] = 423.9198886
c['103'] = 352.654423
c['106'] = 382.642894
c['104'] = 477.1060653
c['105'] = 422.9540055
c['n'] = 36.99396705

user = {}
path = '../data/features/ncuser-c'
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        print name
        data = getData(path + '/' + name)
        for i in xrange(0, len(data)):
            line = data[i]
            # print line.find('Optional.empty')
            if line.find('Optional.empty') > -1:
                a = line.split(',(,Optional.empty)')
                u = a[0][1:]
                # print u
                if user.has_key(u):
                    user[u]['k'] += c['n']
                    user[u]['v'] += 1
                else:
                    user[u] = {}
                    user[u]['k'] = c['n']
                    user[u]['v'] = 1
            else:
                a = line.split(',(,Optional[Optional[')
                # print a
                u = a[0][1:]
                ca = a[1][:len(a[1]) - 5]
                # print u
                if user.has_key(u):
                    user[u]['k'] += c[ca]
                    user[u]['v'] += 1
                else:
                    user[u] = {}
                    user[u]['k'] = c[ca]
                    user[u]['v'] = 1
            # print user
    #         if i == 30:
    #             break
    #     break
    # break
user_list = user.items()
user_f = {}
for k in xrange(1, len(user_list)):
    user_f[user_list[k][0]] = user[user_list[k][0]]['k'] / user[user_list[k][0]]['v']
file_object = open('../data/ncuser-fcf.csv', 'w+')
file_object.write('userID, fc' + '\n')
for j in user_f:
    file_object.write(j + ',' + str(user_f[j]) + '\n')
file_object.close()
