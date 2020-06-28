import parselmouth as pm
from parselmouth.praat import call
from glob import glob
import pandas as pd

stnum = ['512', '3629', '6110', '6468', '9198']
room = ['A', 'B']
stu_part = ['participant', 'student']

data = pd.DataFrame(columns=["stnum", "room", "stu_part", "min_freq", "max_freq", "avg_freq", "freq_diff", "familiarity"])


# Replaces nan values in the list with the average of the list
def rem_nan(val):
      val = pd.DataFrame(val)
      val = pd.DataFrame.fillna(val, val.mean())
      return list(val[0])


for n in stnum:
      
      # Familiarity is based on a familiarity.txt
      # This is because, familiarity is not always same for all students
      familiarity = pd.read_csv(n + "/familiarity.txt")
      
      for r in room:
            for sp in stu_part:
                  
                  # Debug values
                  # n, r, sp = stnum[0], room[1], stu_part[0]
                  
                  # Using a max n min list to get the overall max and min from all simultaneous audios
                  min_freq, max_freq, avg_freq = [],[],[]
                  
                  for wav in glob(n + "/" + r + "/" + sp + "/* - simultaneous.wav"):
                        sound = pm.Sound(wav)
                        pitch = sound.to_pitch(pitch_floor = 50.0, pitch_ceiling = 600.0)
                        pitch = call(sound, "To Pitch", 0.0, 50.0, 600.0)
                        min_freq.append(call(pitch, "Get minimum", sound.xmin, sound.xmax, "Hertz", "Parabolic"))
                        max_freq.append(call(pitch, "Get maximum", sound.xmin, sound.xmax, "Hertz", "Parabolic"))
                  
                  max_freq = rem_nan(max_freq)
                  min_freq = rem_nan(min_freq)
                  
                  # Use min n max from each row to get better avg
                  for i in range(len(min_freq)):
                        avg_freq.append((max_freq[i] + min_freq[i]) / 2)
                  
                  row = {"stnum" : n, "room" : r, "stu_part" : sp, "min_freq" : min(min_freq), "max_freq" : max(max_freq), "avg_freq": sum(avg_freq)/len(avg_freq), "familiarity":familiarity[r][0]}
                  data = data.append(row, ignore_index = True)


# After the initial dataframe is ready this part gets the freq_diff betn participant and student
# Assuming it repeats participant, student, participant, ...
for idx in range(0,len(data)-1,2):
      avg_p = data.loc[idx,"avg_freq"]
      avg_s = data.loc[idx + 1,"avg_freq"]
      freq_diff = abs(avg_p - avg_s)
      data.at[idx, "freq_diff"] = freq_diff
      data.at[idx+1, "freq_diff"] = freq_diff

            
# Output to csv
data.to_csv("freq_aggregate_opt1.csv")