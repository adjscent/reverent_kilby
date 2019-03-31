'''
Data Loading and Normalisation
'''

import datetime
import math
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.sparse import csgraph
from sklearn import neighbors
import numpy as np
from scipy import spatial
import pprint

from data import *
from constants import *


def predict(new_sym, cycle):
    listOfCycleLengths = sorted(new_data["cycle_length_initial"].unique())

    distances = []

    for i in listOfCycleLengths:
        filter_data = new_data.loc[new_data.cycle_length_initial == i]
        data = filter_data[symptoms]
        train_data = data.mul(symptoms_weight, axis=1).values

        tree = spatial.KDTree(train_data)

        result = tree.query(new_sym)
        if i == cycle:
            distances.append(
                (result[0]*weight_for_own_cycle, filter_data.iloc[result[1]]))
        else:
            distances.append((result[0], filter_data.iloc[result[1]]))

    distances = sorted(distances, key=lambda t: t[0], reverse=False)
    return distances[0][1]


def test():
    wrong = 0.
    correct = 0.
    for i in range(len(X_test)):
        r = predict(X_test[symptoms].iloc[i],
                    X_test["cycle_length_initial"].iloc[i])

        if ((X_test["current_day"].iloc[i] / X_test["cycle_length_initial"].iloc[i]) - (r["current_day"] / r["cycle_length_initial"]) <= 0.1):
            correct += 1
        else:
            wrong += 1
    print(symptoms_weight)
    print(correct/(correct+wrong))
