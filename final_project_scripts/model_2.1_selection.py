from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC, SVC
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier, GradientBoostingClassifier, BaggingClassifier, RandomForestClassifier
from sklearn.linear_model import RidgeClassifier, SGDClassifier, PassiveAggressiveClassifier

# pick best classifier
classifiers = [
    RidgeClassifier(random_state=1), SGDClassifier(random_state=1), PassiveAggressiveClassifier(random_state=1), RandomForestClassifier(random_state=1),
    GradientBoostingClassifier(random_state=1), AdaBoostClassifier(algorithm="SAMME", random_state=1),
    BaggingClassifier(random_state=1), ExtraTreesClassifier(random_state=1), SVC(random_state=1),
    LinearSVC(random_state=1), KNeighborsClassifier(),
    GaussianNB(), GaussianProcessClassifier(random_state=1)
]
scores = []
bestModel = None
bestScore = 0

for classifier in classifiers:
    meanScore = np.mean(cross_val_score(classifier, X_train, y_train, cv=10))
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