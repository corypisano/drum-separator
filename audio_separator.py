import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf

def write_audio(audio_data, name):
    # Write out audio as 24bit PCM WAV
    sample_rate = 44100
    sf.write(name, audio_data, sample_rate)

def extract_harmonic_percussive(audio_file=None):
    if audio_file is None:
        audio_file = librosa.util.example_audio_file()
    # Extract harmonic and percussive components
    y, sr = librosa.load(audio_file)
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    return y_harmonic, y_percussive

#D = librosa.stft(y)
#D_harmonic, D_percussive = librosa.decompose.hpss(D)

def show_spectrogram(D, D_percussive): 
    rp = np.max(np.abs(D))
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=rp), y_axis='log')
    plt.colorbar()
    plt.title('Full spectrogram')

    plt.subplot(2, 1, 2)
    librosa.display.specshow(librosa.amplitude_to_db(D_percussive, ref=rp), y_axis='log', x_axis='time')
    plt.colorbar()
    plt.title('Percussive spectrogram')
    plt.tight_layout()

class AudioSeparator:
    def __init__(self, audio_file):
        pass