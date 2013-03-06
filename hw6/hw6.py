import numpy as np
import random
import copy
import heapq
import progressbar as pb
from collections import defaultdict, Counter
from pprint import pprint

import cProfile

import pdb, sys

itercounter = 0

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
    items = set()
    with open(infile, 'r') as f:
        for i,line in enumerate(f):
            items.add(int(line))
    return items    
    
def twosum(items, targetrange):
    count = 0
    widgets = [pb.Percentage(), ' ', pb.Bar(), ' ', pb.ETA()]
    pbar = pb.ProgressBar(widgets=widgets, maxval=len(targetrange)).start()
    hit = {}
    count = 0
    out = open('foo.out', 'w')
    for i,t in enumerate(targetrange):
        for x in items:
            y = t-x
            if y != x and y in items:
                count += 1
                out.write("%i,%i,%i" % (x,y, x + y))
                out.write('\n')
                assert(x+y == t)
                break
        pbar.update(i)
    pbar.finish()
    return count

def medianheap(infile):
    hl = []
    hr = []
    items = []
    s = 0
    with open(infile, 'r') as f:
        for i,line in enumerate(f):
            x = int(line)
            items.append(x)
            if(len(hl) == 0 or x <= -hl[0]):
                heapq.heappush(hl, -x)
            else:
                heapq.heappush(hr, x)

            while len(hl) > len(hr):
                heapq.heappush(hr, -heapq.heappop(hl))
            while len(hl) < len(hr):
                heapq.heappush(hl, -heapq.heappop(hr))
            m = -hl[0]
            # print m
            if len(items) % 2 == 0:
               npm = np.median(sorted(items)[:-1])
            else:
               npm = np.median(items)
            assert(m == int(npm))
            # print hl
            # print hr
            s = (s + m) % 10000
    return s

if __name__ == '__main__':
   import sys
   if len(sys.argv) > 1:
      infile = sys.argv[1]
   # print twosum(readdata('HashInt.txt'), xrange(2500,4001))
   # print twosum(readdata(infile), xrange(60,101))
   print medianheap(infile)

