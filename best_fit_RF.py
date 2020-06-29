from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

data = pd.read_csv('output.csv')

features = data.iloc[:,3:9].values

# Scalers normalize the values feature values (bring to same scale) so that it can compute better
# There's multiple kinds of scalers available but I tried the standard and robust ones alternatively

feature_std_scaled = StandardScaler().fit_transform(features)
# feature_robust_scaled = RobustScaler().fit_transform(features)


familiarity = data.iloc[:,9].values

# Converting class labels as numeric as it can compute better
encoder = LabelEncoder().fit(familiarity)
familiarity = encoder.transform(familiarity)

# Will be later used to decode
# encoder.inverse_transform(predicted_vals)

# Splitting dataset into test and train
features_train, features_test, familiarity_train, familiarity_test = train_test_split(feature_std_scaled, familiarity, train_size = 0.8)
# features_train, features_test, familiarity_train, familiarity_test = train_test_split(feature_robust_scaled, familiarity, train_size = 0.8)


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
max_features = list(range(1,features_train.shape[1], 2))

accuracies = pd.DataFrame(columns=['accuracy','n_estimators','max_depth','min_samples_split','min_samples_leaf', 'max_features'])

# Just a visual reference tracker to see how long the loop will last
count = len(n_estimators) * len(max_depth) * len(min_samples_splits) * len(min_samples_leafs) * len(max_features)

for n_e in n_estimators:
      for d in max_depth:
            for s in min_samples_splits:
                  for l in min_samples_leafs:
                        for f in max_features:
                              classifier_RF = RandomForestClassifier(n_estimators = n_e, max_depth = d, min_samples_split = s, min_samples_leaf = l, max_features = f, n_jobs=-1).fit(features_train, familiarity_train)
                              familiarity_predicted = classifier_RF.predict(features_test)
                              accuracies = accuracies.append({
                                    "accuracy": accuracy_score(familiarity_test, familiarity_predicted) * 100,
                                    "n_estimators" : n_e,
                                    "max_depth": d,
                                    "min_samples_split" : s,
                                    "min_samples_leaf" : l,
                                    "max_features" : f
                                    }, ignore_index=True)
                              print(count)
                              count -= 1
                  
            
# Shows top 10 fit parameters that can be used
best_fits = accuracies.nlargest(10, ["accuracy"])
# print(best_fits)
