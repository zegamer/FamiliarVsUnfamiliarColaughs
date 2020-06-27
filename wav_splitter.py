import os
from pandas import read_csv
from pympi import Elan
from pydub import AudioSegment

reader = read_csv('reader.csv')

for idx, row in reader.iterrows():
      
      input_folder = str(row["input_folder"])
      
      files = {
          "eaf" : input_folder + '/' + row['input_eaf'],
          "audio" : input_folder + '/' + row['input_wav']
          }
      
      target = {
          "stu_part" : row['stu_part'],
          "op_folder" : input_folder + '/' + row['output_folder'],
          "file_prefix" : "",
          "file_suffix" : "",
          "tier" : "tier3",
          "type" : ['simultaneous']
          }
      
      # Last moment addidion, didn't test yet
      # Comment if causes errors
      try:                  
            os.makedirs(target["op_folder"] + '/' + target["stu_part"])
      except FileExistsError:
            pass
      
      print("\nSTART___________________________________________________________________________________________")
      
      # Extract tier 3 annotations from the eaf file
      eaf_file = Elan.Eaf(files["eaf"])
      t3_annots = eaf_file.get_annotation_data_for_tier(target["tier"])
      
      # Selective split the audio file based on co-laughs
      print("Writing to - " + target["op_folder"] + '/' + target["stu_part"])
      audio = AudioSegment.from_wav(files["audio"])
      num_simul = 0
      for i in range(len(t3_annots)):
            (start, end, laugh_type) = (t3_annots[i][0], t3_annots[i][1], t3_annots[i][2])
            try:
                  if (laugh_type in target["type"]):
                        laugh = laugh_type.replace('/','_')
                        file_name = str(target["file_prefix"] + str(start/1000) + ' - ' + str(end/1000) + ' - ' + laugh + target["file_suffix"] + ".wav")
                        op = target["op_folder"] + '/' + target["stu_part"] + '/' + file_name
                        split = audio[start:end]
                        split.export(out_f = op, format='wav')
                        print("Saved as : " + file_name)
                        num_simul += 1
            except Exception as e:
                  print(file_name + " encountered error : " + str(e))
      print("END********** Simultaneous = " + str(num_simul)+ " **************************************************\n")
            