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

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import json
import pandas as pd

moods = ['happy', 'sad', 'chill', 'energetic']
dfs = []
for mood in moods:
    files = [
        f'../raw/spotify_{mood}_1.json',
        # f'../raw/spotify_{mood}_2.json',
        f'../raw/spotify_{mood}_3.json',
        f'../raw/spotify_{mood}_4.json',
        # f'../raw/spotify_{mood}_5.json',
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

#splitting
X = final_df.iloc[:, 0:13]
Y = final_df.iloc[:, 13]

xtrain, xtest, ytrain, ytest = train_test_split(X, Y, test_size=.2, random_state=1)

# train
forest = RandomForestClassifier()
forest.fit(xtrain, ytrain)

# score
# print(forest.score(xtest, ytest))

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

dfs[0].to_csv('testing.csv')

#processing
drop = ['name', 'id']
for df in dfs:
    df = df.drop(columns=drop)

predictions = []

for df in dfs:
    predictions.append(forest.predict(df.iloc[:, :]))














