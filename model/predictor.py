import pandas
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle


class Predictor:
    def __init__(self, data_frame):
        self.titles = pandas.DataFrame(data_frame['TITLE']).reset_index(drop=True)
        self.data_frame = data_frame.drop(columns=['TITLE'], axis=1)

    def make_predict(self):
        """
        Предикт
        :return: pandas.DataFrame
        """
        model = pickle.load(open('model/random_forest.sav', 'rb'))
        predict = model.predict_proba(X=self.data_frame)[:, 1]
        print(model.predict_proba(X=self.data_frame))
        predict = (pandas.Series(predict)*100).rename('PREDICT')
        result_df = pandas.concat([self.titles, predict], axis=1)
        return result_df.to_dict(orient='records')
