### spleeter
from spleeter.separator import Separator

#from spleeter.utils.audio.adapter import get_default_audio_adapter
#audio_loader = get_default_audio_adapter()

import soundfile as sf


def run(audio_path, drum_ratio):
    """ drum percent is amount of drums in output mix, 0 to 1 """
    pass

def separate_drums(audio_path, output_dir='/output'):
    separator = Separator('spleeter:4stems')
    separator.separate_to_file(audio_path, output_dir)

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
