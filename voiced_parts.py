import parselmouth as par
import os
import glob
import pandas as pd

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 500)
all_files  = os.listdir('Data/')

list_of_stnumb = ['512', '3629', '6110', '6468', '9198']
rooms = ['A', 'B']
stuffs = ['participant', 'student']

data = {'number':[],
        'student': [],
        'familiar':[],
        'voiced': [],
        'duration': [],
        'amount_of_laughs': []}

frame = pd.DataFrame(data)

def extract_features(number, room, stuff):
    all_voiced = []
    all_duration = []
    count = 0
    for wav_file in glob.glob(number + "/" + room + "/" + stuff + "/*- simultaneous.wav"):
        sound = par.Sound(wav_file)
        voiced_frames = par.Pitch.count_voiced_frames(sound.to_pitch())
        total_frames = sound.get_number_of_frames()
        part_voiced = voiced_frames / total_frames
        total_duration = sound.get_total_duration()
        count += 1

        all_voiced.append(part_voiced)
        all_duration.append(total_duration)
    
    for i in range(len(all_voiced)):
        frame.loc[len(frame.index)] =  pd.Series(data={'number':number, 'student':stuff, 'familiar':room, 'voiced':str(all_voiced[i]), 'duration': all_duration[i], 'amount_of_laughs':count}, name = 'x')

for numb in list_of_stnumb:
    for room in rooms:
        for stuff in stuffs:
            extract_features(numb, room, stuff)

print(frame)
frame.to_csv('output.csv')
