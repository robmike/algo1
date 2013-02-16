import numpy as np
import random
import copy
import progressbar as pb

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

def readdata(infile='kargerMinCut.txt'): 
    a = []
    with open(infile, 'r') as f:
        for i,line in enumerate(f):
            a.append(sorted([int(x) for x in line.split()])) # FIXME: don't need to traverse list twice 
    return a

# def elemremove(b, j, v):
#     while j > 0 and b[j] == v:
#         j -= 1
#     l = j + 1
#     while l < len(b) and b[l] == v:
#         l += 1
#     b = b[:j+1] + b[l:]
#     # print l, j
#     return b, l - j - 1

def elemremove(b, j, v):        # fixme: list is sorted, remove requires linear scan each time
   count = 0
   while 1:
      try: 
         b.remove(v)
         count += 1
      except:
         break
   return b, count

def nelems2d(x):
   return sum([len(z) for z in x])

def randsel2d(x):
   n = nelems2d(x)
      
   k = random.randint(1, n)
   cumsum = 0
   j = 0
   
   for i,c in enumerate(x):
      if cumsum + len(c) >= k:
         j = k - cumsum - 1
         return i,j
      else:
         cumsum += len(c)
   pdb.set_trace()
   return None

def randmincut(x):
    active = range(1,201)
    nedges = nelems2d(x)
    nvert = len(x)
    while nvert > 2:
       
        i,j = randsel2d(x)
        v = x[i][j]

        x[i], count = elemremove(x[i], j, v)
        nedges -= count

        try:
            idx = x[v-1].index(i)
            x[v-1], count = elemremove(x[v-1], idx, i)
            nedges -= count
        except ValueError:
            pass

        x[i] = sorted(x[i] + x[v-1]) # fixme: lists are already sorted, just merge
        x[v-1] = []

        nvert -= 1
        nedges = nelems2d(x)

        for y in x:
           for k, e in enumerate(y):
              if e == v:
                 y[k] = i

    return nedges

def main():
   a = readdata()
   ntrials = 500
   cutsize = len(a)*len(a)         # bignum

   random.seed(31415)
   #widgets = [pb.Percentage(), ' ', pb.Bar(), ' ', pb.ETA()]
   #pbar = pb.ProgressBar(widgets=widgets, maxval=ntrials).start()

   for i in xrange(0, ntrials):
      x = copy.deepcopy(a)
      newcut = randmincut(x)
      cutsize = min(cutsize, newcut)
      print cutsize, newcut
      # pbar.update(i)
      
   #pbar.finish()
   print cutsize

main()