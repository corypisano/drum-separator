### spleeter
# from spleeter.separator import Separator

# from pydub import AudioSegment

# from spleeter.utils.audio.adapter import get_default_audio_adapter
# audio_loader = get_default_audio_adapter()


def run(audio_path, drum_ratio):
    """ drum percent is amount of drums in output mix, 0 to 1 """
    pass


def combine_drumless(output_dir, song_name):
    """Combine bass, vocals, and other into drumless file, return the filepath"""
    sound1 = AudioSegment.from_wav(f"{output_dir}/{song_name}/bass.wav")
    sound2 = AudioSegment.from_wav(f"{output_dir}/{song_name}/vocals.wav")
    sound3 = AudioSegment.from_wav(f"{output_dir}/{song_name}/other.wav")
    combined = sound1.overlay(sound2).overlay(sound3)

    drumless_filepath = f"{output_dir}/{song_name}/drumless.wav"
    combined.export(drumless_filepath, format="wav")
    return drumless_filepath


"""
def separate_from_waveform(waveform):
    separator = Separator('spleeter:4stems')
    # Perform the separation :
    prediction = separator.separate(waveform)
    return prediction

def load_waveform_from_file(filepath):
    # Use audio loader explicitly for loading audio waveform :
    #sample_rate = 44100
    #waveform, sample_rate = audio_loader.load(filepath, sample_rate=sample_rate)
    waveform, sample_rate = audio_loader.load(filepath)
    return waveform, sample_rate

def save_to_file(waveform, path, sample_rate):
    try:
        audio_loader.save(path=path, data=waveform, sample_rate=sample_rate)
    except IOError as e:
        print(e)
        raise(e)
    return True
"""


def add_waveforms(waveforms=[]):
    result = []
    for waveform in waveforms:
        pass
    return result


def write_audio(audio_data, name):
    """Write out audio data as 24bit PCM WAV"""
    sample_rate = 44100
    sf.write(name, audio_data, sample_rate)
