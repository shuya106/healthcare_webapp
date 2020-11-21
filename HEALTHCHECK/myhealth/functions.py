import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


class DecisionTreeClass():

    def __init__(self):
        self.le = LabelEncoder()
        self.dtc = DecisionTreeClassifier()

    def fit(self, max_temp_list, weather_list, condition_list):
        self.le.fit(['晴','曇', '雨', '晴時々曇', '雨のち曇'])
        weather_list = self.le.transform(weather_list)

        max_temp_list = np.array(max_temp_list)
        weather_list = np.array(weather_list)
        t = np.array(condition_list)

        X1 = max_temp_list.reshape(-1, 1)
        X2 = weather_list.reshape(-1, 1)

        Xdata = np.concatenate([X1, X2], axis=1)

        self.dtc.fit(Xdata, t)

        return self.dtc

    def predict(self, max_temp, weather):

        weather = [weather]
        weather = self.le.transform(weather)
        max_temp = np.array(max_temp)



        X1 = max_temp.reshape(-1, 1)
        X2 = weather.reshape(-1, 1)

        Xdata = np.concatenate([X1, X2], axis=1)

        y = self.dtc.predict(Xdata)

        return y

    def featureimportance(self):
        most_importance = np.argmax(self.dtc.feature_importances_)
        if most_importance == 0:
            most_feature = '最高気温'
        else:
            most_feature = '天気'

        return most_feature