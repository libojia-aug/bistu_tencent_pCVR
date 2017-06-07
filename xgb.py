import xgboost as xgb
import pandas as pd
import scipy as sp

train = pd.read_csv('./data/xgb/train.csv')
# train = train.sample(n=1000000, axis=0)  # shuffle the data
val = train.iloc[0:5000]
train = train.iloc[5000:15000]

train_y = train.label
train_X = train.drop('label', axis=1)
val_y = val.label
val_X = val.drop('label', axis=1)

dtrain = xgb.DMatrix(train_X, label=train_y)
dval = xgb.DMatrix(val_X, label=val_y)

params = {'booster':'gbtree',
          'objective': 'binary:logistic',
          'eta': 0.00001,
          'max_depth': 10,
          'num_boost_round': 100000,
          'scale_pos_weight': 1.0,
          'subsample': 1,
          'colsample_bytree': 0.9,
          'colsample_bylevel': 1.0,
          'min_sample_split': 10,
          'min_child_weight': 5,
          'lambda': 10,
          'gamma': 0,
          'eval_metric': "error",
          'maximize': False,
          'num_thread': 16,
          'learning_rate' :0.01}

def logloss(act, pred):
  epsilon = 1e-15
  pred = sp.maximum(epsilon, pred)
  pred = sp.minimum(1-epsilon, pred)
  ll = sum(act*sp.log(pred) + sp.subtract(1,act)*sp.log(sp.subtract(1,pred)))
  ll = ll * -1.0/len(act)
  return 'logloss', ll

watchlist = [(dval, 'val')]
model = xgb.train(params, dtrain,num_boost_round=10000, early_stopping_rounds=200, evals=watchlist, feval=logloss)
#  Best iteration 37, val-error:0.198
preds = model.predict(dval)

outing = open('./Result.txt', 'w')  
for x in xrange(0,len(preds)):
     outing.write(str(preds[x])+'\n')

outing.close()  