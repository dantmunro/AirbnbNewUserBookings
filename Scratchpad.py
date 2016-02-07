import pandas as pd
import numpy as np

MAX_AGE = 125

train = pd.read_csv('train_users_2.csv', header=0)
train_filled = train.copy()
train_filled[train_filled["age"] > MAX_AGE] = np.nan
age_gender_bkts = pd.read_csv('age_gender_bkts.csv')
agb_filled = age_gender_bkts.copy()

agb_filled['age_bucket'] = \
    agb_filled['age_bucket'].apply(lambda x: tuple([int(num) for num in x.split("-")])
                                        if "-" in x else tuple([int(num) for num in filter(None, x.split("+"))] + [MAX_AGE]))
agb_filled['age_bucket_min'] = agb_filled['age_bucket'].apply(min).astype(int)
agb_filled['age_bucket_max'] = agb_filled['age_bucket'].apply(max).astype(int)

print("Before:", len(train_filled[train_filled['gender'] == '-unknown-']['gender'].tolist()))#print(age_gender_bkts)
print("Before:", train_filled['gender'])
def fill_gender(row):
    #print("Old Row Gender:", row['gender'])
    #print("Row:", row)
    #print(row['age'])
    row_age = int(row['age'])
    row_dest = str(row['country_destination'])
    #print("Row Age:", row_age)
    #print("Row Dest:", row_dest)
    #print("Matching Countries:", age_gender_bkts.loc[(age_gender_bkts['country_destination'].str.match(row_dest))])
    possible_genders = agb_filled.loc[(agb_filled['country_destination'] == row_dest)
                                      & (agb_filled['age_bucket_max'] >= row_age)
                                      & (agb_filled['age_bucket_min'] <= row_age)]
    #print("Possible New Row Genders:", possible_genders)
    new_gender = possible_genders.loc[possible_genders['population_in_thousands'].idxmax()]['gender']
    #print("New Row Gender:", new_gender)
    new_gender = str(new_gender).upper()
    return new_gender
    #row['gender'] = new_gender
    #return row

train_filled.loc[(train_filled['gender'] == '-unknown-') & (~train_filled['country_destination'].isin(["NDF", "other"])) & (~train_filled['age'].isnull()), 'gender'] \
 = train_filled[(train_filled['gender'] == '-unknown-') & (~train_filled['country_destination'].isin(["NDF", "other"])) & (~train_filled['age'].isnull())].apply(lambda row: fill_gender(row), axis=1)



#sample_row = train[(train['gender'] == '-unknown-') & (train['country_destination'] != "NDF")
#            & (~pd.isnull(train['age']))].head(1)
#print("Sample Row:", sample_row)
#fill_gender(sample_row)
#print("New Sample Row:", sample_row)
#train_filled[(train_filled['gender'] == '-unknown-') & (~train_filled['country_destination'].isin(["NDF", "other"])) & (~train_filled['age'].isnull())].replace()
#print(to_replace)
#print(train[(train['gender'] == '-unknown-') & (~train['country_destination'].isin(["NDF", "other"])) & (~train['age'].isnull())])
#train[(train['gender'] == '-unknown-') & (~train['country_destination'].isin(["NDF", "other"])) & (~train['age'].isnull())] = to_replace

'''
for i, row in train[(train['gender'] == '-unknown-') & (train['country_destination'] != "NDF")
            & (~pd.isnull(train['age']))].iterrows():

        #if i == 5:
        #    print(train.loc[i, 'country_destination'])
        #    print(train.loc[i, 'age'])
        #    print(age_gender_bkts[(age_gender_bkts['country_destination'] == train.loc[i, 'country_destination'])
        #        & (age_gender_bkts['age_bucket_max'] >= train.loc[i, 'age'])
        #        & (age_gender_bkts['age_bucket_min'] <= train.loc[i, 'age'])].max(key='population_in_thousands'))

        train.loc[i, 'gender'] = \
            age_gender_bkts[(age_gender_bkts['country_destination'] == train.loc[i, 'country_destination'])
                & (age_gender_bkts['age_bucket_max'] >= train.loc[i, 'age'])
                & (age_gender_bkts['age_bucket_min'] <= train.loc[i, 'age'])].max(key='population_in_thousands')['gender']
'''
print("After:", len(train_filled[train_filled['gender'] == '-unknown-']['gender'].tolist()))
print(train_filled['gender'])