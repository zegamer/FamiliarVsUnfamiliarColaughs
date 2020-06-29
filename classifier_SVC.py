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

# Will be later used to decode
# encoder.inverse_transform(predicted_vals)

# Splitting dataset into test and train
features_train, features_test, familiarity_train, familiarity_test = train_test_split(feature_std_scaled, familiarity, train_size = 0.8)
# features_train, features_test, familiarity_train, familiarity_test = train_test_split(feature_robust_scaled, familiarity, train_size = 0.8)

# SV classifier
classifier_SV = SVC(kernel='sigmoid', gamma=100, C=10).fit(features_train, familiarity_train)
familiarity_predicted = classifier_SV.predict(features_test)


# Show accuracy
# plot_confusion_matrix(classifier_SV, features_test, familiarity_test, labels = [0, 1])
print("Accuracy is {}%".format(accuracy_score(familiarity_test, familiarity_predicted) * 100))
