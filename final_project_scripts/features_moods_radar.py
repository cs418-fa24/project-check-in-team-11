import matplotlib.pyplot as plt

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

moods_df = pd.concat(dfs, ignore_index=True)

#processing
drop = ['name', 'id']
moods_df = moods_df.drop(columns=drop)

moods_mean_df = moods_df.groupby('mood').mean()


factors = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo']

new_max = 100
new_min = 20
new_range = new_max - new_min

for factor in factors:
    max_val = moods_mean_df[factor].max()
    min_val = moods_mean_df[factor].min()
    val_range = max_val - min_val
    moods_mean_df[factor + '_Adj'] = moods_mean_df[factor].apply(
        lambda x: (((x - min_val) * new_range) / val_range) + new_min)

moods_mean_df = moods_mean_df.reset_index()

dft = moods_mean_df.loc[:, ['mood', 'acousticness_Adj', 'danceability_Adj', 'energy_Adj',
                            'instrumentalness_Adj', 'liveness_Adj', 'loudness_Adj', 'speechiness_Adj',
                            'valence_Adj', 'tempo_Adj']]
dft.rename(columns={
    'acousticness_Adj': 'acousticness',
    'danceability_Adj': 'danceability',
    'energy_Adj': 'energy',
    'instrumentalness_Adj': 'instrumentalness',
    'liveness_Adj': 'liveness',
    'loudness_Adj': 'loudness',
    'speechiness_Adj': 'speechiness',
    'valence_Adj': 'valence',
    'tempo_Adj': 'tempo'
}, inplace=True)

dft.set_index('mood', inplace=True)

labels = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo']
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

def add_to_radar(mood, color):
    values = dft.loc[mood].tolist()
    ax.plot(angles, values, color=color, linewidth=1, label=mood)
    ax.fill(angles, values, color=color, alpha=0.25)

add_to_radar('happy', '#1aaf6c')
add_to_radar('sad', '#429bf4')
add_to_radar('chill', '#d42cea')
add_to_radar('energetic', '#f4b41a')

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_thetagrids(np.degrees(angles), labels)

for label, angle in zip(ax.get_xticklabels(), angles):
    if angle in (0, np.pi):
        label.set_horizontalalignment('center')
    elif 0 < angle < np.pi:
        label.set_horizontalalignment('left')
    else:
        label.set_horizontalalignment('right')

ax.set_ylim(0, 100)
ax.set_rlabel_position(180 / num_vars)

ax.tick_params(colors='#222222')
ax.tick_params(axis='y', labelsize=8)
ax.grid(color='#AAAAAA')
ax.spines['polar'].set_color('#222222')
ax.set_facecolor('#FAFAFA')

ax.set_title('Comparing moods across features', y=1.08)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.show()
