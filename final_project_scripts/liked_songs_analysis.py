import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

models = [logreg, forest, xgb_model]
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

# drop unnecessary columns and scale to match trained data
columns_to_drop = ['name', 'id']
dfs = [df.drop(columns=columns_to_drop, errors='ignore') for df in dfs]
dfs = [scaler.transform(df) for df in dfs]

predictions = []
model_number = 1

# Create arrays to store all predictions for visualization
all_predictions = {
    'happy': np.zeros((len(models), len(dfs))),
    'sad': np.zeros((len(models), len(dfs))),
    'chill': np.zeros((len(models), len(dfs))),
    'energetic': np.zeros((len(models), len(dfs)))
}

for model_idx, model in enumerate(models):
    print("-------------------------------------------------------------------------")
    print(f"Model {model_number} predictions:")
    print()

    person = 1

    for df_idx, df in enumerate(dfs):
        # generate predictions for the current model and current person data
        predictions = model.predict(df)

        # calculate mood percentages
        chill_portion = (np.sum(predictions == 0) / len(predictions)) * 100
        energetic_portion = (np.sum(predictions == 1) / len(predictions)) * 100
        happy_portion = (np.sum(predictions == 2) / len(predictions)) * 100
        sad_portion = (np.sum(predictions == 3) / len(predictions)) * 100

        # Store predictions for visualization
        all_predictions['chill'][model_idx, df_idx] = chill_portion
        all_predictions['energetic'][model_idx, df_idx] = energetic_portion
        all_predictions['happy'][model_idx, df_idx] = happy_portion
        all_predictions['sad'][model_idx, df_idx] = sad_portion

        # determine the majority mood
        mood_percentages = [happy_portion, sad_portion, chill_portion, energetic_portion]
        majority_index = np.argmax(mood_percentages)
        majority_percentage = np.max(mood_percentages)
        mood_names = ["happy", "sad", "chill", "energetic"]

        print(f'Person {person} listens to mostly {mood_names[majority_index].upper()} music. '
              f'{round(majority_percentage,2)}%. is of this mood.')
        # print(f' Happy: {happy_portion:.2f}%')
        # print(f' Sad: {sad_portion:.2f}%')
        # print(f' Chill: {chill_portion:.2f}%')
        # print(f' Energetic: {energetic_portion:.2f}%\n')

        person += 1

    # Increment model count
    model_number += 1

# Visualization starts here
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Music Mood Distribution by Person', fontsize=16, y=1)

# Set up x-axis
x = np.arange(len(dfs))
width = 0.25  # Width of bars
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Colors for different models

# Plot Happy mood
ax1.bar(x - width, all_predictions['happy'][0], width, label='Model 1', color=colors[0])
ax1.bar(x, all_predictions['happy'][1], width, label='Model 2', color=colors[1])
ax1.bar(x + width, all_predictions['happy'][2], width, label='Model 3', color=colors[2])
ax1.set_title('Happy Music Distribution')
ax1.set_ylabel('Percentage')
ax1.set_xlabel('Person')
ax1.set_xticks(x)
ax1.set_xticklabels([f'Person {i+1}' for i in range(len(dfs))])
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot Sad mood
ax2.bar(x - width, all_predictions['sad'][0], width, label='Model 1', color=colors[0])
ax2.bar(x, all_predictions['sad'][1], width, label='Model 2', color=colors[1])
ax2.bar(x + width, all_predictions['sad'][2], width, label='Model 3', color=colors[2])
ax2.set_title('Sad Music Distribution')
ax2.set_ylabel('Percentage')
ax2.set_xlabel('Person')
ax2.set_xticks(x)
ax2.set_xticklabels([f'Person {i+1}' for i in range(len(dfs))])
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot Chill mood
ax3.bar(x - width, all_predictions['chill'][0], width, label='Model 1', color=colors[0])
ax3.bar(x, all_predictions['chill'][1], width, label='Model 2', color=colors[1])
ax3.bar(x + width, all_predictions['chill'][2], width, label='Model 3', color=colors[2])
ax3.set_title('Chill Music Distribution')
ax3.set_ylabel('Percentage')
ax3.set_xlabel('Person')
ax3.set_xticks(x)
ax3.set_xticklabels([f'Person {i+1}' for i in range(len(dfs))])
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot Energetic mood
ax4.bar(x - width, all_predictions['energetic'][0], width, label='Model 1', color=colors[0])
ax4.bar(x, all_predictions['energetic'][1], width, label='Model 2', color=colors[1])
ax4.bar(x + width, all_predictions['energetic'][2], width, label='Model 3', color=colors[2])
ax4.set_title('Energetic Music Distribution')
ax4.set_ylabel('Percentage')
ax4.set_xlabel('Person')
ax4.set_xticks(x)
ax4.set_xticklabels([f'Person {i+1}' for i in range(len(dfs))])
ax4.legend()
ax4.grid(True, alpha=0.3)

# Adjust layout and display
plt.tight_layout()
plt.show()