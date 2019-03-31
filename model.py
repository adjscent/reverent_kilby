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
        transformed_data = filter_data.groupby(
            ['current_day'], as_index=False).mean()
        train_data = transformed_data[symptoms].values
        tree = spatial.KDTree(train_data)

        result = tree.query(new_sym)
        if i == cycle:
            distances.append(
                (result[0]*weight_for_own_cycle, filter_data.iloc[result[1]]))
        else:
            distances.append((result[0], filter_data.iloc[result[1]]))

    distances = sorted(distances, key=lambda t: t[0], reverse=False)
    return distances[0][1]

