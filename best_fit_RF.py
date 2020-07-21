from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
from data_acquisition import get_split_data, write_to_csv


for mode in [1,2,3]:
      # for alternate in [True, False]:

      #       if alternate and mode == 3:
      #             continue
     
      features_train, features_test, familiarity_train, familiarity_test = get_split_data(mode)
      
      
      # Testing different parameter combinations to get the optimum combination
      
      # RF Extended parameters - 64000 combos ~ 4.5 hrs  to compute
      # n_estimators = [2, 4, 8, 16, 32, 64, 100, 200]
      # max_depth = np.linspace(1, 32, 32, endpoint=True)
      # min_samples_splits = np.linspace(0.1, 1.0, 10, endpoint=True)
      # min_samples_leafs = np.linspace(0.1, 0.5, 5, endpoint=True)
      # max_features = list(range(1,features_train.shape[1]))
      
      # Simplified parameters  - 324 combos ~ 1m 21s to compute
      n_estimators = [32, 64, 100, 200]
      max_depth = [8, 16, 32]
      min_samples_splits = [0.2, 0.6, 1.0]
      min_samples_leafs = [0.2, 0.4, 0.5]
      max_features = list(range(1,features_train.shape[1]))
      
      accuracies = pd.DataFrame(columns=['accuracy','n_estimators','max_depth','min_samples_split','min_samples_leaf', 'max_features'])
      
      # Just a visual reference tracker to see how long the loop will last
      count = len(n_estimators) * len(max_depth) * len(min_samples_splits) * len(min_samples_leafs) * len(max_features)
      
      for n_e in n_estimators:
            for d in max_depth:
                  for s in min_samples_splits:
                        for l in min_samples_leafs:
                              for f in max_features:
                                    # print('{}: \tn_e: {},\td: {},\ts: {},\tl: {}, \tf: {}'.format(count, n_e, d, s, l, f))
                                    classifier_RF = RandomForestClassifier(n_estimators = n_e, max_depth = d, min_samples_split = s, min_samples_leaf = l, max_features = f, n_jobs=-1).fit(features_train, familiarity_train)
                                    familiarity_predicted = classifier_RF.predict(features_test)
                                    accuracies = accuracies.append({
                                          "accuracy": accuracy_score(familiarity_test, familiarity_predicted),
                                          "n_estimators" : n_e,
                                          "max_depth": d,
                                          "min_samples_split" : s,
                                          "min_samples_leaf" : l,
                                          "max_features" : f
                                          }, ignore_index=True)
                                    count -= 1
                        
                  
      # Show top 10 best fit parametes
      best_fits = accuracies.nlargest(10, ["accuracy"])
      
      # print("\nAverage accuracy mode {}, alternate {} is {}%\n\n".format(mode, alternate, (sum(best_fits['accuracy'])/len(best_fits['accuracy'])) * 100))
      print("\nAverage accuracy mode {}, is {}%\n\n".format(mode, (sum(best_fits['accuracy'])/len(best_fits['accuracy'])) * 100))
      # print()
      # print(best_fits)
      
      write_to_csv(best_fits, 'best_fit_RF', mode)