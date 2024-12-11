import json
import pandas as pd

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

#processing
drop = ['name', 'id']
final_df = final_df.drop(columns=drop)