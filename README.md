# Familiar vs unfamiliar co-laughs

This program identifies whether 2 people are familiar or unfamiliar with each other based on the type of their co-laughter (simultaneous laughter). It is a was made by 4 students for the Affective Computing course at the University of Twente. Read the [paper] for further details. Furthermore, the program used a specialized annotated conversation database created by the students of the course which consisted of around 25 students and each student conversing with two different people outside the course. Despite having multiple conversation data, colaughs were rarely present in any of them, which limited the program performance.

## Features
- Built using Python, Praat and ELAN (to annotate audio segments).
- Finds best-fit parameters for 2 different classifiers, Random Forests and SVM.
- Accuracy of 77.5% with SVM.

## Libraries
- [pympi] - Python interface for ELAN
- [pydub] - Audio manipulation
- [Parselmouth] - Python interface for Praat functions

## Installation

This program requires Python 3.7 [[Download]] to work.

#### Cloning repository
Either download from [here] or use the git shell.  
```sh
$ git clone https://github.com/zegamer/FamiliarVsUnfamiliarColaughs.git
```

#### Installing libraries
The repository includes a requirements.txt file which contains all the libraries which are not present in the default python installation.
```sh
$ cd FamiliarVsUnfamiliarColaughs-master
$ pip install -r requirements.txt
```

#### Running the program
The program needs to be run in separate parts.

Once the database is set up as in the example folder, run wav_splitter.py. This will require reader.csv (see the example reader.csv file)
```sh
$ cd FamiliarVsUnfamiliarColaughs-master
$ python wav_splitter.py
```

All the colaugh audios will have been split in the respective folders.
Next run feature_extraction.py. This outputs 3 files, namely the 3 modes.
```sh
$ python feature_extraction.py
```

We then have to obtain the best-fit parameters for each of the classifier. These lines will output files that will contain the top 10 best-fit parameters.
```sh
$ python best_fit_RF.py
$ python best_fit_SVC.py
```

Using the best-fit parametes we run the classifier files. These will output the accuracies of the models and respective predictions.
```sh
$ python classifier_RF.py
$ python classifier_SVC.py
```

## Licence

The code is **open source** under MIT Licence.  
Check licence file in the repository.

For further questions, you can reach at m.v.konda@student.utwente.nl

[Download]: <https://www.python.org/downloads/>
[paper]: <https://drive.google.com/file/d/1mZR6fV57cB9oLMoh6NftXnRLrZWO_oqN/view?usp=sharing>
[here]: <https://github.com/zegamer/FamiliarVsUnfamiliarColaughs.git>
[pympi]: <https://github.com/dopefishh/pympi>
[pydub]: <https://github.com/jiaaro/pydub>
[Parselmouth]: <https://parselmouth.readthedocs.io/en/stable/>
