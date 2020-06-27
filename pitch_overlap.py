import parselmouth as pm
from parselmouth.praat import call
from glob import glob
import pandas as pd

stnum = ['512', '3629', '6110', '6468', '9198']
room = ['A', 'B']
stu_part = ['participant', 'student']

data = pd.DataFrame(columns=["stnum", "room", "stu_part", "min_freq", "max_freq", "avg_freq", "wav_file"])

for n in stnum:
      for r in room:
            for sp in stu_part:
                  
                  # Debug values
                  # n, r, sp = stnum[0], room[1], stu_part[0]
                  # wav = "512/B/participant/72.17 - 73.18 - simultaneous.wav"
            
                  for wav in glob(n + "/" + r + "/" + sp + "/* - simultaneous.wav"):
                        wav = wav.replace('\\','/')
                        sound = pm.Sound(wav)
                        pitch = sound.to_pitch(pitch_floor = 50.0, pitch_ceiling = 600.0)
                        pitch = call(sound, "To Pitch", 0.0, 50.0, 600.0)
                        min_freq = call(pitch, "Get minimum", sound.xmin, sound.xmax, "Hertz", "Parabolic")
                        max_freq = call(pitch, "Get maximum", sound.xmin, sound.xmax, "Hertz", "Parabolic")
                        avg_freq = (min_freq + max_freq) / 2
                        
                        # # Could manually get frequencies by checking distances between pulses
                        # manipulation = call(sound, "To Manipulation", 0.01, 50, 600)
                        
                        # # Individual pulse of a waveform
                        # pulse = call(manipulation, "Extract pulses")
                        # idx_pulse = call(pulse, "Get number of points")
                        
                        # # Getting pitch values
                        # pitch_1 = call(manipulation, "Extract pitch tier")
                        # idx_pitch = call(pitch_1, "Get number of points")
                        # list_freq_time = [(call(pitch_1, "Get value at index", jb), call(pitch_1, "Get time from index", jb)) for jb in range(1,idx_pitch)]
                        # min_freq, max_freq = min(list_freq_time)[0], max(list_freq_time)[0]
                        
                        
                        # Getting overlaps
                        # To get overlaps, there should be equal number of co laughs at same places
                        # for both student and participant. This does not seem to be the case here.
                        # Either there was a problem duting the annotation or the student did not annotate it in the first place.
                        
                        
                        row = {"stnum" : n, "room" : r, "stu_part" : sp, "min_freq" : min_freq, "max_freq" : max_freq, "avg_freq": avg_freq, "wav_file": wav}
                        # print(row)
                        data = data.append(row, ignore_index = True)

data.to_csv("freq_1.csv")

# data = pd.read_csv("freq_1.csv")
