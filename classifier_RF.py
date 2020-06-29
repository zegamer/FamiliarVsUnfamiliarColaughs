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

# feature_std_scaled = StandardScaler().fit_transform(features)
feature_robust_scaled = RobustScaler().fit_transform(features)

familiarity = data.iloc[:,9].values

# Converting class labels as numeric as it can compute better
encoder = LabelEncoder().fit(familiarity)
familiarity = encoder.transform(familiarity)

# Will be later used to decode
# encoder.inverse_transform(predicted_vals)

# Splitting dataset into test and train
# features_train, features_test, familiarity_train, familiarity_test = train_test_split(feature_std_scaled, familiarity, train_size = 0.8)
features_train, features_test, familiarity_train, familiarity_test = train_test_split(feature_robust_scaled, familiarity, train_size = 0.8)

# RF classifier with optimum parameters
classifier_RF = RandomForestClassifier(n_estimators = 32, max_depth = 8, min_samples_split = 0.6, min_samples_leaf = 0.2, max_features = 5, n_jobs=-1).fit(features_train, familiarity_train)
familiarity_predicted = classifier_RF.predict(features_test)
            
# Shows accuracy
print("Accuracy is {}%".format(accuracy_score(familiarity_test, familiarity_predicted) * 100))
