from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, RobustScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

data = pd.read_csv('output.csv')

features = data.iloc[:,3:9].values
feature_std_scaled = StandardScaler().fit_transform(features)
# feature_robust_scaled = RobustScaler().fit_transform(features)

familiarity = data.iloc[:,9].values
# familiarity = data.iloc[:,9:10].values
encoder = LabelEncoder().fit(familiarity)
familiarity = encoder.transform(familiarity)
# familiarity = OneHotEncoder().fit_transform(familiarity).toarray()

# Will be later used to decode
# encoder.inverse_transform(predicted_vals)

# Splitting dataset into test and train
features_train, features_test, familiarity_train, familiarity_test = train_test_split(feature_std_scaled, familiarity, train_size = 0.8)
# features_train, features_test, familiarity_train, familiarity_test = train_test_split(feature_robust_scaled, familiarity, train_size = 0.8)

# SV classifier
# Tring out multiple parameters to find best fit - 256 combos
kernels = ['poly', 'rbf', 'sigmoid', 'linear']
gamma = [0.1, 1, 10, 100]
penalty = [0.1, 1, 10, 100]
degree = [2,3,4,5]

accuracies = pd.DataFrame(columns=['accuracy','kernel','gamma','penalty','degree'])

# Just a visual reference tracker to see how long the loop will last
count = len(kernels) * len(gamma) * len(penalty) * len(delta)

for k in kernels:
      for c in penalty:
            if k =='linear':
                  classifier_SV = SVC(kernel=k, C=c).fit(features_train, familiarity_train)
                  familiarity_predicted = classifier_SV.predict(features_test)
                  accuracies = accuracies.append({"accuracy": accuracy_score(familiarity_test, familiarity_predicted) * 100, "kernel":k, "penalty":c}, ignore_index=True)
                  print(count)
                  count -= 1
                  
            else:
                  for g in gamma:
                        if k == 'poly': 
                              for d in degree:
                                    classifier_SV = SVC(kernel=k, C=c, gamma=g, degree=d).fit(features_train, familiarity_train)
                                    familiarity_predicted = classifier_SV.predict(features_test)
                                    accuracies = accuracies.append({"accuracy": accuracy_score(familiarity_test, familiarity_predicted) * 100, "kernel":k, "penalty":c, "gamma":g, "degree":d}, ignore_index=True)
                                    print(count)
                                    count -= 1

                        else:
                              classifier_SV = SVC(kernel=k, C=c, gamma=g).fit(features_train, familiarity_train)
                              familiarity_predicted = classifier_SV.predict(features_test)
                              accuracies = accuracies.append({"accuracy": accuracy_score(familiarity_test, familiarity_predicted) * 100, "kernel":k, "penalty":c, "gamma":g}, ignore_index=True)
                              print(count)
                              count -= 1
            
# Show top 10 best fit parametes
best_fits = accuracies.nlargest(10, ["accuracy"])
# print(best_fits)
# best_fits = accuracies.loc[accuracies["accuracy"] == max(accuracies['accuracy'])]

# best_fits.to_csv('best_fits_SVC.csv', index=False)
