import pandas as pd
from random import *
import numpy as np
import matplotlib.pyplot as pp


def leave_one_out_cross_validation(data, current_set, feature_to_add, action):
    cols = []
    # Checks if it wants to remove or add column(Forward or backward selection)
    #Forward selection
    if action == 1:
        cols = [feature_to_add]
        for member in current_set:
            cols.append(member)
    #backward selection
    else:
        for i in range(len(data.columns)):
            cols.append(i)
        for member in current_set:
            cols.remove(member)
        cols.remove(feature_to_add)
    classes = data[data.columns[0]]
    data = data[data.columns[cols]]
    correct = 0
    possible = 0
    count = 0
    #iterate over all the datapoint (k-fold loop)
    for index, row in data.iterrows():
        possible = random()
        if possible < 0.95:
            continue
        count+=1
        min_distance = 900000000
        min_point = -1
        #looking for nearest neighbor
        for second_index, second_row in data.iterrows():
            possible = random()
            #sampling from dataset for large dataset
            if possible < 0.95:
                continue
            if second_index != index:
                # print("calculating the distance from %d th point to %d th point" % (index, second_index,))
                dist = 0
                for i in range(len(data.columns)):
                    dist += np.square(row.iloc[i] - second_row.iloc[i])
                dist = np.sqrt(dist)
                #replace if a closer point is found
                if dist < min_distance:
                    min_distance = dist
                    min_point = second_index
        print("nearest neighbor of %d is %d" %(index,min_point))
        if classes[index] == classes[min_point]:
            correct += 1
        #sampling from the dataset
        if count > 15:
            break
    print("--correct predictions = %d out of %d instances" % (correct, len(data.index)))
    #used when working with small dataset
    # return correct/len(data.index)
    #used when working with large dataset
    return correct/count


def feature_search_forward(data):
    feature_count = len(data.columns)-1
    added_features = set()
    best_so_far_accuracy = 0
    best_features_so_far = set()
    level_accuracies = []
    #first for going through search tree
    for i in range(1, feature_count):
        print("On the '%d'th level of the search tree" % i)
        best_round_accuracy = 0
        best_member_so_far = -1
        #second for loop going through all the features and finds the best to add
        for k in range(1, feature_count):

            print("--Considering adding the '%d' feature" % k)
            #checks if it was not added before
            if k in added_features:
                print("feature already in the set")
                continue
            #calculates accuracy of adding this feature
            accuracy = leave_one_out_cross_validation(data, added_features, k, 1)
            print("accuracy is %.5f" %accuracy)
            print("best so far accuracy is %.5f" %best_round_accuracy)
            #replace if a btter feature is found
            if accuracy > best_round_accuracy:
                print("replaceing best so far")
                best_round_accuracy = accuracy
                best_member_so_far = k
        added_features.add(best_member_so_far)
        print("This level accuracy is %.5f"%best_round_accuracy)
        level_accuracies.append(best_round_accuracy)
        #keeps track of the global best
        if best_round_accuracy <= best_so_far_accuracy:
            print("accuracy decreased, will continue in case of global best")
        else:
            best_features_so_far = added_features.copy()
            best_so_far_accuracy = best_round_accuracy
    print("best accuracy is %.5f" % best_so_far_accuracy)
    print("best members are:")
    print(best_features_so_far)
    x = []
    print(level_accuracies)
    for i in range(len(level_accuracies)):
        x.append(i + 1)
    pp.bar(x, level_accuracies)
    pp.show()


def feature_search_backwards(data):
    feature_count = len(data.columns) - 1
    print(feature_count)
    print(len(data.index))
    removed_features = set()
    best_so_far_accuracy = 0
    best_features_so_far = set()
    level_accuracies = []
    #adds all the feature so they will be removed one by one
    for i in range(1, feature_count):
        best_features_so_far.add(i)
    #first for loop going through search tree levels
    for i in range(1, feature_count):
        print("On the '%d'th level of the search tree" % i)
        best_round_accuracy = 0
        best_member_so_far = -1
        #second loop going through all the features to find the best one to remove
        for k in range(1, feature_count):
            possible = random()
            # samples from the features to test
            if possible > 0.01 * np.sqrt(i):
                continue
            print("--Considering removing the '%d' feature" % k)
            # checks if already was removed
            if k in removed_features:
                print("---feature already removed")
                continue
            accuracy = leave_one_out_cross_validation(data, removed_features, k, -1)
            print("--accuracy is %.5f" % accuracy)
            print("--best so far accuracy is %.5f" % best_round_accuracy)
            # replaces if found a better feature
            if accuracy > best_round_accuracy:
                print("---replaceing best so far")
                best_round_accuracy = accuracy
                best_member_so_far = k
            # stops if gets 100% accuracy
            if best_round_accuracy == 1:
                break
        removed_features.add(best_member_so_far)
        print("--This level accuracy is %.5f" % best_round_accuracy)
        level_accuracies.append(best_round_accuracy)
        # keeps tracks of overall accuracy
        if best_round_accuracy <= best_so_far_accuracy:
            print("---accuracy decreased, will continue in case of global best")
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
    x =[]
    for i in range(len(level_accuracies)):
       x.append(i+1)
    pp.bar(x,level_accuracies)
    pp.show()


if __name__ == '__main__':
    largeFile = "CS205_large_testdata__27.txt"
    smallFile = "CS205_small_testdata__7.txt"
    df = pd.read_fwf(largeFile)
    data = pd.DataFrame(df)
    # print(data.columns)
    feature_search_forward(data)

