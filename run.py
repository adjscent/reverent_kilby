import datetime
import math
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.sparse import csgraph
from sklearn import neighbors


new_data = pd.merge(period_data, symptom_data, left_on='User_id', right_on='user_id', how='inner')
new_data= pd.merge(new_data, user_data, left_on='User_id', right_on='id', how='inner')
new_data.drop(columns=['User_id', 'id'], inplace=True)

new_data = new_data.query('end_date > start_date')
new_data["last_date"] = new_data["end_date"] + pd.to_timedelta(new_data["cycle_length_initial"], unit='D') - pd.to_timedelta(new_data["period_length_initial"], unit='D')
new_data["current_day"] = (abs(  (new_data["date"] -  new_data['start_date']).dt.days))
new_data = new_data[new_data.current_day > 0]
new_data = new_data[new_data.current_day < new_data.cycle_length_initial]
new_data["stage"] = new_data["current_day"] / new_data["cycle_length_initial"]

train_data = new_data[["acne","backache","bloating","cramp","diarrhea","dizzy","headache","mood","nausea","sore"]].values
train_truth = new_data[["user_id","stage"]].values

# #0-0.25
# part1 = new_data.loc[(new_data['stage'] <= 0.25) ]
# #0.25-0.5
# part2 = new_data.loc[(new_data['stage'] > 0.25) & (new_data['stage'] < 0.5) ]
# #0.5-1
# part3 = new_data.loc[(new_data['stage'] >= 0.5) ]



kmeans = KMeans(n_clusters=8, random_state=0).fit(train_data)

# !! Get the indices of the points for each corresponding cluster
mydict = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}

# Transform the dictionary into list
dictlist = []
for key, value in mydict.items():
    dictlist.append(len(value))
    
print("Total points")
print(len(train_data))

print("Number of points in each cluster")
arr = []
for i in range(len(dictlist)):
    arr.append([int(dictlist[i]),kmeans.cluster_centers_[i]])
arr = sorted(arr,key=lambda x: x[0])
for i in arr:
    print (str(i[0]) + " " + str(i[1]))
    plt.plot(i[1])

plt.grid()
