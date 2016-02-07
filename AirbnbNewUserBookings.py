import pandas as pd
import numpy as np
import numbers, sklearn
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn import svm, decomposition, preprocessing
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
from sknn.mlp import Regressor, Layer, Classifier

TRAIN, TEST = 0, 1

print(sklearn.__version__)

print('Reading CSV Files...')
train = pd.read_csv('train_users_2.csv', header=0)
test = pd.read_csv('test_users.csv')
filled = [train.copy(), test.copy()]

sessions = pd.read_csv('age_gender_bkts.csv')

print(filled[0])
print('Cleaning Data: Converting all entries to numerical type, filling NaNs, etc...')
le = preprocessing.LabelEncoder()
for i, df in enumerate(filled):
    for row in df.iterrows():
        if pd.isnull(row['age']):
            row['age'] =

    '''
    for feature in [col for col in df.columns if col not in ['id', 'country_destination']]: #Excluding id
        if df[feature].dtype not in [int, float]:
            if 'date' in feature:
                #df[feature] = pd.to_datetime(df[feature])
                #df[feature] = (df[feature] - df[feature].min()) / np.timedelta64(1,'D')
                print(feature)
                df[feature] = df[feature].astype('timedelta64[s]')
            else:
                #mapping = {value: i for i, value in enumerate([_ for _ in df[feature].unique() if _ is not np.nan])}
                #mapping_full = lambda x: mapping[x] if x not in ['-unknown-', np.nan] else np.nan
                #df[feature] = df[feature].map(mapping_full)
                df[feature] = df[feature].astype(str)
                #print(df[feature])
                df[feature] = le.fit_transform(df[feature])
    df = df.fillna(-1)
    '''

print(filled[0])


        #mean = np.mean(df[feature][df[feature].notnull()])
        #df[feature] = df[feature].fillna(mean)
'''
print('Dropping columns of data entirely missing on at least one set...')
for col in filled[TEST].columns:
    if any(df[col].isnull().all() for df in filled):
        for i, df in enumerate(filled):
            filled[i] = filled[i].drop(col, axis=1)

print('Isolating train/test sets...')
X_train, y_train = filled[TRAIN].ix[:, 1:-1], filled[TRAIN].ix[:, -1]
X_test = filled[TEST].ix[:, 1:]

print('Training Model...')
model = RandomForestClassifier(n_estimators=20, criterion='entropy', oob_score=True)
model.fit(X_train, y_train)



print('Making prediction...')
y_test = pd.DataFrame(model.predict(X_test))
to_output = pd.concat([filled[TEST]['id'], y_test], axis=1)

print('Writing prediction to submission file...')
to_output.to_csv('submission.csv', index=False, header=['id', 'country'])
'''