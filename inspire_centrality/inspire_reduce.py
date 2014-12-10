from mrjob.job import MRJob
from math import sqrt
import json

def cleanname(name):
  parts = name.split(',')
  lastname = parts[0]
  lastname = lastname.strip().replace(' ', '_')
  if len(parts) > 1 and len(parts[1].strip()) > 0:
    firstinit = parts[1].strip()[0]
  else:
    firstinit = ""
  return lastname + '_' + firstinit


class MRInspireReduce(MRJob):
  def mapper(self, _, line):
    paper = json.loads(line)
    authors = []
    authors.extend([cleanname(a) for a in paper['authors']])
    authors.extend([cleanname(a) for a in paper['co-authors']])

    if len(authors) < 50:
      for i in xrange(len(authors)):
        for j in xrange(len(authors)):
          if i != j:
            yield authors[i], [authors[j], 1/float(len(authors) - 1)]

  def reducer(self, key, values):
    collabs = {}
    for collab, weight in values:
      if collab not in collabs.keys():
        collabs[collab] = 0
      collabs[collab] += weight
    yield key, collabs

if __name__ == '__main__':
    MRInspireReduce.run()
