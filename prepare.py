
def toDic(path):
    file_object = open(path)
    dic = {}
    try:
        all_the_text = file_object.readlines()
    finally:
        file_object.close()
    for i in xrange(1, len(all_the_text)):
        line_arr = all_the_text[i].split(',')
        dic[line_arr[0]] = line_arr[1:]
    return dic

BASE_FEATURES = '37'
class prepare():

    def __init__(self):
        self.ad_dic = toDic('./data/pre/ad.csv')
        self.user_dic  = toDic('./data/pre/user.csv')
        self.position_dic = toDic('./data/pre/position.csv')
        self.cUsersF_dic = toDic('./data/cuser-fcf.csv')
        self.ncUsersF_dic = toDic('./data/ncuser-fcf.csv')

    def getAd(adId):
        return self.ad_dic[adId]

    def getUser(userId):
        return self.user_dic[userId]

    def getPosition(positionId):
        return self.position_dic[positionId]

    def getCUsersF(userId):
        if self.cUsersF_dic.has_key(userId):
            return [str(int(round(float(self.cUsersF_dic[userId][0][0:-2]))))]
        else:
            return [BASE_FEATURES]

    def getNCUsersF(userId):
        if self.ncUsersF_dic.has_key(userId):
            return [str(int(round(float(self.ncUsersF_dic[userId][0][0:-2]))))]
        else:
            return [BASE_FEATURES]
        

    def getAll(self, adId, userId, positionId):
        aup = []
        ad_list = self.ad_dic[adId]
        aup.extend(ad_list)
        user_list = self.user_dic[userId]
        aup.extend(user_list)
        position_list = self.position_dic[positionId]
        aup.extend(position_list)
        if self.cUsersF_dic.has_key(userId):
            userF_list = [str(int(round(float(self.cUsersF_dic[userId][0][0:-2]))))]
        elif self.ncUsersF_dic.has_key(userId):
            userF_list = [str(int(round(float(self.ncUsersF_dic[userId][0][0:-2]))))]
        else:
            userF_list = [BASE_FEATURES]
        aup.extend(userF_list)
        return aup