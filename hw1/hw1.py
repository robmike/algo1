import numpy as np

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

def mergeandcount(la, ra):
    n = len(la)+len(ra)
    out = np.empty((n,), dtype='int32')
    i, j = 0, 0
    count = 0
    for k in xrange(n):
        if la[i] < ra[j]:
            out[k] = la[i]
            i += 1
            if i >= len(la):
                out[k+1:] = ra[j:]
                break
        else:
            out[k] = ra[j]
            j += 1
            count += len(la) - i
            if j >= len(ra):
                out[k+1:] = la[i:]
                count += len(la) - i
                break
    return (out, count)

def sortandcount(array):
    n = len(array)
    if n == 1:
        return (array, 0)
    else:
        (la, lc) = sortandcount(array[1:n//2])
        (ra, rc) = sortandcount(array[n//2:])
        (srta, s) = mergeandcount(la, ra)
        return (array, n + l + s)
    

def readdata(infile='IntegerArray.txt'):
    size = 100000
    array = np.empty((size,), dtype='int32')
    with open(infile, 'r') as f:
        for i,line in enumerate(f):
            try:
                array[i] = int(line)
            except IndexError:
                print i
    return array

sortandcount(readdata())