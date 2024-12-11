from scipy.stats import zscore
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, ConfusionMatrixDisplay

moods = ['happy', 'sad', 'chill', 'energetic']
dfs = []
for mood in moods:
    files = [
        f'./raw/spotify_{mood}_1.json',
        f'./raw/spotify_{mood}_2.json',
        f'./raw/spotify_{mood}_3.json',
        f'./raw/spotify_{mood}_4.json',
        f'./raw/spotify_{mood}_5.json',
        f'./raw/spotify_{mood}_6.json',
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

#drop non-feature columns
drop = ['name', 'id']
final_df = final_df.drop(columns=drop)

#encode moods
label_encoder = LabelEncoder()
final_df['mood'] = label_encoder.fit_transform(final_df['mood'])

#splitting
scaler = StandardScaler()
X = final_df.iloc[:, 0:13]
X = scaler.fit_transform(X)
y = final_df.iloc[:, 13]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=1)

#remove outliers
z_scores = np.abs(zscore(X_train))
threshold = 3
outliers = np.where(z_scores > threshold)

X_train = X_train[(z_scores < threshold).all(axis=1)]
y_train = y_train[(z_scores < threshold).all(axis=1)]