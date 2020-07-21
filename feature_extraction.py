import parselmouth as par
from parselmouth.praat import call
import os
import glob
import pandas as pd

def rem_nan(val):
    val = pd.DataFrame(val)
    val = pd.DataFrame.fillna(val, val.mean())
    return list(val[0])

def extract_features_op1(number, room, frame):
        all_info = []
        
        familiarity = pd.read_csv("Data/" + number + "/familiarity.txt")
        
        for item in stuffs:
            all_voiced = []
            all_duration = []
            avg_freq = []
            count = 0
        
            for wav_file in glob.glob("Data/" + number + "/" + room + "/" + item + "/*- simultaneous.wav"):
                sound = par.Sound(wav_file)
                voiced_frames = par.Pitch.count_voiced_frames(sound.to_pitch())
                total_frames = sound.get_number_of_frames()
                part_voiced = voiced_frames / total_frames
                total_duration = sound.get_total_duration()
                count += 1

                pitch = sound.to_pitch(pitch_floor = 50.0, pitch_ceiling = 600.0)
                pitch = call(sound, "To Pitch", 0.0, 50.0, 600.0)
                min_freq = call(pitch, 'Get minimum', sound.xmin, sound.xmax, "Hertz", "Parabolic")
                max_freq = call(pitch, 'Get maximum', sound.xmin, sound.xmax, "Hertz", "Parabolic")
                avg_freq.append((min_freq + max_freq)/2)

                all_voiced.append(part_voiced)
                all_duration.append(total_duration)


            try: 
                avg_freq = rem_nan(avg_freq)
                avg_freq = sum(avg_freq) / len(avg_freq)

                all_info.append(sum(all_duration)/len(all_duration))
                all_info.append(count)            
                all_info.append(sum(all_voiced)/len(all_voiced))
                all_info.append(avg_freq)
            except:
                return
            
        frame.loc[len(frame.index)] =  pd.Series(data={
              'stnum' : number,
              'room' : room,
              'freq_st' : all_info[7],
              'freq_par' : all_info[3],
              'freq_diff' : abs(all_info[3]- all_info[7]),
              'dur_laughs_st' : all_info[4],
              'dur_laughs_par' : all_info[0],
              'num_laughs_st' : all_info[5],
              'num_laughs_par' : all_info[1],
              'ratio_voiced_st' : all_info[6],
              'ratio_voiced_par' : all_info[2],
              'familiarity' : familiarity[room][0]
              }, name = 'x')

def extract_features_op2(number, room, stuff, frame):
        all_info = []
        all_voiced = []
        all_duration = []
        min_freq, max_freq, avg_freq = [], [], []
        count = 0
        
        familiarity = pd.read_csv("Data/" + number + "/familiarity.txt")

        for wav_file in glob.glob("Data/" + number + "/" + room + "/" + stuff + "/*- simultaneous.wav"):
            sound = par.Sound(wav_file)
            voiced_frames = par.Pitch.count_voiced_frames(sound.to_pitch())
            total_frames = sound.get_number_of_frames()
            part_voiced = voiced_frames / total_frames
            total_duration = sound.get_total_duration()
            count += 1

            pitch = sound.to_pitch(pitch_floor=50.0, pitch_ceiling=600.0)
            pitch = call(sound, "To Pitch", 0.0, 50.0, 600.0)
            min_freq.append(call(pitch, "Get minimum", sound.xmin, sound.xmax, "Hertz", "Parabolic"))
            max_freq.append(call(pitch, "Get maximum", sound.xmin, sound.xmax, "Hertz", "Parabolic"))

            all_voiced.append(part_voiced)
            all_duration.append(total_duration)

        try:
              max_freq = rem_nan(max_freq)
              min_freq = rem_nan(min_freq)

              for i in range(len(min_freq)):
                    avg_freq.append((max_freq[i] + min_freq[i]) / 2)

              all_info.append(sum(all_duration) / len(all_duration))
              all_info.append(count)
              all_info.append(sum(all_voiced) / len(all_voiced))
        except:
            return

        frame.loc[len(frame.index)] =  pd.Series(data={
              'stnum' : number,
              'room' : room,
              'stu_par' : stuff,
              'min_freq' : min(min_freq),
              'max_freq': max(max_freq),
              'freq_diff': sum(avg_freq)/len(avg_freq), 
              'dur_laughs': all_info[0],
              'num_laughs': all_info[1],
              'ratio_voiced': all_info[2],
              'familiarity' : familiarity[room][0]
              }, name = 'x')
                     
def extract_features_option3(number, room, stuff):
    count = 0
    familiarity = pd.read_csv("Data/" + number + "/familiarity.txt")
    for single_audio_file in glob.glob("Data/" + number + "/" + room + "/" + stuff + "/*- simultaneous.wav"):
        sound = par.Sound(single_audio_file)
        voiced_frames = par.Pitch.count_voiced_frames(sound.to_pitch())
        total_frames = sound.get_number_of_frames()
        part_voiced = voiced_frames / total_frames
        total_duration = sound.get_total_duration()
        count+=1
        
        pitch = sound.to_pitch(pitch_floor=50.0, pitch_ceiling=600.0)
        pitch = call(sound, "To Pitch", 0.0, 50.0, 600.0)
        min_freq = call(pitch, 'Get minimum', sound.xmin, sound.xmax, "Hertz", "Parabolic")
        max_freq = call(pitch, 'Get maximum', sound.xmin, sound.xmax, "Hertz", "Parabolic")
        avg_freq = (min_freq + max_freq)/2
        
        try:
            frame.loc[len(frame.index)] = pd.Series(data = {
                  'stnum': number,
                  'room': room,
                  'stu_par': stuff,
                  'avg_freq': avg_freq,
                  'dur_laughs': total_duration,
                  'num_laughs': count,
                  'ratio_voiced': part_voiced,
                  'familiarity': familiarity[room][0]
                  }
                  , name = 'x')
        except:
            print("Excluded: " + room + numb + stuff)

for MODE in [1,2]:
      
      list_of_stnumb = list(os.listdir('Data'))
      rooms = ['A', 'B']
      stuffs = ['participant', 'student']
      
      if MODE == 1:
      
          data = {'stnum':[],
                  'room': [],
                  'freq_st': [],
                  'freq_par': [],
                  'freq_diff': [],
                  'dur_laughs_st' : [],
                  'dur_laughs_par' : [],
                  'num_laughs_st': [],
                  'num_laughs_par': [],
                  'ratio_voiced_st': [],
                  'ratio_voiced_par': [],
                  'familiarity' : []
                  }
      
          frame = pd.DataFrame(data)
      
          for numb in list_of_stnumb:
              for room in rooms:
                    print(numb, room)
                    extract_features_op1(numb, room, frame)
      
      if MODE == 2:
      
          data = {
              'stnum': [],
              'room': [],
              'stu_par': [],
              'min_freq': [],
              'max_freq': [],
              'freq_diff': [],
              'dur_laughs': [],
              'num_laughs': [],
              'ratio_voiced': [],
              'familiarity' : []
          }
          
          frame = pd.DataFrame(data)
          
          for numb in list_of_stnumb:
              for room in rooms:
                  for stuff in stuffs:
                        print(numb, room, stuff)
                        extract_features_op2(numb, room, stuff, frame)
      
      if MODE == 3:
            data = {
                  'stnum':[],
                  'room': [],
                  'stu_par':[],
                  'avg_freq':[],
                  'dur_laughs':[],
                  'num_laughs': [],
                  'ratio_voiced': [],
                  'familiarity': []
            }
            
            frame = pd.DataFrame(data)
            
            for numb in list_of_stnumb:
                  for room in rooms:
                        for stuff in stuffs:
                              print(numb, room, stuff)
                              extract_features_option3(numb, room, stuff)
            
      
            frame = frame[frame['avg_freq'].notna()]
      
      frame.to_csv('output_mode_{}.csv'.format(MODE), index = False)
      
