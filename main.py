import pandas as pd
from random import *
import numpy as np
import matplotlib.pyplot as pp





def leave_one_out_cross_validation(data, current_set, feature_to_add, action):
    cols = []
    if action == 1:
        cols = [feature_to_add]
        for member in current_set:
            cols.append(member)
    else:
        for i in range(len(data.columns)):
            cols.append(i)
        for member in current_set:
            cols.remove(member)
        cols.remove(feature_to_add)
    classes = data[data.columns[0]]
    data = data[data.columns[cols]]
    correct = 0
    for index, row in data.iterrows():
        min_distance = 900000000
        min_point = -1
        for second_index, second_row in data.iterrows():
            if second_index != index:
                # print("calculating the distance from %d th point to %d th point" % (index, second_index,))
                dist = 0
                for i in range(len(data.columns)):
                    dist += np.square(row.iloc[i] - second_row.iloc[i])
                dist = np.sqrt(dist)
                if dist < min_distance:
                    min_distance = dist
                    min_point = second_index
        if classes[index] == classes[min_point]:
            correct += 1
    return correct/len(data.index)


def feature_search_forward(data):
    feature_count = len(data.columns)-1
    added_features = set()
    best_so_far_accuracy = 0
    best_features_so_far = set()
    for i in range(1, feature_count):
        print("On the '%d'th level of the search tree" % i)
        best_round_accuracy = 0
        best_member_so_far = -1
        for k in range(1, feature_count):
            print("--Considering adding the '%d' feature" % k)
            if k in added_features:
                print("feature already in the set")
                continue
            accuracy = leave_one_out_cross_validation(data, added_features, k, 1)
            print("accuracy is %.5f" %accuracy)
            print("best so far accuracy is %.5f" %best_round_accuracy)
            if accuracy > best_round_accuracy:
                print("replaceing best so far")
                best_round_accuracy = accuracy
                best_member_so_far = k
        added_features.add(best_member_so_far)
        print("This level accuracy is %.5f"%best_round_accuracy)
        if best_round_accuracy <= best_so_far_accuracy:
            print("accuracy decreased, will continue in case of global best")
        else:
            best_features_so_far = added_features.copy()
            best_so_far_accuracy = best_round_accuracy
    print("best accuracy is %.5f" % best_so_far_accuracy)
    print("best members are:")
    print(best_features_so_far)


def feature_search_backwards(data):
    feature_count = len(data.columns) - 1
    removed_features = set()
    best_so_far_accuracy = 0
    best_features_so_far = set()
    level_accuracies = []
    for i in range(1, feature_count):
        best_features_so_far.add(i)
    for i in range(1, feature_count):
        print("On the '%d'th level of the search tree" % i)
        best_round_accuracy = 0
        best_member_so_far = -1
        for k in range(1, feature_count):
            print("--Considering removing the '%d' feature" % k)
            if k in removed_features:
                print("feature already removed")
                continue
            accuracy = leave_one_out_cross_validation(data, removed_features, k, -1)
            print("accuracy is %.5f" % accuracy)
            print("best so far accuracy is %.5f" % best_round_accuracy)
            if accuracy > best_round_accuracy:
                print("replaceing best so far")
                best_round_accuracy = accuracy
                best_member_so_far = k
            removed_features.add(best_member_so_far)
            print("This level accuracy is %.5f" % best_round_accuracy)
            level_accuracies.append(best_round_accuracy)
            if best_round_accuracy <= best_so_far_accuracy:
                print("accuracy decreased, will continue in case of global best")
            else:
                best_features_so_far = removed_features.copy()
                best_so_far_accuracy = best_round_accuracy
        print("best accuracy is %.5f" % best_so_far_accuracy)
        print("best members are:")
        best_feaures_add = []
        for i in range(1, feature_count):
            if i in best_features_so_far:
                continue
            best_feaures_add.append(i)
        print(best_feaures_add)
        pp.plot(level_accuracies)
        pp.show()


if __name__ == '__main__':
    largeFile = "CS205_large_testdata__27.txt"
    smallFile = "CS205_small_testdata__7.txt"
    df = pd.read_fwf(smallFile)
    data = pd.DataFrame(df)
    feature_search_backwards(data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
