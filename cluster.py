#! /usr/bin/env python

import sys
import levenshtein as l

def wordstream():
   i = 0
   for line in sys.stdin:
      i += 1
      line = line.rstrip().lstrip()
      (_, text) = line.split('\t', 1)
      for w in text.split(','):
         w = w.rstrip().lstrip()
         if w != "":
            yield w

def build_wordlist(stream):
   used = set()
   for w in stream:
      l = w.lower()
      if l not in used:
         used.add(l)
         yield w

def find_nearest(matrix):
   min_d = sys.float_info.max 
   min_i = 0
   min_j = 0
   n = len(matrix)
   for i in range(n):
      for j in range(i+1,n):
         if matrix[i][j] < min_d:
            min_i = i
            min_j = j
            min_d = matrix[i][j]
   return (min_i, min_j, min_d) 

def build_distance_matrix(words):
   n = len(words)
   matrix  = [[0 for x in range(n)] for x in range(n)] 
   clusters = [ [w, ] for w in words]

   for i in range(n):
      clusters[i] = (words[i], )
      for j in range(i+1,n):
         d = l.distance(words[i], words[j]) * 1.0 / max(len(words[i]), len(words[j])) 
         matrix[i][j] = d
         matrix[j][i] = d
      matrix[i][i] = 0.0
   return (matrix, clusters)

def merge_clusters(i, j, matrix, clusters):
   clusters[i] = clusters[i] + clusters[j]
   del clusters[j]

   n = len(matrix[i]) 
   matrix[i] = [min(matrix[i][k], matrix[j][k]) for k in range(n)]
   for k in range(n):
      matrix[k][i] = min(matrix[k][i], matrix[k][j])

   for k in range(n):
      del matrix[k][j]
   
   del matrix[j]

wordlist = list(build_wordlist(wordstream()))
matrix, clusters = build_distance_matrix(wordlist)

while len(clusters) > 1:
   (i,j,min_d) = find_nearest(matrix)
   if min_d > .2:
      break

   print "cluster (%s) is near (%s)" % (clusters[i], clusters[j]) 

   merge_clusters(i,j, matrix, clusters)


for c in clusters:
   print "%s\t%s" % (len(c), "\t".join(c))
