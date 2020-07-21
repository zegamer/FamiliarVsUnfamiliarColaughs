from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd
from data_acquisition import get_split_data, write_to_csv

for mode in [1,2,3]:
      # for alternate in [True, False]:

      #       if alternate and mode == 3:
      #             continue

      alternate = False
      
      features_train, features_test, familiarity_train, familiarity_test = get_split_data(mode, alternate)
      
      # SV classifier
      # Trying out multiple parameters to find best fit - 256 combos
      kernels = ['poly', 'rbf', 'sigmoid', 'linear']
      gamma = [0.1, 1, 10, 100, 'auto', 'scale']
      penalty = [0.1, 1, 10, 100]
      degree = [2,3,4,5]
      
      accuracies = pd.DataFrame(columns=['accuracy','kernel','gamma','penalty','degree'])
      
      # Just a visual reference tracker to see how long the loop will last
      count = len(kernels) * len(gamma) * len(penalty) * len(degree)
      
      for k in kernels:
            for c in penalty:
                  if k =='linear':
                        print('{}: \tk: {},\tg: {},\tp: {},\td: {}'.format(count, k, 0, c, 0))
                        classifier_SV = SVC(kernel=k, C=c).fit(features_train, familiarity_train)
                        familiarity_predicted = classifier_SV.predict(features_test)
                        accuracies = accuracies.append({"accuracy": accuracy_score(familiarity_test, familiarity_predicted), "kernel":k, "penalty":c}, ignore_index=True)
                        count -= 1
                        
                  else:
                        for g in gamma:
                              if k == 'poly': 
                                    if g in[10,100]:
                                          break
                                    for d in degree:
                                          
                                          
                                          print('{}:\tk: {},\tg: {},\tp: {},\td: {}'.format(count, k, g, c, d))
                                          classifier_SV = SVC(kernel=k, C=c, gamma=g, degree=d).fit(features_train, familiarity_train)
                                          familiarity_predicted = classifier_SV.predict(features_test)
                                          accuracies = accuracies.append({"accuracy": accuracy_score(familiarity_test, familiarity_predicted), "kernel":k, "penalty":c, "gamma":g, "degree":d}, ignore_index=True)
                                          count -= 1
      
                              else:
                                    print('{}:\tk: {},\tg: {},\tp: {},\td: {}'.format(count, k, g, c, 0))
                                    classifier_SV = SVC(kernel=k, C=c, gamma=g).fit(features_train, familiarity_train)
                                    familiarity_predicted = classifier_SV.predict(features_test)
                                    accuracies = accuracies.append({"accuracy": accuracy_score(familiarity_test, familiarity_predicted), "kernel":k, "penalty":c, "gamma":g}, ignore_index=True)
                                    count -= 1
                  
      # Show top 10 best fit parametes
      best_fits = accuracies.nlargest(10, ["accuracy"])
      
      print("\nAverage accuracy mode {}, alternate {} is {}%\n\n".format(mode, alternate, (sum(best_fits['accuracy'])/len(best_fits['accuracy'])) * 100))
      # print()
      # print(best_fits)
      
      write_to_csv(best_fits, 'best_fit_SVC', mode, alternate)