from subprocess import call
from subprocess import check_output
import copy
import pandas as pd
import numpy as np


def executeSolver(s, h, n, w):
    info = check_output(["./feg", h, "--random", s, n, w, "--FEG", "--compund_moves"])
    info = str(info)
    info = info.replace(" ", '-')
    info = info.replace("n", '')

    states = []
    state = []
    moves = []
    move = []
    countFirstState = 0
    firstStateFlag = True
    stackFlag = False
    digitFlag = False
    moveFlag = False
    for s in info:
        if s == '(':
            moveFlag = True
            move = []
            continue
        elif s == ')':
            moveFlag = False
            #ACA AGREGAR EL ESTADO A ALOS ESTADOS
            moves.append((move[0],move[1]))
            states.append(state)
            state = []
            continue

        if moveFlag:
            if s == ',':
                continue
            else: 
                move.append(int(s))
        else:
            if s == '[':
                stackFlag = True
                digitFlag = True
                stack = []
                digit = ""
                continue
            elif s == ']':
                countFirstState += 1
                stackFlag = False
                state.append(stack)
                stack = []
            if stackFlag:
                if s != '-':
                    digit += s
                else:
                    stack.append(int(digit))
                    digit = ""
                continue
    '''
    if len(states) == len(moves):
        for i in range(len(moves)):
            print('state: ', states[i])
            print('move: ', moves[i])
            print('\n')
    '''
    return states, moves

def compactState(yard):
    sort = []
    for stack in yard:
      for container in stack:
        if not container in sort:
          sort.append(container)
    sort = sorted(sort)
    maxValue = 0
    for i in range(len(yard)):
      for j in range(len(yard[i])):
        yard[i][j] = sort.index(yard[i][j]) + 1
        if yard[i][j] > maxValue:
          maxValue = yard[i][j]

def fillStacksWithCeros(yard, h, max_item):
    for stack in yard:
      while len(stack) < h:
        stack.append(0)
    return yard

def elevateState(yard, h, max_item):
    for stack in yard:
      while len(stack) < h:
        stack.insert(0, max_item)
    return yard

def getStackValues(yard): #sorted stacks?
    values = []
    for stack in yard:
        flag = False
        cont = 0
        for i in range(len(stack)):
            if i==0:
                cont += 1
            else:
                if stack[i] <= stack[i-1]:
                    cont += 1
                else: break
        values.append(cont)
    return values

def getStackLen(yard):
    lens = []
    for stack in yard:
        lens.append(len(stack))
    return lens

def getTopStacks(yard,max_item):
    tops = []
    for stack in yard:
        if len(stack) != 0:
            tops.append(stack[len(stack)-1])
        else:
            tops.append(max_item)
    return tops

def flattenState(state):
    flatten = []
    for lista in state:
        for item in lista:
            flatten.append(item)
    return flatten

def normalizeState(state, max_item):
    np_state = np.array([])
    for stack in state:
        np_state = np.append(np_state, np.array(stack))
    return np_state/max_item

def generateInstances(s, h, n, w, l, name, tec):
    #tec -> [compact, norm, elev] -> [True, False, True]
    flatenStates = []
    movements = []

    for k in range(l):
        print('k: ', k)
        states, moves = executeSolver(s, h, n, w)
        for i, state in enumerate(states):
            maxs = []
            for stack in state:
                maxs.append(max(stack, default=0))
            max_item = max(maxs, default=0)
            stackValues = getStackValues(state)
            stacksLen = getStackLen(state)
            topStacks = getTopStacks(state, max_item)
            if tec[2]:
                elevateState(state, int(h), max_item)
            else:
                fillStacksWithCeros(state, int(h), max_item)
            if tec[0]:
                compactState(state)
            if tec[1]:
                state = normalizeState(state, max_item)
            if tec[0] == False and tec[1] == False and tec[2] == False: 
                fillStacksWithCeros(state, int(h), max_item)
            state = np.append(state, stackValues)
            state = np.append(state, stacksLen)
            state = np.append(state, topStacks)
            print('state.shape: ', state.shape)
            flatenStates.append(state)
        movements.append(moves)

    movements = flattenState(movements)
    x = pd.DataFrame(flatenStates)
    y = pd.DataFrame(movements)
    x.to_csv('./datasets/x'+ name +'.csv', header=False, index=False)
    y.to_csv('./datasets/y'+ name +'.csv', header=False, index=False)

#tec -> [compact, norm, elev] -> [True, False, True]
print('cne')
generateInstances('5', '7', '25', '5000', 300, 'bsg5x7-cne', [True, True, True])
print('cn')
generateInstances('5', '7', '25', '5000', 300, 'bsg5x7-cn', [True, True, False])
print('c')
generateInstances('5', '7', '25', '5000', 300, 'bsg5x7-c', [False, False, False])
#generateInstances('5', '7', '25', '100', 1, 'test-bsg5x7-c', [False, True, False])