from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

class RandomForestRegressor:
    """
    - Good at learn non-linearities;
    - Easy to interpret;
    - Computationally expensive for large forests;

    Reference: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
    """
    def get_model(self):
        return RandomForestRegressor()

class MLPRegressor:
    """
    Reference: https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html#sklearn.neural_network.MLPRegressor
    """
    def get_model(self):
        return MLPRegressor()

class KNNRegressor:
    """
    Reference: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html
    """
    def get_model(self):
        return KNeighborsRegressor()

class SVMRegressor:
    """
    Reference: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html
    """
    def get_model(self):
        return SVR()

class XGBoostRegressor:
    pass