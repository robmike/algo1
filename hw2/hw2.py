import numpy as np

import pdb, sys
sys.setrecursionlimit(21000)    # FIXME: Make solution iterative (just use a stack)

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

def partition(a, pivotidx=0):
    if len(a) < 2:
        return 0
    if pivotidx != 0:
        a[0], a[pivotidx] = a[pivotidx], a[0] # swap
    pivot = a[0]
    i = 1
    j = 1
    for j in xrange(1,len(a)):
        if(a[j] < pivot):
            a[i], a[j] = a[j], a[i]
            i += 1
    a[0], a[i-1] = a[i-1], a[0]
    return i-1

def quicksorthelper(a, fpivotsel):
    n = len(a)
    if n < 2:
        return 0
    pivotidx = fpivotsel(a)
    count = n - 1
    i = partition(a, pivotidx)
    count += quicksort(a[:i], fpivotsel)
    count += quicksort(a[i+1:], fpivotsel)
    return count

def quicksort(a, fpivotsel = lambda x: 0):
    return quicksorthelper(a, fpivotsel)

def readdata(infile='QuickSort.txt'):
    size = 10000
    a = np.empty((size,), dtype='int32')
    with open(infile, 'r') as f:
        for i,line in enumerate(f):
            a[i] = int(line)
    return a

def median3(x):
   y = [x[0], x[(len(x)-1)//2], x[-1]]
   if y[0] >= min(y[1],y[2]) and y[0] <= max(y[1], y[2]):
      return 0
   if y[2] >= min(y[0],y[1]) and y[2] <= max(y[0], y[1]):
      return len(x) - 1
   return (len(x) -1)//2

a = readdata()
x = np.copy(a)
print quicksort(x) # 49995000
x = np.copy(a)
print quicksort(x, lambda x: len(x) - 1) # 164123
x = np.copy(a)
print quicksort(x, median3)
