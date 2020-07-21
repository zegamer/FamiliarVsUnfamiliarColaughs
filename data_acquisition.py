import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler, LabelEncoder
from sklearn.model_selection import train_test_split


def get_data(mode = 2, alternate = False, robust_scaler = False):

      data = pd.read_csv('{}output_mode_{}.csv'.format('alt_' if alternate else '', mode))
      
      if mode == 3:
           features = data.iloc[:,3:7].values
           familiarity = data.iloc[:,7].values
      else:
            if alternate:
                  if mode == 1:
                        features = data.iloc[:,2:10].values
                        familiarity = data.iloc[:,10].values
                  
                  if mode == 2:
                        features = data.iloc[:,3:7].values
                        familiarity = data.iloc[:,7].values
            else:
                  if mode == 1:
                        features = data.iloc[:,2:11].values
                        familiarity = data.iloc[:,11].values
                  
                  if mode == 2:
                        features = data.iloc[:,3:9].values
                        familiarity = data.iloc[:,9].values

      # Scalers normalize the values feature values (bring to same scale) so that the data can be computed better
      features = RobustScaler().fit_transform(features) if robust_scaler else StandardScaler().fit_transform(features)
            
      # Converting class labels as numeric as it can compute better
      familiarity = LabelEncoder().fit_transform(familiarity)
      
      return [features, familiarity]


def get_split_data(mode = 2, alternate = False):

      features, familiarity = get_data(mode = mode, alternate = alternate)
      feat_tr, feat_te, fam_tr, fam_te = train_test_split(features, familiarity, train_size = 0.8)
      
      return [feat_tr, feat_te, fam_tr, fam_te]


def write_to_csv(data, name, mode = 2, alternate = False):
      data.to_csv('{}{}_mode_{}.csv'.format('alt_' if alternate else '', name, mode), index = False)

      
      