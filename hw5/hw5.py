import numpy as np
import random
import copy
import heapq
import progressbar as pb
from collections import defaultdict, Counter
from pprint import pprint

import cProfile

import pdb, sys

# debug shit (from stackexchange)
def info(type, value, tb):
   if hasattr(sys, 'ps1') or not sys.stderr.isatty():
      # we are in interactive mode or we don't have a tty-like
      # device, so we call the default hook
      sys.__excepthook__(type, value, tb)
   else:
      import traceback, pdb
      # we are NOT in interactive mode, print the exception...
      traceback.print_exception(type, value, tb)
      print
      # ...then start the debugger in post-mortem mode.
      pdb.pm()

sys.excepthook = info

def readdata(infile): 
    edges = {}
    nodes = set()
    with open(infile, 'r') as f:
        for i,line in enumerate(f):
            x = line.split()
            u = int(x.pop(0))
            nodes.add(u)
            for y in x:
                v, cost = [int(z) for z in y.split(',')]
                a,b = u,v
                if a > b:
                    a,b = b,a
                edges[(a,b)] = cost
    return edges, nodes

# Not sure I like this implementation. Choose cheapest vertex so far
# and explore neighbors is seems to make more sense

def dijkstra(start, edgs, nods):
    edges = copy.deepcopy(edgs)
    nodes = copy.deepcopy(nods)
    best = {}
    best[start] = 0
    nodes.remove(start)

    while(edges and nodes):
        mincost = 2**30         # big int. FIXME: get (max edge cost)*(number of edges-1) during read
        minedge = None
        for (u,v), cost in edges.items():
            for x,y in [(u,v), (v,u)]:
                try:            # try x in best but y not
                    best[x]
                    try:
                        best[y]
                        break
                    except KeyError:
                        thiscost = best[x] + cost
                        if thiscost < mincost:
                            mincost = thiscost
                            minedge = (x,y)
                        break
                except:
                    continue

        x, y = minedge
        u, v = x, y
        if u > v:
           u, v = v, u
        del edges[(u,v)]
        best[y] = mincost
        nodes.remove(y)
    return best


edges, nodes = readdata('dijkstraData.txt')
# edges, nodes = readdata('test2.txt')
best = dijkstra(1, edges, nodes)
targets = [7,37,59,82,99,115,133,165,188,197]
# targets = range(1,7)
print([best[x] for x in targets])
