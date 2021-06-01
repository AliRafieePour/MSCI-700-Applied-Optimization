from pyomo.environ import *
import random
import numpy as np
import time
import logging
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

from yellowbrick.cluster import KElbowVisualizer
logging.getLogger('pyomo.core').setLevel(logging.ERROR)


NUM_ITEMS = 20

i = [ii for ii in range(NUM_ITEMS)]
j = [jj for jj in range(NUM_ITEMS)]
s = ['x', 'y', 'z']
np.random.seed(50546)

def generateItems():    
    items = {i: {'x':np.random.randint(20, 60), 'y':np.random.randint(20, 60), 'z':np.random.randint(20, 60)} for i in range(NUM_ITEMS)}
    items2 = []
    for k in range(NUM_ITEMS):
        items2.append([items[k]['x'], items[k]['y'], items[k]['z']])
        
    return items, items2

lis, lis2 = generateItems()

Ls = {'x':59, 'y':59, 'z':200}
Ls2 = {0:59, 1:59, 2:200}


cis = [[0,0,0] for bb in range(NUM_ITEMS)]
time0 = 0
time1 = 0

def neighbour(cis, lis):
    flag = 0
    while(1):
        randS = random.choice([0,1,2])
        itemtoChnage = np.random.randint(0, len(lis))
        if randS == 0:
            randUni = np.random.randint(0, Ls2[randS])
            if randUni+lis[itemtoChnage]['x']<= Ls2[randS]:
                cis[itemtoChnage][randS] = randUni
                break
        elif randS == 1:
            randUni = np.random.randint(0, Ls2[randS])
            if randUni+lis[itemtoChnage]['y']<= Ls2[randS]:
                cis[itemtoChnage][randS] = randUni
                break
        elif randS == 2:
            ss = 0
            for item in range(len(lis)):
                ss += lis[item]['z']
            #print(ss)
            randUni = np.random.randint(0, 1.25*ss)
            if randUni+lis[itemtoChnage]['z']<= ss:
                cis[itemtoChnage][randS] = randUni
                break
    return cis

def evaluate(cis,lis):
    summ = 0
    
#    for item in range(len(lis)):
#        summ +=cis[item][2]+lis[item]['z']

    for item in range(len(lis)):
        for item2 in range(item+1, len(lis)):
            if (cis[item2][0] <= lis[item]['x']+cis[item][0] <= lis[item2]['x']+cis[item2][0] and cis[item][0]>=cis[item2][0]):
                if (cis[item2][1] <= lis[item]['y']+cis[item][1] <= lis[item2]['y']+cis[item2][1] and cis[item][1]>=cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item]['x'] * lis[item]['y'] * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item]['x'] * lis[item]['y'] * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item]['x'] * lis[item]['y'] * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item]['x'] * lis[item]['y'] * lis[item2]['z']
                
                if (cis[item2][1] <= lis[item]['y']+cis[item][1] <= lis[item2]['y']+cis[item2][1] and cis[item][1]<cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * lis[item2]['z']
                
                if (lis[item2]['y']+cis[item2][1] <= lis[item]['y']+cis[item][1] and cis[item2][1]<=cis[item][1]<=cis[item2][1]+lis[item2]['y']):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * lis[item2]['z']
                
                if (lis[item2]['y']+cis[item2][1] <= lis[item]['y']+cis[item][1] and cis[item][1]<cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item]['x'] * lis[item]['y'] * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item]['x'] * lis[item]['y'] * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item]['x'] * lis[item]['y'] * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item]['x'] * lis[item2]['y'] * lis[item2]['z']
            
            if (cis[item2][0] <= lis[item]['x']+cis[item][0] <= lis[item2]['x']+cis[item2][0] and cis[item][0]<cis[item2][0]):
                if (cis[item2][1] <= lis[item]['y']+cis[item][1] <= lis[item2]['y']+cis[item2][1] and cis[item][1]>=cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item2]['x'] * lis[item]['y'] * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item2]['x'] * lis[item]['y'] * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item2]['x'] * lis[item]['y'] * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item2]['x'] * lis[item]['y'] * lis[item2]['z']
                
                if (cis[item2][1] <= lis[item]['y']+cis[item][1] <= lis[item2]['y']+cis[item2][1] and cis[item][1]<cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item2]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item2]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item2]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item2]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * lis[item2]['z']
                
                if (lis[item2]['y']+cis[item2][1] <= lis[item]['y']+cis[item][1] and cis[item2][1]<=cis[item][1]<=cis[item2][1]+lis[item2]['y']):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item2]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item2]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item2]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item2]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * lis[item2]['z']
                
                if (lis[item2]['y']+cis[item2][1] <= lis[item]['y']+cis[item][1] and cis[item][1]<cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item2]['x'] * lis[item]['y'] * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item2]['x'] * lis[item]['y'] * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item2]['x'] * lis[item]['y'] * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item2]['x'] * lis[item2]['y'] * lis[item2]['z']
            
            if (lis[item2]['x']+cis[item2][0] <= lis[item]['x']+cis[item][0] and cis[item2][0]<=cis[item][0]<=cis[item2][0]+lis[item2]['x']):
                if (cis[item2][1] <= lis[item]['y']+cis[item][1] <= lis[item2]['y']+cis[item2][1] and cis[item][1]>=cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * lis[item]['y'] * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * lis[item]['y'] * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * lis[item]['y'] * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * lis[item]['y'] * lis[item2]['z']
                
                if (cis[item2][1] <= lis[item]['y']+cis[item][1] <= lis[item2]['y']+cis[item2][1] and cis[item][1]<cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * (lis[item]['y']+cis[item][1] - cis[item2][1]) * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * (lis[item]['y']+cis[item][1] - cis[item2][1]) * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * (lis[item]['y']+cis[item][1] - cis[item2][1]) * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * (lis[item]['y']+cis[item][1] - cis[item2][1]) * lis[item2]['z']
                
                if (lis[item2]['y']+cis[item2][1] <= lis[item]['y']+cis[item][1] and cis[item2][1]<=cis[item][1]<=cis[item2][1]+lis[item2]['y']):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * lis[item2]['z']
                
                if (lis[item2]['y']+cis[item2][1] <= lis[item]['y']+cis[item][1] and cis[item][1]<cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * lis[item]['y'] * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * lis[item]['y'] * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * lis[item]['y'] * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += (lis[item2]['x']+cis[item2][0] - cis[item][0]) * lis[item2]['y'] * lis[item2]['z']
                        
            if (lis[item2]['x']+cis[item2][0] <= lis[item]['x']+cis[item][0] and cis[item][0]<cis[item2][0]):
                if (cis[item2][1] <= lis[item]['y']+cis[item][1] <= lis[item2]['y']+cis[item2][1] and cis[item][1]>=cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item2]['x'] * lis[item]['y'] * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item2]['x'] * lis[item]['y'] * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item2]['x'] * lis[item]['y'] * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item2]['x'] * lis[item]['y'] * lis[item2]['z']
                
                if (cis[item2][1] <= lis[item]['y']+cis[item][1] <= lis[item2]['y']+cis[item2][1] and cis[item][1]<cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item2]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item2]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item2]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item2]['x'] * (lis[item]['y']+cis[item][1] - cis[item2][1]) * lis[item2]['z']
                
                if (lis[item2]['y']+cis[item2][1] <= lis[item]['y']+cis[item][1] and cis[item2][1]<=cis[item][1]<=cis[item2][1]+lis[item2]['y']):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item2]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item2]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item2]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item2]['x'] * (lis[item2]['y']+cis[item2][1] - cis[item][1]) * lis[item2]['z']
                
                if (lis[item2]['y']+cis[item2][1] <= lis[item]['y']+cis[item][1] and cis[item][1]<cis[item2][1]):
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]>=cis[item2][2]):
                        #the item is completely within item2
                        summ += lis[item2]['x'] * lis[item]['y'] * lis[item]['z']
                    if (cis[item2][2] <= lis[item]['z']+cis[item][2] <= lis[item2]['z']+cis[item2][2] and cis[item][2]<cis[item2][2]):
                        #bottom side of item is out of item2
                        summ += lis[item2]['x'] * lis[item]['y'] * (lis[item]['z']+cis[item][2] - cis[item2][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item2][2]<=cis[item][2]<=cis[item2][2]+lis[item2]['z']):
                        #upper side of item is out of item2 and bottom side within item2
                        summ += lis[item2]['x'] * lis[item]['y'] * (lis[item2]['z']+cis[item2][2] - cis[item][2])
                    if (lis[item2]['z']+cis[item2][2] <= lis[item]['z']+cis[item][2] and cis[item][2]<cis[item2][2]):
                        #upper side of item is out of item2 and bottom side out of item2
                        summ += lis[item2]['x'] * lis[item2]['y'] * lis[item2]['z']

    return summ




def main(cis, lis):
    bests = []
    np.random.seed(np.random.randint(1, 100000))
    BEST = evaluate(cis, lis)
    best = BEST
    CIS = []
    t = 250000
    time0 = time.time()
    for r in range(350000):
        print(f"best={BEST}")
        if (BEST == 0):
            print("bin feasible")
            time1 = time.time()
            print(time1-time0)
            print(f"r: {r}")
            break

        
        newcis = neighbour(cis, lis)
        newbest = evaluate(newcis, lis)
        #print(f"newbest={newbest}")
        if (newbest <= best):
            if (newbest <= BEST):
                bests.append(newbest)
                BEST = newbest
                CIS = newcis
            best = newbest
            cis = newcis
            t *=.99999
            continue
        else:
            diff = -best + newbest
            metro = exp(-diff/t)
            #print(metro)
            
            if np.random.rand() < metro:
                best = newbest
                cis = newcis
                t *=.99999
                continue
    
    return CIS, BEST, bests
        

bb = []
t1 = time.time()
for ff in range(5):
    _, B, bests = main(cis,lis)
    bb.append(B)
t2 = time.time()

import matplotlib.pyplot as plt
plt.plot(bests)
plt.show()

print(f"time= {t2-t1}")

print(bb)