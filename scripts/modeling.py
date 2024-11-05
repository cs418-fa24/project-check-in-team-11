from sklearn.linear_model import (
    LinearRegression, LogisticRegression, Ridge, Lasso, ElasticNet,
    BayesianRidge, SGDRegressor, SGDClassifier, Perceptron, PassiveAggressiveRegressor,
    PassiveAggressiveClassifier, RidgeClassifier, RidgeCV, LassoCV, ElasticNetCV
)

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier,
    GradientBoostingRegressor, AdaBoostClassifier, AdaBoostRegressor,
    BaggingClassifier, BaggingRegressor, ExtraTreesClassifier, ExtraTreesRegressor,
    VotingClassifier, VotingRegressor, StackingClassifier, StackingRegressor
)

from sklearn.svm import SVC, SVR, LinearSVC, LinearSVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB, CategoricalNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.gaussian_process import GaussianProcessClassifier, GaussianProcessRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.semi_supervised import LabelPropagation, LabelSpreading
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture
from sklearn.cluster import (
    KMeans, MiniBatchKMeans, MeanShift, SpectralClustering, AgglomerativeClustering,
    DBSCAN, OPTICS, Birch, AffinityPropagation
)

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import json
import pandas as pd
import json
import numpy as np
from sklearn.preprocessing import LabelEncoder

moods = ['happy', 'sad', 'chill', 'energetic']
dfs = []
for mood in moods:
    files = [
        f'../raw/spotify_{mood}_1.json',
        # f'../raw/spotify_{mood}_2.json',
        f'../raw/spotify_{mood}_3.json',
        f'../raw/spotify_{mood}_4.json',
        f'../raw/spotify_{mood}_5.json',
        # f'../raw/spotify_{mood}_6.json',
    ]

    for file in files:
        with open(file, 'r') as fileio:
            df = pd.DataFrame(json.load(fileio))
            df['mood'] = mood
            dfs.append(df)

final_df = pd.concat(dfs, ignore_index=True)

#processing
drop = ['name', 'id']
final_df = final_df.drop(columns=drop)

final_df.to_csv('training.csv')

#splitting
X = final_df.iloc[:, 0:13]
Y = final_df.iloc[:, 13]
# encoder = LabelEncoder()
# y = encoder.fit_transform(Y)
xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size=.2, random_state=1)

# k-fold
k = 10
forest = RandomForestClassifier(random_state=2)
scores = cross_val_score(forest, xtrain, ytrain, cv=k)
print('CV scores', scores)
print('Mean CV scores', np.mean(scores))

# single
forest.fit(xtrain, ytrain)
print('Fit Score', forest.score(xtest, ytest))

################################################################################################
#analysis

import json
import pandas as pd

dfs = []

files = [
    f'../raw/liked_songs_1.json',
    # f'../raw/liked_songs_2.json',
    f'../raw/liked_songs_3.json',
    f'../raw/liked_songs_4.json',
    # f'../raw/liked_songs_5.json',
    # f'../raw/liked_songs_6.json',
]

for file in files:
    with open(file, 'r') as fileio:
        df = pd.DataFrame(json.load(fileio))
        dfs.append(df)

#processing
drop = ['name', 'id']
for i in range(0, 3):
    dfs[i] = dfs[i].drop(columns=drop)

predictions = []

for df in dfs:
    predictions.append(forest.predict(df.iloc[:, :]))

person = 1
for prediction in predictions:
    print(f'Person {person}')
    print('Happy', (prediction.tolist().count('happy')/len(prediction.tolist()))*100)
    print('Sad', (prediction.tolist().count('sad')/len(prediction.tolist()))*100)
    print('Chill', (prediction.tolist().count('chill')/len(prediction.tolist()))*100)
    print('Energetic', (prediction.tolist().count('energetic')/len(prediction.tolist()))*100)
    print()
    person += 1
