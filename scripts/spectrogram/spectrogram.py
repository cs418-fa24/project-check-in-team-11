import essentia.standard as es

# Load an audio file
audio = es.MonoLoader(filename='your_audio_file.wav')()

# Extract features
rhythm_extractor = es.RhythmExtractor2013()
bpm, beats, confidence, estimates = rhythm_extractor(audio)

# Print the BPM
