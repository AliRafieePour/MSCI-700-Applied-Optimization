from pyomo.environ import *
import random
import numpy as np
import matplotlib.pyplot as plt

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

www = sum(lis[ii]['z'] for ii in i)
Ls = {'x':59, 'y':59, 'z':www}
Ls2 = {0:59, 1:59, 2:www}


cis = [[0,0,0] for bb in range(NUM_ITEMS)]

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

def pop(n):
    population = []
    for nn in range(n):

        new = [[np.random.randint(0,Ls['x']),np.random.randint(0,Ls['y']),np.random.randint(0,Ls['z'])] for x in range(NUM_ITEMS)]
        
        for itemtoChnage in range(len(lis)):
            for randS in [0,1,2]:
                print("Trying to generate a feasible population")
                if (new[itemtoChnage][randS] + lis2[itemtoChnage][randS]<=Ls2[randS]):
                    continue
                if randS == 0:
                    while(1):
                        randUni = np.random.randint(0, Ls2[randS])
                        if randUni+lis[itemtoChnage]['x']<= Ls2[randS]:
                            new[itemtoChnage][randS] = randUni
                            break
                    continue
                elif randS == 1:
                    while(1):
                        randUni = np.random.randint(0, Ls2[randS])
                        if randUni+lis[itemtoChnage]['y']<= Ls2[randS]:
                            new[itemtoChnage][randS] = randUni
                            break
                    continue
                elif randS == 2:
                    ss = 0
                    for item in range(len(lis)):
                        ss += lis[item]['z']
                    while(1):
                        randUni = np.random.randint(0, 1.25*ss)
                        if randUni+lis[itemtoChnage]['z']<= ss:
                            new[itemtoChnage][randS] = randUni
                            break
                    continue
        if (check(new)):
            population.append(new)
    return population


def elit(popu):
    print("Function elit")
    evaluations = []
    for yy in range(len(popu)):
        score = evaluate(popu[yy], lis)
        evaluations.append([popu[yy], score])
    evaluations.sort(key = lambda x: x[1])
    return evaluations

def check(item):
    print("Function check")
    for box in range(len(item)):
        if (item[box][0]+lis[box]['x'] > Ls['x']):
            print(item[box][0]+lis[box]['x'], Ls['x'])
            return False
        elif (item[box][1]+lis[box]['y'] > Ls['y']):
            print(item[box][1]+lis[box]['y'], Ls['y'])
            return False
        elif (item[box][2]+lis[box]['z'] > Ls['z']):
            print(item[box][2]+lis[box]['z'], Ls['z'])
            return False
    
    return True

def mary(elitgroup, generalpop):
    print("Function mary")
    popu = []
    for tt in elitgroup:
        popu.append(tt[0])
    counter = 0
    while(counter!=250-len(elitgroup)):
        print(counter)

        typee = random.choice([1,2,3])
        r = random.randint(0, len(generalpop)-1)
        a = generalpop[r]
        a = a[0]
        r = random.randint(0, len(generalpop)-1)
        b = generalpop[r]
        b = b[0]
        
        newitem = [0 for qq in range(len(b))]
        if (typee == 1):
            which = random.choice([1,2])
            if (which == 1):
                newitem[::2] = a[::2]
                newitem[1::2] = b[1::2]
                if(check(newitem)):
                    counter += 1
                    pass
                else:
                    newitem = neighbour(newitem, lis)
                
            else:
                newitem[::2] = b[::2]
                newitem[1::2] = a[1::2]    
                if(check(newitem)):
                    counter += 1
                    pass
                else:
                    newitem = neighbour(newitem, lis)                
        elif (typee == 2):
            which = random.choice([1,2])
            newitem = []
            if (which == 1):
                newitem = a[0:len(a)//2]
                newitem[len(a)//2:] = b[len(a)//2:]
                if(check(newitem)):
                    counter += 1
                    pass
                else:
                    newitem = neighbour(newitem, lis)                
            else:
                newitem = b[0:len(a)//2]
                newitem[len(a)//2:] = a[len(a)//2:]
                if(check(newitem)):
                    counter += 1
                    pass
                else:
                    newitem = neighbour(newitem, lis)
        elif (typee == 3):
            which = random.choice([1,2])
            z = np.random.randint(0, len(a))
            x = np.random.randint(0, len(a))
            
            newitem = [0 for ii in range(len(a))]
            if (z>x):
                for ii in range(len(a)):
                    if (ii>=x and ii<=z):
                        newitem[ii] = []
                        for (item1, item2) in zip(a[ii], b[ii]):
                            newitem[ii].append((item1+item2)/2)
                        
                    else:
                        if (which == 1):
                            newitem[ii] = a[ii]
                        else:
                            newitem[ii] = b[ii]
                if(check(newitem)):
                    counter += 1
                    pass
                else:
                    newitem = neighbour(newitem, lis)   
                
            elif (z<=x):
                for ii in range(len(a)):
                    if (ii<=x and ii>=z):
                        newitem[ii] = []
                        for (item1, item2) in zip(a[ii], b[ii]):
                            newitem[ii].append((item1+item2)/2)
                    else:
                        if (which == 1):
                            newitem[ii] = a[ii]
                        else:
                            newitem[ii] = b[ii]
                if(check(newitem)):
                    counter += 1
                    pass
                else:
                    newitem = neighbour(newitem, lis)   
                        
        # elif (typee == 4):
        #     which = random.choice([1,2])
        #     if (which == 1):
        #         newtime = a.copy()
                
            
        popu.append(newitem)
        
            
    return popu

def mutate(item):
    
    yy = np.random.randint(0, len(item))
    xx = np.random.randint(0, len(item[yy]))
    item[yy][xx] = [np.random.randint(0, Ls['x']),np.random.randint(0, Ls['y']),np.random.randint(0, Ls['z'])]
    while(check(item[yy]) == False):
        item[yy][xx] = [np.random.randint(0, Ls['x']),np.random.randint(0, Ls['y']),np.random.randint(0, Ls['z'])]
    return item

    

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

from time import time
def main(initpop):
    
    bests = []
    eli = elit(initpop)
    for rr in range(1000):
        print(f"Loop {rr}")
        newpop = mary(eli[0:30], eli)
        if (random.uniform(0, 1) <= 0.5):
            newpop = mutate(newpop)
        eli = elit(newpop)
        
        bests.append(eli[0][-1])
        if(eli[0][-1] == 0):
            break
    
    plt.plot(bests)
    plt.show()
    print(min(bests))

t1 = time()
initpop = pop(100)
main(initpop)    
t2 = time()
print(t2-t1)