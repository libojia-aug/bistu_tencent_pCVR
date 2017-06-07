from getCUser import getData

cUsersData =  getData('../output/CUsers.csv')
installedApps = getData('../data/pre/user_installedapps.csv')


file_object = open('../output/CUsersApps.csv', 'w+')
file_object.write('userID,appID' + '\n')

for i in xrange(1, len(cUsersData)):  
    line1 = cUsersData[i].split(',')
    print i
    for j in xrange(1, len(installedApps)):
        line2 = installedApps[j].split(',')
        
        if int(line1[4]) == int(line2[0]):

            file_object.write(','.join(line2))
        if int(line1[4]) < int(line2[0]):
            break
file_object.close()