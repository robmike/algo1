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

class DisjointSet(object):
    def __init__(self):
        self.partitions = {}
    def count(self):
        return len(self.partitions.keys())
    def makeset(self, x):
        self.partitions[x] = [x]
    def find(self, x):
        for rep, elems in self.partitions.iteritems():
            if x in elems:
                return rep
        return None
    def sameset(self, x, y):
        return self.find(x) == self.find(y)
    def merge(self, p, q):
        p = self.find(p)
        q = self.find(q)
        rep = p
        if len(self.partitions[p]) < len(self.partitions[q]):
            rep = q
        a, b = self.partitions[p], self.partitions[q]
        del(self.partitions[p])
        del(self.partitions[q])
        self.partitions[rep] = a + b

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

def dfs(n, rev, tfinish, started, finheap, leader): # FIXME: leader should be a UnionFind
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

   leader, finheap = kos(sorted_nodes, fwd)
   return leader


def main(infile):
   leader = kosaraju(*readdata(infile))
   cnt = Counter(leader.values())
   pprint(cnt.most_common(5))

if __name__ == '__main__':
   import sys
   infile = 'test.txt'
   if len(sys.argv) > 1:
      infile = sys.argv[1]
   main(infile)

