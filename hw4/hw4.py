import numpy as np
import random
import copy
import heapq
import progressbar as pb
from collections import defaultdict

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
    fwd = defaultdict(lambda: [])
    rev = defaultdict(lambda: [])
    nodes = []
    seen = {}
    h = []
    with open(infile, 'r') as f:
        for i,line in enumerate(f):
            u, v = [int(x) for x in line.split()]
            fwd[u].append(v)
            rev[v].append(u)
            for w in [u,v]:
               try:
                  seen[w]
               except KeyError:
                  seen[w] = True
                  heapq.heappush(h, -w)
    while(h):
        nodes.append(-heapq.heappop(h))
    return nodes, fwd, rev

def dfs(n, rev, tfinish, started, finheap, leader):
   stack = [n]
   while(stack):
      u = stack.pop()
      if u < 0:                 # sentinel, node is finished
         heapq.heappush(finheap, (-tfinish, -u)) # maxheap
         tfinish += 1
         continue

      try: # If node has been started
         started[u]
      except KeyError:
         # Node not been started, mark as started, add successors to stack
         started[u] = True
         leader[u] = n
         stack.append(-u)           # sentinel to mark when finished
         for v in reversed(rev[u]): # Reversed to keep node order with lectures
            stack.append(v)
   return tfinish
         
def kos(nodes, rev):
    tfinish = 0
    seen = {}
    leader = {}
    finheap = []
    
    for n in nodes:
       try:
          seen[n]
          continue
       except KeyError:
          tfinish = dfs(n, rev, tfinish + 1, seen, finheap, leader)
    return leader, finheap

def kosaraju(nodes, fwd, rev):
   leader, finheap = kos(nodes, rev)

   sorted_nodes = []
   while(finheap):
      sorted_nodes.append(heapq.heappop(finheap)[1])

   import pdb
   pdb.set_trace()
   leader, finheap = kos(sorted_nodes, fwd)
   return leader


def main():
   leader = kosaraju(*readdata('test.txt'))

x = {'a': 1}
def foo(y):
   y['b'] = 3
