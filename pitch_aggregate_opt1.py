import parselmouth as pm
from parselmouth.praat import call
from glob import glob
import pandas as pd

stnum = ['512', '3629', '6110', '6468', '9198']
room = ['A', 'B']
stu_part = ['participant', 'student']

data = pd.DataFrame(columns=["stnum", "room", "freq_st", "freq_par", "freq_diff", "dur_laugh_st", "num_laugh_st", "dur_laugh_par", "num_laugh_st", "ratio_voiced", "familiarity"])


# Replaces nan values in the list with the average of the list
def rem_nan(val):
      val = pd.DataFrame(val)
      val = pd.DataFrame.fillna(val, val.mean())
      return list(val[0])


for n in stnum:
      
      familiarity = pd.read_csv(n + "/familiarity.txt")
      
      # Debug values
      # n, r, = stnum[0], room[1]
            
      for r in room:
            
            avg_freq_par = []
            
            for wav in glob(n + "/" + r + "/participant/* - simultaneous.wav"):
                  sound = pm.Sound(wav)
                  pitch = sound.to_pitch(pitch_floor = 50.0, pitch_ceiling = 600.0)
                  pitch = call(sound, "To Pitch", 0.0, 50.0, 600.0)
                  min_freq = call(pitch, "Get minimum", sound.xmin, sound.xmax, "Hertz", "Parabolic")
                  max_freq = call(pitch, "Get maximum", sound.xmin, sound.xmax, "Hertz", "Parabolic")
                  avg_freq_par.append((min_freq + max_freq)/2)

            avg_freq_par = rem_nan(avg_freq_par)
            avg_freq_par = sum(avg_freq_par)/len(avg_freq_par)
            
            
            avg_freq_st = []                  
            
            for wav in glob(n + "/" + r + "/student/* - simultaneous.wav"):
                  sound = pm.Sound(wav)
                  pitch = sound.to_pitch(pitch_floor = 50.0, pitch_ceiling = 600.0)
                  pitch = call(sound, "To Pitch", 0.0, 50.0, 600.0)
                  min_freq = call(pitch, "Get minimum", sound.xmin, sound.xmax, "Hertz", "Parabolic")
                  max_freq = call(pitch, "Get maximum", sound.xmin, sound.xmax, "Hertz", "Parabolic")
                  avg_freq_st.append((min_freq + max_freq)/2)
            
            avg_freq_st = rem_nan(avg_freq_st)
            avg_freq_st = sum(avg_freq_st)/len(avg_freq_st)
            
            row = {"stnum" : n,
                   "room" : r,
                   "freq_st" : avg_freq_st,
                   "freq_par" : avg_freq_par,
                   "freq_diff" : abs(avg_freq_par - avg_freq_st),
                   "dur_laugh_st" : 0.0,
                   "num_laugh_st" : 0,
                   "dur_laugh_par" : 0.0,
                   "num_laugh_st" : 0,
                   "ratio_voiced" : 0.0,
                   "familiarity": familiarity[r][0]}
            
            data = data.append(row, ignore_index = True)


# After the initial dataframe is ready this part gets the freq_diff betn participant and student
# Assuming it repeats participant, student, participant, ...
# for idx in range(0,len(data)-1,2):
#       avg_p = data.loc[idx,"avg_freq"]
#       avg_s = data.loc[idx + 1,"avg_freq"]
#       freq_diff = abs(avg_p - avg_s)
#       data.at[idx, "freq_diff"] = freq_diff
#       data.at[idx+1, "freq_diff"] = freq_diff

            
# Output to csv
data.to_csv("freq_aggregate_opt2.csv")