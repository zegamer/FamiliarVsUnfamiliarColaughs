from sklearn.svm import SVC
from sklearn import svm
from sklearn.metrics import accuracy_score
import pandas as pd
from data_acquisition import get_split_data
import numpy as np

accuracy = []
model_no = 0

for mode in [1,2,3]:
      # for alternate in [True, False]:
            
      #       if alternate and mode == 3:
      #             continue
            
      alternate = False
      best_fit = pd.read_csv('{}best_fit_SVC_mode_{}.csv'.format('alt_' if alternate else '', mode))
      importance = []
      
      for _ in range(5):
            
            alternate = False
            features_train, features_test, familiarity_train, familiarity_test = get_split_data(mode, alternate)

            # SV classifier
            classifier_SV = SVC(
                  kernel= best_fit['kernel'][model_no],
                  gamma = best_fit['gamma'][model_no] if best_fit['gamma'][model_no] in ['auto', 'scale'] else float(best_fit['gamma'][model_no]),
                  C = best_fit['penalty'][model_no],
                  degree = 3 if pd.isna(best_fit['degree'][model_no]) else best_fit['degree'][model_no]
            ).fit(features_train, familiarity_train)
            
            familiarity_predicted = classifier_SV.predict(features_test)
            accuracy.append(accuracy_score(familiarity_test, familiarity_predicted))

      # Show accuracy
      print("Min: {},\t Max: {},\t Avg: {}% for mode {}, alternate {}".format(min(accuracy) * 100 , max(accuracy) * 100, np.average(accuracy) * 100, mode, alternate))
