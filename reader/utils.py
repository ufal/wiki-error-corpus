# *-* coding: utf-8 *-*

"""Utility functions.

"""
import numpy as np
import sys

def levenshtein_distance(s, t):
  """Minimum edit distance between two strings.

  Args:
    s: Source string
    t: Target string

  Returns:
    int: Minimum edit distance between the two input strings.

  """
  m = len(s)
  n = len(t)
  if m == 0:
    return n
  if n == 0:
    return m
  d = np.zeros((m+1, n+1))
  print d.shape
  d[:, 0] = np.arange(m+1)
  d[0, :] = np.arange(n+1)
  for j in range(1, n+1):
    for i in range(1, m+1):
      if s[i-1] == t[j-1]:
        d[i][j] = d[i-1][j-1]
      else:
        d[i][j] = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+1)
  return int(d[m][n])
