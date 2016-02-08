import pandas as pd
import numpy as np
from scipy.stats import rv_discrete

#Experimentation with methods of filling data holes

MAX_AGE = 125
KEY, VALUE = 0, 1
FIRST = 1

#Read and copy traing and age_gender_bkts datasets
train = pd.read_csv('train_users_2.csv', header=0)
train_filled = train.copy()
train_filled[train_filled["age"] > MAX_AGE] = np.nan
age_gender_bkts = pd.read_csv('age_gender_bkts.csv')
agb_filled = age_gender_bkts.copy()

#Break up age-bucket ranges into their endpoints, and represent the bucket mins and maxes on separate columns
agb_filled['age_bucket'] = \
    agb_filled['age_bucket'].apply(lambda x: tuple([int(num) for num in x.split("-")])
                                        if "-" in x else tuple([int(num) for num in filter(None, x.split("+"))] + [MAX_AGE]))
agb_filled['age_bucket_min'] = agb_filled['age_bucket'].apply(min).astype(int)
agb_filled['age_bucket_max'] = agb_filled['age_bucket'].apply(max).astype(int)

#Before/after comparison on number of rows with unknown gender
print("Before:", len(train_filled[train_filled['gender'] == '-unknown-']['gender'].tolist()))
print("Before:", train_filled['gender'])

#Given a row and a column/feature, reassign that row's feature some value based on the most likely
#value of some other feature (generally using age_gender_bkts).  For instance, if filling in missing genders,
#get the most likely gender given the age of the user

#Also attempting to emit a random variable for such a feature weighted by the counts of each feature value
#(For instance, if 500 men and 500 women in the dataset are between 20-25, generate a random value for the
#gender weighted on the normalization of those counts - i.e. .5 probability male, .5 female.
def fill_gender(row, column):
    if column == 'gender':
        row_age = int(row['age'])
        row_dest = str(row['country_destination'])
        possible_genders = agb_filled.loc[(agb_filled['age_bucket_max'] >= row_age) & (agb_filled['age_bucket_min'] <= row_age)]
        new_gender = rv_discrete(values=((0, 1), tuple([possible_genders.groupby('gender').get_group(gender)['population_in_thousands'].sum() for gender in ('female', 'male')])), seed=20)
        #FIXME Distribution puts all weight toward 0
        print(new_gender.pmf(0))
        new_gender = "FEMALE" if new_gender.rvs() == 0 else "MALE"
        if new_gender == "MALE": print("New Row Gender:", new_gender)
        return new_gender
    elif column == 'age':
        row_gender = str(row['gender'])
        possible_ages = agb_filled.loc[(agb_filled['gender'] == row_gender)]

#Fills in missing genders - can only do so for rows with a given age (i.e. not NaN)
train_filled.loc[(train_filled['gender'] == '-unknown-') & (~train_filled['age'].isnull()), 'gender'] \
     = train_filled[(train_filled['gender'] == '-unknown-') & (~train_filled['age'].isnull())].apply(lambda row: fill_gender(row, column='gender'), axis=1)

#Before/after comparison on number of rows with unknown gender
print("After:", len(train_filled[train_filled['gender'] == '-unknown-']['gender'].tolist()))
print(train_filled['gender'])