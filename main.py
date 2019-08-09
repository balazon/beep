import pyaudio
import numpy as np

import winsound

# TODO cross platform either by adding linux synthesizer or pyaudio

def test_linux():
    # SoX must be installed using 'sudo apt-get install sox' in the terminal
    import os
    duration = 1000
    frequency = 440
    os.system('play -n synth %s sin %s' % (duration/1000, frequency))

duration_mul = 75 # duration unit is 100 millisecs

# Note format:
# basic note letter (C,D,E,F,G,A,B)
# followed by an optional modifier (#, b)
# and an optional octave (4 by default, C4 is the mid piano C)
# '_' separator, and the duration
score_bociboci = "C_4 E_4 C_4 E_4 G_8 G_8 C_4 E_4 C_4 E_4 G_8 G_8 C5_4 B_4 A_4 G_4 F_8 A_8 G_4 F_4 E_4 D_4 C_8 C_8"

score_jurassic_park = "G_4 E_4 F_2 E_2 D_4 C_4 G_4 C5_4 C_4"

score_liszt = "C#_1 C#_31 C#3_1 C#3_31 C#_2 B3_1 C#_1 B3_31 D3_1 D3_15 C#_2 E_2 D_2 C#_1 C#_31"

# Z accounts for half notes so that D can be 2 half notes away from C, and F only 1 half-note away from E
notes_ordered = "CZDZEFZGZAZB"
note_map = {val:idx for idx, val in enumerate(notes_ordered)}

def get_freq_dur(note_str):
    note, dur = note_str.split("_")
    dur = int(dur)
    
    mod = 0
    mod_map = {'#' : 1, "b" : -1}
    if len(note) >= 2 and note[1] in mod_map:
        mod = mod_map[note[1]]
    pitch = note_map[note[0]]
    pitch += mod
    
    octave_offset = 1 + int(mod)
    octave = 4 if len(note) <= octave_offset else int(note[octave_offset:])
    pitch += (octave - 4) * 12
    
    freq = int(440 * (2 ** (1 / 12)) ** (3 + pitch))
    dur *= duration_mul
    return freq, dur

def play_score(score):
    notes = score.split(" ")
    for note in notes:
        freq, dur = get_freq_dur(note)
        winsound.Beep(freq, dur)

def test_pyaudio():
    # TODO duration is buggy as hell
    p = pyaudio.PyAudio()

    volume = 0.5     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    duration = 1.0   # in seconds, may be float
    f = 440.0        # sine frequency, Hz, may be float


    duration *= 4.0 # TODO this is just a practical number, not accurate, but needed, dunno why

    # generate samples, note conversion to float32 array
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    # play. May repeat with different volume values (if done interactively) 
    stream.write(volume*samples)

    stream.stop_stream()
    stream.close()

    p.terminate()

if __name__ == "__main__":
    import time
    play_score(score_liszt)

    # test_pyaudio()
    # time.sleep(1.0)
    # test_pyaudio()
    # time.sleep(1.0)
    # test_pyaudio()
    # time.sleep(1.0)
    # play_score("A3_10")
    # time.sleep(1.0)
    # play_score("A3_10")
    # time.sleep(1.0)
    # play_score("A3_10")