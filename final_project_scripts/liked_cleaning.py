import pandas as pd
import json
import numpy as np

dfs = []

files = [
    f'./raw/liked_songs_1.json',
    f'./raw/liked_songs_2.json',
    f'./raw/liked_songs_3.json',
    f'./raw/liked_songs_4.json',
    f'./raw/liked_songs_5.json',
    f'./raw/liked_songs_6.json',
]

for file in files:
    with open(file, 'r') as fileio:
        df = pd.DataFrame(json.load(fileio))
        dfs.append(df)

liked_songs_df = pd.concat(dfs, ignore_index=True)

#processing
drop = ['name', 'id']
liked_songs_df = liked_songs_df.drop(columns=drop)

#liked_songs_df.head(5)
liked_songs_df.describe()