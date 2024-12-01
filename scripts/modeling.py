from scipy.stats import zscore
from sklearn.linear_model import (SGDClassifier,
    PassiveAggressiveClassifier, RidgeClassifier
)

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier,
    BaggingClassifier, ExtraTreesClassifier
)

from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier


from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import json
import pandas as pd

moods = ['happy', 'sad', 'chill', 'energetic']
dfs = []
for mood in moods:
    files = [
        f'../raw/spotify_{mood}_1.json',
        f'../raw/spotify_{mood}_2.json',
        f'../raw/spotify_{mood}_3.json',
        f'../raw/spotify_{mood}_4.json',
        f'../raw/spotify_{mood}_5.json',
        f'../raw/spotify_{mood}_6.json',
    ]

    for file in files:
        with open(file, 'r') as fileio:
            df = pd.DataFrame(json.load(fileio))
            df['mood'] = mood
            dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)

#drop nondistinct rows
duplicate_names = final_df[final_df.duplicated(subset=['name'], keep=False)]
conflicting_moods = duplicate_names.groupby('name')['mood'].nunique()
conflicting_names = conflicting_moods[conflicting_moods > 1].index
final_df = final_df[~final_df['name'].isin(conflicting_names)]


#processing
drop = ['name', 'id']
final_df = final_df.drop(columns=drop)
encoder = LabelEncoder()
final_df['mood'] = encoder.fit_transform(final_df['mood'])

#splitting
X = final_df.iloc[:, 0:13]
Y = final_df.iloc[:, 13]
xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size=.3, random_state=1)

#scaling
scaler = StandardScaler()
xtrainScaled = scaler.fit_transform(xtrain)
xtestScaled = scaler.transform(xtest)

#remove outliers
z_scores = np.abs(zscore(xtrainScaled))
threshold = 3
outliers = np.where(z_scores > threshold)

xtrainClean = xtrainScaled[(z_scores < threshold).all(axis=1)]
ytrainClean = ytrain[(z_scores < threshold).all(axis=1)]

# pick best classifier
classifiers = [
    RidgeClassifier(random_state=1), SGDClassifier(random_state=1), PassiveAggressiveClassifier(random_state=1),
    DecisionTreeClassifier(random_state=1), RandomForestClassifier(random_state=1),
    GradientBoostingClassifier(random_state=1), AdaBoostClassifier(random_state=1),
    BaggingClassifier(random_state=1), ExtraTreesClassifier(random_state=1), SVC(random_state=1),
    LinearSVC(random_state=1), KNeighborsClassifier(),
    GaussianNB(), MLPClassifier(random_state=1), GaussianProcessClassifier(random_state=1)
]
scores = []
bestModel = None
bestScore = 0

for classifier in classifiers:
    meanScore = np.mean(cross_val_score(classifier, xtrain, ytrain, cv=5))
    scores.append(
        {
            'Name': f'{type(classifier).__name__}',
            'Score': meanScore
        }
    )

    if meanScore > bestScore:
        bestScore = meanScore
        bestModel = classifier

print(bestModel, bestScore)

bestModel = RandomForestClassifier(random_state=1)
bestModel.fit(xtrain, ytrain)

###############################################################################################
# analysis

dfs = []

files = [
    '../raw/liked_songs_1.json',
    '../raw/liked_songs_2.json',
    '../raw/liked_songs_3.json',
    '../raw/liked_songs_4.json',
    '../raw/liked_songs_5.json',
    '../raw/liked_songs_6.json',
]

for file in files:
    with open(file, 'r') as fileio:
        df = pd.DataFrame(json.load(fileio))
        dfs.append(df)

#processing
drop = ['name', 'id']
for i in range(0, 6):
    dfs[i] = dfs[i].drop(columns=drop)

predictions = []

for df in dfs:
    predictions.append(bestModel.predict(df.iloc[:, :]))

person = 1
print()
for prediction in predictions:
    print(f'Person {person}')
    print('Happy', (prediction.tolist().count(2)/len(prediction.tolist()))*100)
    print('Sad', (prediction.tolist().count(3)/len(prediction.tolist()))*100)
    print('Chill', (prediction.tolist().count(0)/len(prediction.tolist()))*100)
    print('Energetic', (prediction.tolist().count(1)/len(prediction.tolist()))*100)
    print()
    person += 1
