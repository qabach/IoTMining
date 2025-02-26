#!/usr/bin/env python3

# Research: Incremental Learning from IoT for Smart Home Automation
# Authors: Nguyen Do, Quan Bach
# Usage:
# Time Threshold Based Association Rules Generator
# By running rulesGenerator(), this function will get into the imported and pruned data,
# runs the apriori algorithm per sliding window of 4 weeks and generate the rules

import utils
from utils import sizeOfSlidingWindow
import os
from datetime import datetime, time, timedelta
import numpy as np
from numpy.core.defchararray import find
from efficient_apriori import apriori

def findFrequentSets(weeks):
    dataTable = None
    baskets = {} # dictionary
    for week in weeks:
        filename = "./npy/prunedDataByWeek/week" + str(week) + ".npy"
        weekDataTable = []
        try:
            weekDataTable = np.load(filename, allow_pickle = True)
        except:
            print(filename, "doesn't exist.")
            
            
        if (len(weekDataTable) > 0):
            for dayInWeek in range(0,6):
                for partitionTimeIndex in utils.timePartitionMap:
                    idx = (weekDataTable[:, 1] == dayInWeek) & (weekDataTable[:, 2] == int(partitionTimeIndex))
                    
                    currentDataTable = weekDataTable[idx]
                    id = str(dayInWeek) + partitionTimeIndex
                    # print('currentDataTable', tuple(set(currentDataTable[:, 3])))
                    
                    if (len(currentDataTable) == 0):
                        continue
                    
                    uniqueSegments = np.unique(currentDataTable[:,4])
                    
                    for uniqueSegment in uniqueSegments:
                        if (not id in baskets):
                            baskets[id] = [tuple(set(currentDataTable[:, 5]))]
                        else:
                            baskets[id].extend([tuple(set(currentDataTable[:, 5]))])        
                    
    rulesList = []
    itemsetsList = [] 
    sizeOfRules = []
    for id in baskets:        
        itemsets, rules = apriori(baskets[id], min_support=0.5, min_confidence=1, max_length=2)
        itemsetsList.append(itemsets)
    
        rulesFilter = filter(lambda rule: findActuator(rule), rules)
        filteredRules = []
        for rule in rulesFilter:
            filteredRules.append(rule)
        
        rulesList.append([id, filteredRules])
 
    return itemsetsList, rulesList, len(baskets)

def findActuator(tup):
    return all((any(substr in e for substr in ['Light', 'fan'])) for e in tup.rhs)
        
def rulesGenerator():
    
    path = './npy/prunedDataByWeek/'
    weekCount = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    
    #compute the total number of sliding window
    windowCount = weekCount - sizeOfSlidingWindow + 1  #algor:(n-k+1) with k is the size of sliding window
    
    if not os.path.exists('./ttRules/'):
            os.makedirs('./ttRules/')
    
    if not os.path.exists('./npy/demoData/'):
            os.makedirs('./npy/demoData/')
    
    ruleSizeFile = open('./ttRules/ruleSize.txt', 'a+')
    for i in range(0, windowCount+1):
        dataTable = []
        itemsetsList, rulesList, basketsSize = findFrequentSets(tuple(range(i, i+3)))
        outFile = open('./ttRules/f' + str(i) + 't' +str(i+3) + '.txt', 'w')
        outFile.write("size of baskets: " + str(basketsSize))
        outFile.write("\n")
        for j in range(0, basketsSize):
            ruleSizeFile.write("\n")
            outFile.write("date time segment: " + str(rulesList[j][0]) + "\n")
            outFile.write("size of rule list: " + str(len(rulesList[j][1])))
            outFile.write("\n")
            outFile.write(str(rulesList[j]))
            outFile.write("\n")
            outFile.write("\n")
            dataTable.append([str(rulesList[j][0]),str(rulesList[j])])
        np.save('./npy/demoData/set' + str(i), dataTable)
        outFile.close()

rulesGenerator()
        

