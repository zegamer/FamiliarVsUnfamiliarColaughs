from sklearn.ensemble import RandomForestClassifier
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
      data = pd.read_csv('{}output_mode_{}.csv'.format('alt_' if alternate else '', mode))
      
      
      best_fit = pd.read_csv('{}best_fit_RF_mode_{}.csv'.format('alt_' if alternate else '', mode))
      importance = []
      
      for _ in range(5):
            
            features_train, features_test, familiarity_train, familiarity_test = get_split_data(mode, alternate)
            
            classifier_RF = RandomForestClassifier(n_estimators = int(best_fit['n_estimators'][model_no]),
                                                   max_depth = int(best_fit['max_depth'][model_no]),
                                                   min_samples_split = best_fit['min_samples_split'][model_no],
                                                   min_samples_leaf = best_fit['min_samples_leaf'][model_no],
                                                   max_features = int(best_fit['max_features'][model_no]),
                                                   n_jobs=-1).fit(features_train, familiarity_train)
                 
            familiarity_predicted = classifier_RF.predict(features_test)
            accuracy.append(accuracy_score(familiarity_test, familiarity_predicted))
            importance.append(classifier_RF.feature_importances_)
      
      # Show accuracy
      print("Min: {},\t Max: {},\t Avg: {}% for mode {}, alternate {}".format(min(accuracy) * 100 , max(accuracy) * 100, np.average(accuracy) * 100, mode, alternate))
      
      importance = np.average(importance, axis = 0)

      for i in range(len(importance)):
            print("Feature: %d,\t Score: %.5f" % (i+1, importance[i]))
