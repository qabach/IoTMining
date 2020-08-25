#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
                    
                    uniqueSegments = np.unique(currentDataTable[:,3])
                    
                    for uniqueSegment in uniqueSegments:
                        if (not id in baskets):
                            baskets[id] = [tuple(set(currentDataTable[:, 4]))]
                        else:
                            baskets[id].extend([tuple(set(currentDataTable[:, 4]))])
            
        # if ((dataTable is None) & (len(weekDataTable) > 0)):
        #     dataTable = weekDataTable
        # elif (len(weekDataTable) > 0):
        #     dataTable = np.concatenate([dataTable, weekDataTable])
        
    
    
                    
    rulesList = []
    itemsetsList = [] 
    sizeOfRules = []
    for id in baskets:
        #print("Basket", baskets[id])
        
        itemsets, rules = apriori(baskets[id], min_support=0.9, min_confidence=1, max_length=2)
        rulesList.append(rules)
        itemsetsList.append(itemsets)
        sizeOfRules.append(len(rules))
        #print( "size of rules: " + str(len(rules)))
        #print("size of basket : " + str(len(baskets)))
        #for elem in rules:
            #print(elem)

                    
            
    # print("Baskets", baskets)
    return itemsetsList, rulesList, sizeOfRules, len(baskets)

        
def rulesGenerator():
    
    path = './npy/prunedDataByWeek/'
    weekCount = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    
    #compute the total number of sliding window
    windowCount = weekCount - sizeOfSlidingWindow + 1  #algor:(n-k+1) with k is the size of sliding window
    
    if not os.path.exists('./ppRules/'):
            os.makedirs('./ppRules/')
    for i in range(0,windowCount+1):
        itemsetsList, rulesList, sizeOfRules,basketsSize = findFrequentSets(tuple(range(i,i+3)))
        outFile = open('./ppRules/f' + str(i) + 't' +str(i+3) + '.txt', 'w')
        outFile.write("size of baskets: " + str(basketsSize))
        outFile.write("\n")
        for i in range(0,len(sizeOfRules)):
            outFile.write("size of rule list: " + str(sizeOfRules[i]))
            outFile.write("\n")
            for j in range(0,len(rulesList)):
                outFile.write(str(rulesList[j]))
                outFile.write("\n")
                outFile.write("\n")
            
        outFile.close()
        
#rulesGenerator()
        

