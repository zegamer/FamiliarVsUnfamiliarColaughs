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
        
        familiarity = pd.read_csv(number + "/familiarity.txt")
        
        for item in stuffs:
            all_voiced = []
            all_duration = []
            avg_freq = []
            count = 0
        
            for wav_file in glob.glob(number + "/" + room + "/" + item + "/*- simultaneous.wav"):
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
            except:
                avg_freq = 0

            try:
                all_info.append(sum(all_duration)/len(all_duration))
            except:
                all_info.append(0)
            
            all_info.append(count)
            
            try:
                all_info.append(sum(all_voiced)/len(all_voiced))
            except:
                all_info.append(0)
            
            all_info.append(avg_freq)

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
        
        familiarity = pd.read_csv(number + "/familiarity.txt")

        for wav_file in glob.glob(number + "/" + room + "/" + stuff + "/*- simultaneous.wav"):
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

        max_freq = rem_nan(max_freq)
        min_freq = rem_nan(min_freq)

        for i in range(len(min_freq)):
            avg_freq.append((max_freq[i] + min_freq[i]) / 2)

        try:
            all_info.append(sum(all_duration) / len(all_duration))
        except:
            all_info.append(0)

        all_info.append(count)

        try:
            all_info.append(sum(all_voiced) / len(all_voiced))
        except:
            all_info.append(0)

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


MODE = 2


list_of_stnumb = ['512', '3629', '5751', '6110', '6468']
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
                extract_features_op2(numb, room, stuff, frame)

frame.to_csv('output.csv', index = False)

