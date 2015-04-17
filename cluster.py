#! /usr/bin/env python

import sys
import levenshtein

def wordstream():
   for line in sys.stdin:
      yield line.rstrip().lstrip()

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


def distance(a,b):
   if len(a) + len(b) < 1:
      return 0

   return float(levenshtein.distance(a.lower(), b.lower())) / max(len(a),len(b))

def build_distance_matrix(words):
   n = len(words)
   matrix  = [[0 for x in range(n)] for x in range(n)] 
   clusters = [ [w, ] for w in words]

   for i in range(n):
      clusters[i] = (words[i], )
      for j in range(i+1,n):
         d = distance(words[i], words[j]) 
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

wordlist = list(wordstream())
matrix, clusters = build_distance_matrix(wordlist)

while len(clusters) > 1:
   (i,j,min_d) = find_nearest(matrix)
   if min_d > .2:
      break

   merge_clusters(i,j, matrix, clusters)


for c in clusters:
   print "%s\t%s" % (len(c), "\t".join(c))
