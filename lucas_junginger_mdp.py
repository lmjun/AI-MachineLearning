#!/usr/bin/env python
from __future__ import print_function
import copy
import sys

#open, read file
with open(sys.argv[1], 'r') as this:
	disc = float(this.readline())
	reward = float(this.readline())

	parse = this.readline()
	pInt = float(parse.rsplit(' ', 4)[0])
	pClock = float(parse.rsplit(' ', 4)[1])
	pCount = float(parse.rsplit(' ', 4)[2])
	pBack = float(parse.rsplit(' ', 4)[3])

	lines = this.readlines()
	cols = len(lines[0].rsplit(' '))
	rows = len(lines)
	grid = []

	for c in range(0, cols):
		grid.append([])
		for r in range(0, rows):
			if (c == cols - 1):
				grid[c].append(lines[r].rsplit(' ')[c][:-1])
			else:	
				grid[c].append(lines[r].rsplit(' ')[c])

#U, U' utility vectors for all states in S initialized to 0
U = copy.deepcopy(grid)
for c in range(0, cols):
                for r in range(0, rows):
			if(grid[c][r] == '*'):
				U[c][r] = 0
			elif(grid[c][r] != 'x'):
				U[c][r] = float(grid[c][r])
Up = copy.deepcopy(U)
delta = eps = 0.00001
#delta = maximum change in utility of any state in an iteration
#while delta > eps
while(delta >= eps):
	#assign Up to U and 0 to delta
	U = copy.deepcopy(Up)
	#set delta to 0 each iter
	delta = 0
	
	for c in range(0, cols):
                for r in range(0, rows):
			if(grid[c][r] != 'x'):
            		    	maxA = 0
				rew = reward
				if(grid[c][r] != '*'):
					rew = float(grid[c][r])
				else:
					canMoveTo = []
					#for each action: (N, E, S, W) find sum over all resulting states
					#check boundaries
					if(r > 0 and grid[c][r - 1] != 'x'):
						canMoveTo.append('N')
					if(r < rows - 1 and grid[c][r + 1] != 'x'):
						canMoveTo.append('S')
					if(c > 0 and grid[c - 1][r] != 'x'):
						canMoveTo.append('W')
					if(c < cols - 1 and grid[c + 1][r] != 'x'):
						canMoveTo.append('E')
				
					#canMoveTo has all possible directions from state [c][r]
					#next iterate over canMoveTo for each action
			
					#MOVE NORTH
					add = 0
					if('N' in canMoveTo):
						add = add + pInt * float(U[c][r - 1])
					else:
						add = add + pInt * float(U[c][r])
					if('S' in canMoveTo):
						add = add + pBack * float(U[c][r + 1])
					else:
						add = add + pBack * float(U[c][r])
					if('W' in canMoveTo):
						add = add + pCount * float(U[c - 1][r])
					else:
						add = add + pCount * float(U[c][r])
					if('E' in canMoveTo):
						add = add + pClock * float(U[c + 1][r])
					else:
						add = add + pClock * float(U[c][r])
					if(add > maxA):
						maxA = add
				
					#MOVE WEST
					add = 0
					if('N' in canMoveTo):
						add = add + pClock * float(U[c][r - 1])
					else:
						add = add + pClock * float(U[c][r])
					if('S' in canMoveTo):
						add = add + pCount * float(U[c][r + 1])
					else:
						add = add + pCount * float(U[c][r])
					if('W' in canMoveTo):
						add = add + pInt * float(U[c - 1][r])
					else:
						add = add + pInt * float(U[c][r])
					if('E' in canMoveTo):
						add = add + pBack * float(U[c + 1][r])
					else:
						add = add + pBack * float(U[c][r])
					if(add > maxA):
						maxA = add
				
					#MOVE SOUTH
					add = 0
					if('N' in canMoveTo):
						add = add + pBack * float(U[c][r - 1])
					else:
						add = add + pBack * float(U[c][r])
					if('S' in canMoveTo):
						add = add + pInt * float(U[c][r + 1])
					else:
						add = add + pInt * float(U[c][r])
					if('W' in canMoveTo):
						add = add + pClock * float(U[c - 1][r])
					else:
						add = add + pClock * float(U[c][r])
					if('E' in canMoveTo):
						add = add + pCount * float(U[c + 1][r])
					else:
						add = add + pCount * float(U[c][r])
					if(add > maxA):
						maxA = add
				
					#MOVE EAST
					add = 0
					if('N' in canMoveTo):
						add = add + pCount * float(U[c][r - 1])
					else:
						add = add + pCount * float(U[c][r])
					if('S' in canMoveTo):
						add = add + pClock * float(U[c][r + 1])
					else:
						add = add + pClock * float(U[c][r])
					if('W' in canMoveTo):
						add = add + pBack * float(U[c - 1][r])
					else:
						add = add + pBack * float(U[c][r])
					if('E' in canMoveTo):
						add = add + pInt * float(U[c + 1][r])
					else:
						add = add + pInt * float(U[c][r])
					if(add > maxA):
						maxA = add	
			
					maxA = maxA * disc
				Up[c][r] = rew + maxA
				#if abs(u'[c][r] - u[c][r]) > delta
				if(abs(float(Up[c][r]) - float(U[c][r])) > delta):
					delta = abs(float(Up[c][r]) - float(U[c][r]))

#output correct grid
for r in range(0, rows):
                for c in range(0, cols):
                        if(grid[c][r] == '*'):
				print(U[c][r],end='')
			elif(grid[c][r] == 'x'):
				print('x',end="")
			else:
				print(float(grid[c][r]), end="")
			if(c == cols - 1):
				print('\n',end="")
			else:
				print(' ',end="")


